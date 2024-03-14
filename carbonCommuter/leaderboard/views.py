from django.shortcuts import render
from user.models import Profile
from user.models import Journey
from django.contrib.auth.models import Group
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
    users = []
    users_journeys = Journey.objects.all().order_by("-user_id")
    users = leaderboardData(users_journeys)
    
    #return HttpResponse("This is the leaderboard page.")
    return render(request, "leaderboard/leaderboard.html", {'users':users})
