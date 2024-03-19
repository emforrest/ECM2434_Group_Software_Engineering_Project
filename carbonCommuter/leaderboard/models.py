
"""Defines the Django Models associated with the leaderboard app.

Each Django model is releated to one database table, and can be linked with
other models. This class defines the datatypes of each attribute (column) 
and any additonal methods that relate to that table.
"""

from django.db import models

class Leaderboard_Entry: 
    position : int
    name : str
    totalCo2Saved : float 
    id : int
    username : str

# Create your models here.
