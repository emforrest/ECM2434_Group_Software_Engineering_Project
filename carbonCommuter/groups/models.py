from django.db import models
from django.contrib.auth.models import Group, User


class GroupProfile(models.Model):
    objects = None
    group = models.OneToOneField(Group, on_delete=models.CASCADE, related_name='profile')
    leader = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.group.name} led by {self.leader.username}"

