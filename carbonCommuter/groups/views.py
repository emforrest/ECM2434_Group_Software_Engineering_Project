"""
Authors:
-Charles Symonds
"""

from django.contrib.auth.models import Group
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    """
    Display the home page with a list of all groups.

    This view retrieves all groups from the database, including prefetching
    related users to minimize database queries. It then renders the groups/home.html
    template, passing the groups as context.

    :Parameters: HttpRequest object
    :return: HttpResponse object with rendered template
    """
    groups = Group.objects.prefetch_related('user_set').all()
    context = {'groups': groups}
    return render(request, 'groups/home.html', context)


@login_required
def create_group(request):
    """
    Create a new group.

    This view handles both GET and POST requests. For GET requests, it simply renders
    the group creation form. For POST requests, it attempts to create a new group
    with the given name, ensuring that the group name doesn't already exist. If the
    creation is successful, the user is redirected to the groups listing page.

    :Parameters: HttpRequest object
    :return: HttpResponse object with rendered template or redirection
    """
    context = {}
    if request.method == 'POST':
        group_name = request.POST.get('group_name')
        if Group.objects.filter(name=group_name).exists():
            context['error'] = 'Group already exists.'
            return render(request, 'groups/create.html', context)

        new_group = Group.objects.create(name=group_name)
        request.user.groups.add(new_group)
        return redirect('/groups/')

    return render(request, 'groups/create.html', context)


@login_required
def join_group(request):
    """
    Join an existing group.

    On GET request, displays a list of groups excluding those the user is already a member of.
    On POST request, attempts to add the user to the selected group. If the group doesn't exist,
    it adds an error message to the context and re-renders the join form.

    :Parameters: HttpRequest object
    :return: HttpResponse object with rendered template or redirection
    """
    context = {'groups': Group.objects.all().exclude(user=request.user)}
    if request.method == 'POST':
        group_id = request.POST.get('group_id')
        try:
            group = Group.objects.get(id=group_id)
            request.user.groups.add(group)
            return redirect('/groups/')
        except Group.DoesNotExist:
            context['error'] = 'This group does not exist.'

    return render(request, 'groups/join.html', context)


@login_required
def leave_group(request):
    """
    Leave a group that the user is currently a member of.

    This view handles the POST request when a user wants to leave a group. It checks if the user
    is actually a member of the group and removes the user from the group if true. Otherwise, it
    returns an error message. After successfully leaving a group, the user is redirected to the
    groups listing page.

    :Parameters: HttpRequest object
    :return: HttpResponse object with rendered template or redirection
    """
    context = {'groups': request.user.groups.all()}
    if request.method == 'POST':
        group_id = request.POST.get('group_id')
        group = get_object_or_404(Group, id=group_id)

        if group in request.user.groups.all():
            request.user.groups.remove(group)
            context['message'] = f'You have successfully left {group.name}.'
            return redirect('/groups/')
        else:
            context['error'] = 'You are not a member of this group.'

    return render(request, 'groups/leave.html', context)
