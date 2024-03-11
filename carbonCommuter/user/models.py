
"""Defines the Django Models associated with the users.

Each Django model is releated to one database table, and can be linked with
other models. This class defines the datatypes of each attribute (column) 
and any additonal methods that relate to that table.

Authors:
- Sam Townley
"""

from django.db import models
from main.models import Location
from datetime import date, timedelta
from django.contrib.auth.models import User


class JourneyManager(models.Manager):
    
    def get_all_time_savings(self, user: User):
        return self.filter(user=user).aaggregate(models.Sum('carbon_savings'))['carbon_savings__sum']
    
    def get_weekly_savings(self, user: User):
        start = date.today() - timedelta(days=(date.today().weekday() + 1) % 7)
        end = start + timedelta(days=7)
        return self.filter(user=user, time_started__range=(start, end)).aaggregate(models.Sum('carbon_savings'))['carbon_savings__sum']
    
    def get_monthly_savings(self, user: User):
        start = date.today().replace(day=1)
        end = start + timedelta(months=1)
        return self.filter(user=user, time_started__range=(start, end)).aaggregate(models.Sum('carbon_savings'))['carbon_savings__sum']
    
 
class Journey(models.Model):
    """Contains information about each journey, linked to a user.
    
    To conform to GDPR, locations off-campus (origin) are only stored as long as
    they are needed. In this case, the last 10 journeys from a user will store
    an origin incase the user wants to re-record the same journey.

    Attributes:
        id (int): A unique identifier for the journey, auto-incremented.
        user (User): A reference to a primary key on the built in User model.
        distance (float): The distance travelled in KM.
        carbon_savings (float): The CO2 saved (in KG) for the journey.
        origin (Location): A reference to the origin location as stored inside the main_location table. 
        destination (Location): A reference to the destination location as stored inside the main_location table. 
        transport (str): A string representing the mode of transport.
    """
    id = models.AutoField(primary_key=True, auto_created=True, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    distance = models.FloatField(null=False, blank=True, default=0)
    carbon_savings = models.FloatField(null=False, blank=True, default=0)
    origin = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=False, related_name='origin')
    destination = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True, related_name='destination')
    transport = models.CharField(max_length=16, blank=False, null=False)
    time_started = models.DateTimeField(null=False, blank=False)
    time_finished = models.DateTimeField(null=True, blank=True)
    objects = JourneyManager()
    
    
class Profile(models.Model):
    """Contains any information about a user that isn't related to authentication.

    Attributes:
        user (User): A one-to-one relationship with the built in User model.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_saving = models.FloatField(default=0)
    active_journey = models.ForeignKey(Journey, on_delete=models.SET_NULL, null=True, blank=True)
    
    def get_total_savings(self):
        return Journey.objects.get_all_time_savings(self.user)
    
    def has_active_journey(self):
        if self.active_journey is None:
            return False
        else:
            return True