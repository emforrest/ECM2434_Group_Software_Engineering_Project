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
    Display the home page with a list of all groups.

    This view retrieves all groups from the database, including prefetching
    related users to minimize database queries. It then renders the groups/user_groups_home_page.html
    template, passing the groups as context.

    :Parameters: HttpRequest object
    :return: HttpResponse object with rendered template
    """
    groups = Group.objects.prefetch_related('user_set').all()
    context = {'groups': groups}
    return render(request, 'groups/user_groups_home_page.html', context)


@login_required
def group_page(request, group_id):
    # Try to get the group and its profile
    group = get_object_or_404(Group, id=group_id)
    group_profile = GroupProfile.objects.filter(group=group).first()

    # Check if the group has a leader
    if group_profile is None or group_profile.leader is None:
        # If not, delete the group and redirect or show a message
        group.delete()
        # You can redirect to another page or show a custom message
        # For example, redirect to the list of groups
        return redirect('user_groups_home_page')  # Replace with the actual URL name for the groups list

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
        'join_requests': join_requests,  # Make sure to pass this to the template
        'has_requested_join': has_requested_join,
    }
    return render(request, 'groups/group_page.html', context)


@login_required
def search_groups(request):
    query = request.GET.get('q', '')
    if query:
        groups = Group.objects.filter(name__icontains=query)
    else:
        groups = Group.objects.none()
    return render(request, 'groups/search.html', {'groups': groups, 'query': query})


@login_required
def create_group(request):
    if request.method == "POST":
        group_name = request.POST.get('group_name')
        is_private = request.POST.get('is_private', 'off') == 'on'
        # Create the group
        group = Group.objects.create(name=group_name)
        # Automatically add the creator to the group (optional)
        group.user_set.add(request.user)
        # Create GroupProfile with the current user as the leader and set privacy
        GroupProfile.objects.create(group=group, leader=request.user, is_private=is_private)
        print("Group privacy status:", is_private)
        return redirect('user_groups_home_page')  # Adjust as needed


def join_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    # Your logic for adding a user to a group
    # For example:
    request.user.groups.add(group)
    messages.success(request, "You have joined the group.")
    return redirect('search_groups')  # Redirect to a relevant page


@login_required
def leave_group(request, group_id):
    if request.method == 'POST':
        group = get_object_or_404(Group, id=group_id)
        group.user_set.remove(request.user)
        # Redirect to a confirmation page, the group page, or elsewhere
        return HttpResponseRedirect(reverse('group_page', args=[group_id]))


@login_required
def delete_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    group_profile = get_object_or_404(GroupProfile, group=group)
    if request.user == group_profile.leader:
        group.delete()
        return redirect('user_groups_home_page')
    else:
        # Here you can return an error message or redirect as appropriate
        return HttpResponseRedirect(reverse('group_page', args=[group_id]))


@login_required
def remove_member(request, group_id, user_id):
    group = get_object_or_404(Group, id=group_id)
    group_profile = get_object_or_404(GroupProfile, group=group)
    user_to_remove = get_object_or_404(User, id=user_id)

    if request.user == group_profile.leader:
        group.user_set.remove(user_to_remove)
        # Redirect back to the group page or display a success message
        return HttpResponseRedirect(reverse('group_page', args=[group_id]))
    else:
        # Redirect or display an error if the user is not the leader
        return HttpResponseRedirect(reverse('group_page', args=[group_id]))


@login_required
def request_join_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    group_profile = get_object_or_404(GroupProfile, group=group)

    # Redirect user if they are already a member
    if request.user.groups.filter(id=group_id).exists():
        messages.error(request, "You are already a member of this group.")
        return redirect('group_page', group_id=group_id)

    if group_profile.is_private:
        # For private groups, create a join request
        existing_request = GroupJoinRequest.objects.filter(group=group, user=request.user).first()
        if not existing_request:
            GroupJoinRequest.objects.create(group=group, user=request.user)
            messages.success(request, "Join request sent.")
        else:
            messages.info(request, "You've already requested to join this group.")
    else:
        # For public groups, add the user directly
        request.user.groups.add(group)
        messages.success(request, "You've joined the group.")

    return redirect('group_page', group_id=group_id)


@login_required
def handle_join_request(request, group_id, request_id, decision):
    group_profile = get_object_or_404(GroupProfile, group_id=group_id)

    # Ensure the current user is the group leader
    if request.user != group_profile.leader:
        return HttpResponseForbidden()

    join_request = get_object_or_404(GroupJoinRequest, id=request_id, group=group_profile.group)

    if decision == 'accept':
        join_request.user.groups.add(group_profile.group)
        join_request.delete()  # Remove the request once handled
        message = "Request accepted."
    elif decision == 'reject':
        join_request.delete()
        message = "Request rejected."
    else:
        message = "Invalid decision."

    # Redirect back to the group page with a message
    return redirect('group_page', group_id=group_id)


@login_required
def view_join_requests(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    group_profile = get_object_or_404(GroupProfile, group=group)

    # Check if the current user is the leader
    if request.user != group_profile.leader:
        return HttpResponseForbidden("You are not authorized to view this page.")

    join_requests = GroupJoinRequest.objects.filter(group=group)

    context = {
        'group': group,
        'join_requests': join_requests,
    }

    return render(request, 'groups/view_join_requests.html', context)


@login_required
def accept_join_request(request, group_id, request_id):
    join_request = get_object_or_404(GroupJoinRequest, id=request_id, group_id=group_id)
    group_profile = get_object_or_404(GroupProfile, group=join_request.group)

    if request.user != group_profile.leader:
        return HttpResponseForbidden("You are not authorized to perform this action.")

    # Add the user to the group
    join_request.user.groups.add(join_request.group)
    # Delete the join request as it's been handled
    join_request.delete()
    # Optionally, show a success message
    messages.success(request, "Join request accepted.")

    # Redirect to the group page
    return redirect('group_page', group_id=group_id)


@login_required
def reject_join_request(request, group_id, request_id):
    join_request = get_object_or_404(GroupJoinRequest, id=request_id, group_id=group_id)
    group_profile = get_object_or_404(GroupProfile, group=join_request.group)

    if request.user != group_profile.leader:
        return HttpResponseForbidden("You are not authorized to perform this action.")

    # Delete the join request as it's been handled
    join_request.delete()
    # Optionally, show a success message
    messages.success(request, "Join request rejected.")

    # Redirect to the group page
    return redirect('group_page', group_id=group_id)


