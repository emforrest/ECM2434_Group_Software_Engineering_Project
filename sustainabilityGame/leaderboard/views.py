from django.shortcuts import render
from django.contrib.auth.models import User
from user.models import Profile
from .models import Leaderboard_Entry

# Render Leaderboard webpages here

from django.http import HttpResponse

    

def leaderboard(request):
    users = []
    users_profile = Profile.objects.all().order_by("-total_saving")[:5]
    x = 1
    for profile in users_profile:
        user_entry = Leaderboard_Entry()
        user = profile.user
        user_entry.name = user.first_name + " " + user.last_name
        user_entry.totalCo2Saved = profile.total_saving
        user_entry.position = x 
        x+= 1
        users.append(user_entry)


        
    


    #return HttpResponse("This is the leaderboard page.")
    return render(request, "leaderboard/leaderboard.html", {'users':users})
