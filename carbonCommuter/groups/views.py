"""
Authors:
-Charles Symonds
"""

from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from groups.models import GroupProfile


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
    group_profile = get_object_or_404(GroupProfile, group=group)
    context = {
        'group': group,
        'is_member': is_member,
        'members': members,
        'leader': group_profile.leader,
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
        # Create the group
        group = Group.objects.create(name=group_name)
        # Automatically add the creator to the group (optional)
        group.user_set.add(request.user)
        # Create GroupProfile with the current user as the leader
        GroupProfile.objects.create(group=group, leader=request.user)
        return redirect('user_groups_home_page')  # Adjust as needed


@login_required
def join_group(request, group_id):
    # Assuming the rest of your join logic is here
    group = get_object_or_404(Group, id=group_id)
    request.user.groups.add(group)
    # Use the name of the URL pattern for the group page
    return HttpResponseRedirect(reverse('group_page', args=[group_id]))


@login_required
def leave_group(request, group_id):
    if request.method == 'POST':
        group = get_object_or_404(Group, id=group_id)
        group.user_set.remove(request.user)
        # Redirect to a confirmation page, the group page, or elsewhere
        return HttpResponseRedirect(reverse('group_page', args=[group_id]))
