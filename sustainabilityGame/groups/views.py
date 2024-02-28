from venv import logger

from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    groups = Group.objects.prefetch_related('user_set').all()
    context = {'groups': groups}
    return render(request, 'groups/home.html', context)


@login_required
def create_group(request):
    if request.method == 'POST':
        group_name = request.POST.get('group_name')
        if Group.objects.filter(name=group_name).exists():
            messages.error(request, 'Group already exists.')
            return redirect('/groups/create/')  # Adjusted to use direct path

        new_group = Group.objects.create(name=group_name)
        request.user.groups.add(new_group)
        messages.success(request, 'Group created successfully.')
        return redirect('/')  # Adjust as necessary, assuming home page lists groups

    return render(request, 'groups/create.html')


@login_required
def join_group(request):
    if request.method == 'POST':
        group_id = request.POST.get('group_id')
        try:
            group = Group.objects.get(id=group_id)
            request.user.groups.add(group)
            messages.success(request, f'You have joined {group.name}.')
            return redirect('/groups/')  # Adjust as necessary
        except Group.DoesNotExist:
            messages.error(request, 'This group does not exist.')

    groups = Group.objects.all().exclude(user=request.user)
    return render(request, 'groups/join.html', {'groups': groups})


@login_required
def leave_group(request):
    if request.method == 'POST':
        group_id = request.POST.get('group_id')
        group = get_object_or_404(Group, id=group_id)

        # Check if the user is a member of the group
        if group in request.user.groups.all():
            request.user.groups.remove(group)
            messages.success(request, f'You have successfully left {group.name}.')
        else:
            messages.error(request, 'You are not a member of this group.')

        return redirect('/groups/')  # Use a direct path for redirect

    # GET request: Show the leave group page with list of user's groups
    user_groups = request.user.groups.all()
    return render(request, 'groups/leave.html', {'groups': user_groups})

