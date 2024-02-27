
"""Defines the Django Models associated with the users.

Each Django model is releated to one database table, and can be linked with
other models. This class defines the datatypes of each attribute (column) 
and any additonal methods that relate to that table.

Authors:
- Sam Townley
"""

from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """Contains any information about a user that isn't related to authentication.

    Attributes:
        user (User): A one-to-one relationship with the built in User model.
        total_saving (float): The total carbon savings of a user across all journeys.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_saving = models.FloatField(default=0)