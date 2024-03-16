from django.db import models
from django.contrib.auth.models import Group, User


class GroupProfile(models.Model):
    group = models.OneToOneField(Group, on_delete=models.CASCADE)
    leader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='led_groups')
    is_private = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.group.name} led by {self.leader.username}"


class GroupJoinRequest(models.Model):
    objects = None
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='join_requests')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='join_requests')
    created_at = models.DateTimeField(auto_now_add=True)
