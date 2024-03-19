
"""Defines the Django Models associated with the admin app.

Each Django model is releated to one database table, and can be linked with
other models. This class defines the datatypes of each attribute (column) 
and any additonal methods that relate to that table.
"""

from django.db import models

class Event(models.Model):
    """Contains information about an event.
    
    Attributes:
        id (int): A unique identifier for the event, auto-incremented.
        type (int): An identifier for which type of event this is.
        target (int): The target amount of CO2 saved or number of journeys
        building (str): A string representing a building on campus
        endDate (date): The end date for this event
    """
    id = models.AutoField(primary_key=True, auto_created=True, unique=True)
    type = models.PositiveIntegerField(null=False, blank=False)
    target = models.PositiveIntegerField(null=True, blank=True, default=50)
    building = models.CharField(max_length=200, null=True, blank=True)
    endDate = models.DateField(null=False, blank=False)

