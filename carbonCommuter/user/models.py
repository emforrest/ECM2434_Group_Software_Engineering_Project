
"""Defines the Django Models associated with the users.

Each Django model is releated to one database table, and can be linked with
other models. This class defines the datatypes of each attribute (column) 
and any additonal methods that relate to that table.

Authors:
- Sam Townley
- Eleanor Forrest
"""

from django.db import models
from main.models import Location
from datetime import date, timedelta
from django.contrib.auth.models import User


class JourneyManager(models.Manager):
    """A custom manager for journey's to allow abstraction of methods commonly used for querying the Journey table."""
    
    def get_all_time_savings(self, user: User) -> float:
        """Calculates the total amount of CO2 saved for all journeys made in a User's lifetime on the system.

        Args:
            user (User): The user object to retrieve results for.

        Returns:
            float: The total amount of CO2 saved measured in KG.
        """
        return self.filter(user=user).aggregate(models.Sum('carbon_savings'))['carbon_savings__sum']
    
    def get_weekly_savings(self, user: User) -> float:
        """Calculates the total amount of CO2 saved for all journeys made in the current week, starting from Monday.

        Args:
            user (User): The user object to retrieve results for.

        Returns:
            float: The total amount of CO2 saved measured in KG.
        """
        # Get a date for the monday of the current week, and the sunday of the same week.
        start = date.today() - timedelta(days=date.today().weekday())
        end = start + timedelta(days=6)
        return self.filter(user=user, time_started__range=(start, end)).aggregate(models.Sum('carbon_savings'))['carbon_savings__sum']
    
    def get_monthly_savings(self, user: User) -> float:
        """Calculates the total amount of CO2 saved for all journeys made in the current month, starting from the first day of the month.

        Args:
            user (User): The user object to retrieve results for.

        Returns:
            float: The total amount of CO2 saved measured in KG.
        """
        # Get a date for the first day of the current month, and the last day of the current month.
        start = date.today().replace(day=1)
        end = start + timedelta(months=1) - timedelta(days=1)
        return self.filter(user=user, time_started__range=(start, end)).aggregate(models.Sum('carbon_savings'))['carbon_savings__sum']
    
 
class Journey(models.Model):
    """Contains information about each journey, linked to a user.
    
    To conform to GDPR, locations off-campus (origin) are only stored as long as
    they are needed. In this case, the last 10 journeys from a user will store
    an origin incase the user wants to re-record the same journey.

    Attributes:
        id (int): A unique identifier for the journey, auto-incremented.
        user (User): A reference to a primary key on the built in User model.
        distance (float): The distance travelled (in KM).
        carbon_savings (float): The CO2 saved (in KG) for the journey.
        origin (Location): A reference to the origin location as stored inside the main_location table. 
        destination (Location): A reference to the destination location as stored inside the main_location table. 
        transport (str): A string representing the mode of transport.
        time_started (datetime): The time the journey was started in the system.
        time_finished (datetime): The time the journey was marked as finished.
        estimated_time (float): The time the journey was estimated to take (in minutes), not accounting for traffic. Used for verification only.
        flagged (bool): A flag to indicate whether the journey is considered to be suspicious and should be manually reviewed.
        reason (str): A reason for why the journey is considered suspicious.
        objects (JourneyManager): Overwrite the default model manager with our custom manager defined above.
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
    estimated_time = models.FloatField(null=True, blank=True)
    flagged = models.BooleanField(null=False, blank=True, default=False)
    reason = models.CharField(max_length=255, blank=True, null=True)
    objects = JourneyManager()
    
    
class Profile(models.Model):
    """Contains any information about a user that isn't related to authentication.

    Attributes:
        user (User): A one-to-one relationship with the built in User model.
        active_journey (Journey): A reference to an incomplete journey for the current user if one exists. Will be none otherwise.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    active_journey = models.ForeignKey(Journey, on_delete=models.SET_NULL, null=True, blank=True)
    streak = models.IntegerField(default=0)
    
    def get_total_savings(self) -> float:
        """Gets the total CO2 savings for the current user, using the JourneyManager.

        Returns:
            float: The total amount of CO2 saved measured in KG.
        """
        return Journey.objects.get_all_time_savings(self.user)
    
    def has_active_journey(self) -> bool:
        """Checks if the current user object has an active journey associated with their account.

        Returns:
            bool: True if the user has an active journey, false otherwise.
        """
        if self.active_journey is None:
            return False
        else:
            return True
        

class Follower(models.Model):
    """Represents the following relationship between users

    Attributes:
    follower (User) - The user who is following another user
    followedUser (User) - The user who is being followed
    """
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    followedUser = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('follower', 'followedUser') #There should only be one 'following' relationship from the first user to the second user.
        
        

class Badges(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True, unique=True, default=0)
    name = models.CharField(max_length=100, blank=False, default="")
    #description = models.TextField()

class UserBadge(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    badge = models.ForeignKey(Badges, on_delete=models.CASCADE)
    #collected = models.BooleanField(default=False)
    def get_badges(user) -> list:
        """Gets all the badges one user has achieved

        Returns:
            list: A list of all badges
        """
        badges = UserBadge.objects.all().filter(user=user)
        return badges
