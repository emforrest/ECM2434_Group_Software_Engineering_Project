"""
Authors:
-Charles Symonds
"""

from django.contrib.auth.models import Group, User
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import GroupProfile, GroupJoinRequest
from django.contrib import messages


@login_required
def user_groups_home_page(request):
    """
    View for displaying the home page of user groups. It lists all the groups available
    in the system. Utilizes prefetch_related to optimize database queries when accessing
    related users.
    """
    groups = Group.objects.prefetch_related('user_set').all()
    context = {'groups': groups}
    return render(request, 'groups/user_groups_home_page.html', context)


@login_required
def group_page(request, group_id):
    """
    Displays the details of a specific group identified by `group_id`. It checks if
    the group has a designated leader and if not, the group is deleted. The view
    handles both members and non-members differently and provides functionalities
    accordingly.
    """
    group = get_object_or_404(Group, id=group_id)
    group_profile = GroupProfile.objects.filter(group=group).first()

    if group_profile is None or group_profile.leader is None:
        group.delete()
        return redirect('user_groups_home_page')

    is_member = request.user.groups.filter(id=group_id).exists()
    members = group.user_set.all()
    join_requests = GroupJoinRequest.objects.filter(group=group).all() if group_profile.is_private else None
    has_requested_join = GroupJoinRequest.objects.filter(group=group, user=request.user).exists()

    context = {
        'group': group,
        'group_profile': group_profile,
        'is_member': is_member,
        'members': members,
        'leader': group_profile.leader,
        'join_requests': join_requests,
        'has_requested_join': has_requested_join,
    }
    return render(request, 'groups/group_page.html', context)


@login_required
def search_groups(request):
    """
    Facilitates the search functionality for groups by a given query. It filters the groups
    by the name that includes the search query.
    """
    query = request.GET.get('q', '')
    if query:
        groups = Group.objects.filter(name__icontains=query)
    else:
        groups = Group.objects.none()
    return render(request, 'groups/search.html', {'groups': groups, 'query': query})


@login_required
def create_group(request):
    """
    Allows the creation of a new group with an option to mark it as private. The creator
    of the group automatically becomes a member and the leader of the newly created group.
    """
    if request.method == "POST":
        group_name = request.POST.get('group_name')
        is_private = request.POST.get('is_private', 'off') == 'on'
        group = Group.objects.create(name=group_name)
        group.user_set.add(request.user)
        GroupProfile.objects.create(group=group, leader=request.user, is_private=is_private)
        return redirect('user_groups_home_page')


def join_group(request, group_id):
    """
    Manages the joining process of a user to a group. Upon successful addition, redirects
    the user with a success message.
    """
    group = get_object_or_404(Group, id=group_id)
    request.user.groups.add(group)
    messages.success(request, "You have joined the group.")
    return redirect('group_page')


@login_required
def leave_group(request, group_id):
    """
    Facilitates a member's departure from a group. Ensures that this operation is done
    via POST request for security.
    """
    if request.method == 'POST':
        group = get_object_or_404(Group, id=group_id)
        group.user_set.remove(request.user)
        return HttpResponseRedirect(reverse('group_page', args=[group_id]))


@login_required
def delete_group(request, group_id):
    """
    Allows the deletion of a group by its leader. If the current user is not the leader,
    an error message or redirection can occur.
    """
    group = get_object_or_404(Group, id=group_id)
    group_profile = get_object_or_404(GroupProfile, group=group)
    if request.user == group_profile.leader:
        group.delete()
        return redirect('user_groups_home_page')
    else:
        return HttpResponseRedirect(reverse('group_page', args=[group_id]))


