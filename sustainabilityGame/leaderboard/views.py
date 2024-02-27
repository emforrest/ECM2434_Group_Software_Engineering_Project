from django.shortcuts import render
from django.contrib.auth.models import User
from user.models import Profile
from .models import Leaderboard_Entry

# Render Leaderboard webpages here

from django.http import HttpResponse

    

def leaderboard(request):
    user1 = User()
    user1.name = "Sam"
    user1.totalCo2Saved = 10.6
    user1.position = 1

    user2 = User()
    user2.name = "Abi"
    user2.totalCo2Saved = 9.6
    user2.position = 2

    user3 = User()
    user3.name = "Charles"
    user3.totalCo2Saved = 8.6
    user3.position = 3

    user4 = User()
    user4.name = "Eleanor"
    user4.totalCo2Saved = 7.4
    user4.position = 4

    user5 = User()
    user5.name = "Giulia"
    user5.totalCo2Saved = 6.5
    user5.position = 5

    user6 = User()
    user6.name = "Jack"
    user6.totalCo2Saved = 5.2
    user6.position = 6

    user7 = User()
    user7.name = "Diego"
    user7.totalCo2Saved = 4.8
    user7.position = 7

    user8 = User()
    user8.name = "Solomon"
    user8.totalCo2Saved = 4.5
    user8.position = 8

    user9 = User()
    user9.name = "Matt"
    user9.totalCo2Saved = 4.3
    user9.position = 9

    user10 = User()
    user10.name = "John"
    user10.totalCo2Saved = 0.8
    user10.position = 19


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
