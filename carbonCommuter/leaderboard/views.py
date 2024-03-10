from django.shortcuts import render
from user.models import Profile
from user.models import Journey
from .models import Leaderboard_Entry

# Render Leaderboard webpages here

from django.http import HttpResponse

    

def leaderboard(request):
    users = []
    users_journeys = Journey.objects.all().order_by("-user_id")
    current_id = 1
    for journey in users_journeys:
        if journey.user_id != current_id: 
            user_entry = Leaderboard_Entry
            current_id = journey.user_id
            user = Profile.objects.get(user_id = current_id)
            user_entry.name = user.first_name + " " + user.last_name
        user_entry.totalCo2Saved += journey.carbon_savings
        users.append(user_entry)

    users.sort(key=lambda x: x.totalCo2Saved, reverse=True)
    users = users[:10]
        

        
    


    #return HttpResponse("This is the leaderboard page.")
    return render(request, "leaderboard/leaderboard.html", {'users':users})
