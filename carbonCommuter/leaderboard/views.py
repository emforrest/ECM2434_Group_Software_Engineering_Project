from django.shortcuts import render
from user.models import Profile
from user.models import Journey
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from .models import Leaderboard_Entry
from django.contrib.auth.decorators import login_required
from common.utils import leaderboardData
from datetime import datetime, timedelta

# Render Leaderboard webpages here

from django.http import HttpResponse


    
@login_required
def user_leaderboard(request):
    users_total = []
    users_weekly = []
    users_group = []
    users_journeys = Journey.objects.all().order_by("-user_id")
    users_weekly_journeys = []
    users_group_journeys = []

    users_total = leaderboardData(users_journeys)
    for journey in users_journeys:
        now = datetime.now()
        this_monday = now - timedelta(days=now.weekday())
        journey_week_monday = journey.time_finished - timedelta(days=journey.time_finished.weekday())
        if (this_monday.date() == journey_week_monday.date()): 
            users_weekly.append(journey)
    print(users_weekly)

    groups = Group.objects.all().order_by("-group_id")
    for group in groups:
        group_entry = Leaderboard_Entry()
        group_entry.name = group.name
        group_entry.totalCo2Saved = 0
        for journey in users_journeys:
            for user_group in journey.user.groups:
                if user_group.id == group.id:
                    group_entry.totalCo2Saved += journey.carbon_savings
    group_entry.sort(key=lambda x: x.totalCo2Saved, reverse=True)
    group_entry = group_entry[:10]
    for x in range(0,len(group_entry)):
        group_entry[x].position = x+1

def leaderboard(request):
    users_total = []
    users_weekly = []
    group_scores = []
    users_journeys = Journey.objects.all().order_by("-user_id")
    users_total = leaderboardData(users_journeys)
    current_id = - 1
    for journey in users_journeys:
        if journey.user.id != current_id: 
            if current_id != -1:
                users_weekly.append(user_entry)
            user_entry = Leaderboard_Entry()
            current_id = journey.user_id
            user_entry.name = journey.user.first_name + " " + journey.user.last_name
            user_entry.totalCo2Saved = 0
            user_entry.id = current_id
        now = datetime.now()
        this_monday = now - timedelta(days=now.weekday())
        try:
            journey_week_monday = journey.time_finished - timedelta(days=journey.time_finished.weekday())
            if (this_monday.date() == journey_week_monday.date()): 
                user_entry.totalCo2Saved += journey.carbon_savings
        except: 
            #If journey is in progress, ignore it. 
            continue
    users_weekly.append(user_entry)

    groups = Group.objects.all()
    for group in groups:
        group_entry = Leaderboard_Entry()
        group_entry.name = group.name
        group_entry.totalCo2Saved = 0
        group_entry.id = group.id
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

    users_total.sort(key=lambda x: x.totalCo2Saved, reverse=True)
    users_total = users_total[:10]
    for x in range(0,len(users_total)):
        users_total[x].position = x+1

    users_weekly.sort(key=lambda x: x.totalCo2Saved, reverse=True)
    users_weekly = users_weekly[:10]
    for x in range(0,len(users_weekly)):
        users_weekly[x].position = x+1
    
    #return HttpResponse("This is the leaderboard page.")
    return render(request, "leaderboard/leaderboard.html", {'users':users_total,
                                                            'weekly_users': users_weekly,
                                                            'groups': group_scores})
