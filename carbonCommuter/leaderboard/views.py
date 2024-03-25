from django.shortcuts import render
from user.models import Profile
from user.models import Journey
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from .models import Leaderboard_Entry
from django.contrib.auth.decorators import login_required
from common.utils import leaderboardData
from datetime import datetime, timedelta, date
from django.db.models import Sum

# Render Leaderboard webpages here

from django.http import HttpResponse

from user.models import Badges, UserBadge
    
@login_required
def user_leaderboard(request):
    # Initialize empty lists and variables
    users_total = []
    users_weekly = []
    group_scores = []
    users_followers = []
    
    # Retrieve all users' total carbon savings from the database
    users_journeys = Journey.objects.values('user__first_name', 'user__last_name', 'user__username', 'user__id').annotate(total_carbon_saved=Sum('carbon_savings')).order_by("-user_id")
    users_total = leaderboardData(users_journeys)

    # Retrieve users' weekly carbon savings from the database
    now = date.now()
    this_monday = now - timedelta(days=now.weekday())
    weekly_journeys = Journey.objects.filter(time_finished__gt=this_monday).values('user__first_name', 'user__last_name', 'user__username', 'user__id').annotate(total_carbon_saved=Sum('carbon_savings')).order_by("-user_id")
    users_weekly = leaderboardData(weekly_journeys)

    # Retrieve all groups
    groups = Group.objects.all()
    for group in groups:
        # Initialize a group entry for each group
        group_entry = Leaderboard_Entry()
        group_entry.name = group.name
        group_entry.totalCo2Saved = 0
        group_entry.id = group.id
        group_entry.username = group.name
        group_scores.append(group_entry)
    
    # Calculate total carbon savings for each group
    for user_model in users_total:
        user_id = user_model.id
        user = User.objects.get(id=user_id)
        user_groups = user.groups.all()
        for user_group in user_groups:
            for group in group_scores:
                if user_group.id == group.id:
                    group.totalCo2Saved += user_model.totalCo2Saved
    
    # Sort groups by total carbon savings and limit to top 10
    group_scores.sort(key=lambda x: x.totalCo2Saved, reverse=True)
    group_scores = group_scores[:10]

    # Calculate positions for group scores
    for x in range(0,len(group_scores)):
        group_scores[x].position = x+1
        group_scores[x].totalCo2Saved = round(group_scores[x].totalCo2Saved,2)
    
    # Retrieve users that the current user is following
    following = request.user.following.all() 
    for user in following: 
        follower_entry = Leaderboard_Entry()
        follower_entry.name = user.followedUser.first_name + ' ' + user.followedUser.last_name
        follower_entry.id = user.followedUser.id
        follower_entry.username = user.followedUser.username
        follower_entry.totalCo2Saved = 0
        for follower in users_total:
            if follower.id == user.followedUser.id:
                follower_entry.totalCo2Saved=follower.totalCo2Saved
                break
        users_followers.append(follower_entry)

    # Sort users by total carbon savings and limit to top 10
    users_total.sort(key=lambda x: x.totalCo2Saved, reverse=True)
    users_total = users_total[:10]
    for x in range(0,len(users_total)):
        users_total[x].position = x+1

    # Logic for leaderboard badges
    badge = Badges.objects.get(name="topLeaderboard").id
    if not UserBadge.objects.filter(user_id=users_total[0].id, badge_id=badge).exists():
        newBadge = UserBadge(user_id=users_total[0].id, badge_id=badge)
        newBadge.save()

    # Sort weekly users by total carbon savings and limit to top 10
    users_weekly.sort(key=lambda x: x.totalCo2Saved, reverse=True)
    users_weekly = users_weekly[:10]
    for x in range(0,len(users_weekly)):
        users_weekly[x].position = x+1

    # Sort followers by total carbon savings and limit to top 10
    users_followers.sort(key=lambda x: x.totalCo2Saved, reverse=True)
    users_followers = users_followers[:10]
    for x in range(0,len(users_followers)):
        users_followers[x].position = x+1
    
    # Return leaderboard data to render the user leaderboard page
    return render(request, "leaderboard/user_leaderboard.html", {'users':users_total,
                                                            'weekly_users': users_weekly,
                                                            'groups': group_scores,
                                                            'followers':users_followers})


def leaderboard(request):
    # Similar logic as user_leaderboard function, but for the general leaderboard page
    # Retrieve users' total and weekly carbon savings
    users_total = []
    users_weekly = []
    group_scores = []
    users_journeys = Journey.objects.values('user__first_name', 'user__last_name', 'user__username', 'user__id').annotate(total_carbon_saved=Sum('carbon_savings')).order_by("-user_id")
    users_total = leaderboardData(users_journeys)

    now = date.now()
    this_monday = now - timedelta(days=now.weekday())
    weekly_journeys = Journey.objects.filter(time_finished__gt=this_monday).values('user__first_name', 'user__last_name', 'user__username', 'user__id').annotate(total_carbon_saved=Sum('carbon_savings')).order_by("-user_id")
    users_weekly = leaderboardData(weekly_journeys)

    # Retrieve groups and calculate group scores
    groups = Group.objects.all()
    for group in groups:
        group_entry = Leaderboard_Entry()
        group_entry.name = group.name
        group_entry.totalCo2Saved = 0
        group_entry.id = group.id
        group_entry.username = group.name
        group_scores.append(group_entry)
    
    for user_model in users_total:
        user_id = user_model.id
        user = User.objects.get(id=user_id)
        user_groups = user.groups.all()
        for user_group in user_groups:
            for group in group_scores:
                if user_group.id == group.id:
                    group.totalCo2Saved += user_model.totalCo2Saved
    group_scores.sort(key=lambda x: x.totalCo2Saved, reverse=True)
    group_scores = group_scores[:10]
    for x in range(0,len(group_scores)):
        group_scores[x].position = x+1
        group_scores[x].totalCo2Saved = round(group_scores[x].totalCo2Saved,2)
            
    # Sort users by total and weekly carbon savings and limit to top 10
    users_total.sort(key=lambda x: x.totalCo2Saved, reverse=True)
    users_total = users_total[:10]
    for x in range(0,len(users_total)):
        users_total[x].position = x+1

    users_weekly.sort(key=lambda x: x.totalCo2Saved, reverse=True)
    users_weekly = users_weekly[:10]
    for x in range(0,len(users_weekly)):
        users_weekly[x].position = x+1

    # Return leaderboard data to render the general leaderboard page
    return render(request, "leaderboard/leaderboard.html", {'users':users_total,
                                                            'weekly_users': users_weekly,
                                                            'groups': group_scores})



