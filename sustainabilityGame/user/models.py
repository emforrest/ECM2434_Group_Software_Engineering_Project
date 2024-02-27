
"""Defines the Django Models associated with the users.

Each Django model is releated to one database table, and can be linked with
other models. This class defines the datatypes of each attribute (column) 
and any additonal methods that relate to that table.

Authors:
- Sam Townley
"""

from django.db import models
from main.models import Location
from django.contrib.auth.models import User


class Profile(models.Model):
    """Contains any information about a user that isn't related to authentication.

    Attributes:
        user (User): A one-to-one relationship with the built in User model.
        total_saving (float): The total carbon savings of a user across all journeys.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_saving = models.FloatField(default=0)
    
    
class Journey(models.Model):
    """Contains information about each journey, linked to a user.
    
    To conform to GDPR, locations off-campus (origin) are only stored as long as
    they are needed. In this case, the last 10 journeys from a user will store
    an origin incase the user wants to re-record the same journey.

    Attributes:
        id (int): A unique identifier for the journey, auto-incremented.
        user (User): A reference to a primary key on the built in User model.
        distance (float): the distance travelled in KM.
        origin (Location): A reference to a location stored inside the main_location table. 
        destination (str): The on-campus location stored as a string.
        transport (str): A string representing the mode of transport.
        time_logged (datetime): The time the journey was recorded in the system.
    """
    id = models.AutoField(primary_key=True, auto_created=True, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    distance = models.FloatField(blank=False)
    origin = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    destination = models.CharField(max_length=128)
    transport = models.CharField(max_length=16, blank=False)
    time_logged = models.DateTimeField(auto_now_add=True)