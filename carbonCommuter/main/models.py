
"""Defines the Django Models that aren't related to a particular app.

Each Django model is releated to one database table, and can be linked with
other models. This class defines the datatypes of each attribute (column) 
and any additonal methods that relate to that table.

Authors:
- Sam Townley
"""

from django.db import models


class Location(models.Model):
    """Contains information about a geographical location (on or off campus).

    Attributes:
        id (int): A unique identifier for the location, automatically generated.
        name (str): An optional name used to identify the location.
        lat (float): The latitude of the location.
        lng (float): The longitude of the location.
        address (str): The full address of the location.
        on_campus (bool): Whether or not the location is location inside campus.
        type (str): The type of location. Used to distinguish between areas on campus, e.g. Bus Stops or Bike Racks
    """
    id = models.AutoField(primary_key=True, auto_created=True, unique=True)
    name = models.CharField(max_length=64, null=True, blank=True)
    lat = models.FloatField(null=False, blank=False)
    lng = models.FloatField(null=False, blank=False)
    address = models.CharField(max_length=255, null=False, blank=False, db_index=True)
    on_campus = models.BooleanField(null=False, blank=True, default=False)
    type = models.CharField(max_length=32, null=True, blank=True)
    