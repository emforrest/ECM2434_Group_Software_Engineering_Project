
"""Defines the Django Models that aren't related to a particular app.

Each Django model is releated to one database table, and can be linked with
other models. This class defines the datatypes of each attribute (column) 
and any additonal methods that relate to that table.

Authors:
- Sam Townley
"""

from django.db import models


class Location(models.Model):
    """Contains information about a location outside of campus.

    Attributes:
        id (int): A unique identifier for the location, automatically generated.
        lat (float): The latitude of the location.
        lng (float): The longitude of the location.
        address (string): The full address of the location.
        postcode (string): The postcode of the location.
    """
    id = models.AutoField(primary_key=True, auto_created=True, unique=True)
    lat = models.FloatField(blank=False)
    lng = models.FloatField(blank=False)
    address = models.CharField(max_length=256, blank=False, unique=True)
    postcode = models.CharField(max_length=16, blank=False)