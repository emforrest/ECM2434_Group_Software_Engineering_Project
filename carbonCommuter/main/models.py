
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
    """
    id = models.AutoField(primary_key=True, auto_created=True, unique=True)
    name = models.CharField(max_length=64, null=True, blank=True)
    lat = models.FloatField(null=False, blank=False)
    lng = models.FloatField(null=False, blank=False)
    address = models.CharField(max_length=255, null=False, blank=False, unique=True, db_index=True)
    on_campus = models.BooleanField(null=False, blank=True, default=False)
    type = models.CharField(max_length=32, null=True, blank=True)
    