"""
Authors:
-Charles Symonds
"""

from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.decorators.http import require_POST


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
    group = get_object_or_404(Group, id=group_id)
    is_member = request.user.groups.filter(id=group_id).exists()
    context = {
        'group': group,
        'is_member': is_member,
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
def join_group(request, group_id):
    # Assuming the rest of your join logic is here
    group = get_object_or_404(Group, id=group_id)
    request.user.groups.add(group)
    # Use the name of the URL pattern for the group page
    return HttpResponseRedirect(reverse('group_page', args=[group_id]))
