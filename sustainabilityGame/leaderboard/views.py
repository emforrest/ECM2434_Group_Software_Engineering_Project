from django.shortcuts import render
from .models import User

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


    users = [user1, user2, user3, user4, user5, user6]
    #return HttpResponse("This is the leaderboard page.")
    return render(request, "leaderboard/leaderboard.html", {'users':users})
