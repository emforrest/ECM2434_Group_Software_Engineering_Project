from django.db import models
from django.contrib.auth.models import Group, User

class GroupProfile(models.Model):
    """
    GroupProfile extends the built-in Group model to add additional attributes specific to the application's needs.

    Attributes:
    - group: A OneToOneField linking to Django's built-in Group model. This allows for the extension of the Group model
      without modifying its core structure.
    - leader: A ForeignKey to the User model, identifying the leader of the group. The `related_name` 'led_groups'
      allows for easy access from the User model to find all groups a user leads.
    - is_private: A BooleanField indicating whether the group is private. Private groups may have different visibility
      and join request handling compared to public groups.
    """
    group = models.OneToOneField(Group, on_delete=models.CASCADE)
    leader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='led_groups')
    is_private = models.BooleanField(default=False)

    def __str__(self):
        """
        String representation of a GroupProfile, showing the group's name and its leader's username.
        """
        return f"{self.group.name} led by {self.leader.username}"

class GroupJoinRequest(models.Model):
    """
    GroupJoinRequest model handles join requests for private groups.

    Attributes:
    - group: A ForeignKey linking to the Group model. This indicates which group the join request is for.
    - user: A ForeignKey linking to the User model. This indicates which user has made the join request.
    - created_at: A DateTimeField that automatically sets the date and time when a join request is created,
      useful for tracking and managing requests over time.
    """
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='join_requests')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='join_requests')
    created_at = models.DateTimeField(auto_now_add=True)
