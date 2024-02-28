from django.contrib.auth.models import Group
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    groups = Group.objects.prefetch_related('user_set').all()
    context = {'groups': groups}
    return render(request, 'groups/home.html', context)


@login_required
def create_group(request):
    context = {}  # Initialize context dictionary
    if request.method == 'POST':
        group_name = request.POST.get('group_name')
        if Group.objects.filter(name=group_name).exists():
            context['error'] = 'Group already exists.'  # Add error to context instead of using messages
            return render(request, 'groups/create.html', context)  # Pass context to render

        new_group = Group.objects.create(name=group_name)
        request.user.groups.add(new_group)
        return redirect('/groups/')  # Assuming successful creation redirects to groups listing

    return render(request, 'groups/create.html', context)  # Ensure context is passed for GET requests


@login_required
def join_group(request):
    context = {'groups': Group.objects.all().exclude(user=request.user)}  # Initialize context with groups
    if request.method == 'POST':
        group_id = request.POST.get('group_id')
        try:
            group = Group.objects.get(id=group_id)
            request.user.groups.add(group)
            return redirect('/groups/')  # Redirect after successful addition
        except Group.DoesNotExist:
            context['error'] = 'This group does not exist.'  # Add error message to context

    return render(request, 'groups/join.html', context)


@login_required
def leave_group(request):
    context = {'groups': request.user.groups.all()}  # Initialize context with user's groups
    if request.method == 'POST':
        group_id = request.POST.get('group_id')
        group = get_object_or_404(Group, id=group_id)

        # Check if the user is a member of the group
        if group in request.user.groups.all():
            request.user.groups.remove(group)
            context['message'] = f'You have successfully left {group.name}.'  # Success message
            return redirect('/groups/')  # Use a direct path for redirect with message
        else:
            context['error'] = 'You are not a member of this group.'  # Error message

    return render(request, 'groups/leave.html', context)