@login_required
def remove_member(request, group_id, user_id):
    """
    Enables a group leader to remove a member from the group. Checks are in place to
    ensure only the leader can perform this action.
    """
    group = get_object_or_404(Group, id=group_id)
    group_profile = get_object_or_404(GroupProfile, group=group)
    user_to_remove = get_object_or_404(User, id=user_id)

    if request.user == group_profile.leader:
        group.user_set.remove(user_to_remove)
        messages.success(request, "Member removed successfully.")
        return HttpResponseRedirect(reverse('group_page', args=[group_id]))
    else:
        messages.error(request, "You are not authorized to remove members.")
        return HttpResponseRedirect(reverse('group_page', args=[group_id]))


@login_required
def request_join_group(request, group_id):
    """
    Handles the functionality for a user to request to join a private group. If the group
    is public, the user is added immediately. For private groups, a join request is created.
    """
    group = get_object_or_404(Group, id=group_id)
    group_profile = get_object_or_404(GroupProfile, group=group)

    if request.user.groups.filter(id=group_id).exists():
        messages.error(request, "You are already a member of this group.")
        return redirect('group_page', group_id=group_id)

    if group_profile.is_private:
        existing_request = GroupJoinRequest.objects.filter(group=group, user=request.user).first()
        if not existing_request:
            GroupJoinRequest.objects.create(group=group, user=request.user)
            messages.success(request, "Join request sent.")
        else:
            messages.info(request, "You've already requested to join this group.")
    else:
        request.user.groups.add(group)
        messages.success(request, "You've joined the group.")

    return redirect('group_page', group_id=group_id)


@login_required
def handle_join_request(request, group_id, request_id, decision):
    """
    Manages the accept or reject actions on join requests for private groups by the group
    leader. A decision ('accept' or 'reject') is required.
    """
    group_profile = get_object_or_404(GroupProfile, group_id=group_id)
    if request.user != group_profile.leader:
        return HttpResponseForbidden("You are not authorized to manage join requests.")

    join_request = get_object_or_404(GroupJoinRequest, id=request_id, group=group_profile.group)
    if decision == 'accept':
        join_request.user.groups.add(group_profile.group)
        messages.success(request, "Join request accepted.")
        join_request.delete()
    elif decision == 'reject':
        messages.info(request, "Join request rejected.")
        join_request.delete()
    else:
        messages.error(request, "Invalid decision.")

    return redirect('group_page', group_id=group_id)


@login_required
def view_join_requests(request, group_id):
    """
    Displays a list of all join requests for a private group to the group leader, allowing
    them to manage these requests.
    """
    group = get_object_or_404(Group, id=group_id)
    group_profile = get_object_or_404(GroupProfile, group=group)

    if request.user != group_profile.leader:
        return HttpResponseForbidden("You are not authorized to view this page.")

    join_requests = GroupJoinRequest.objects.filter(group=group)
    context = {'group': group, 'join_requests': join_requests}
    return render(request, 'groups/view_join_requests.html', context)


@login_required
def accept_join_request(request, group_id, request_id):
    """
    Directly accepts a join request for a group, adding the requester to the group members.
    Ensures that only the group leader can perform this action.
    """
    join_request = get_object_or_404(GroupJoinRequest, id=request_id, group_id=group_id)
    group_profile = get_object_or_404(GroupProfile, group=join_request.group)

    if request.user != group_profile.leader:
        return HttpResponseForbidden("You are not authorized to perform this action.")

    join_request.user.groups.add(join_request.group)
    join_request.delete()
    messages.success(request, "Join request accepted.")
    return redirect('group_page', group_id=group_id)


@login_required
def reject_join_request(request, group_id, request_id):
    """
    Directly rejects a join request for a group. Ensures that only the group leader can
    perform this action.
    """
    join_request = get_object_or_404(GroupJoinRequest, id=request_id, group_id=group_id)
    group_profile = get_object_or_404(GroupProfile, group=join_request.group)

    if request.user != group_profile.leader:
        return HttpResponseForbidden("You are not authorized to perform this action.")

    join_request.delete()
    messages.info(request, "Join request rejected.")
    return redirect('group_page', group_id=group_id)
