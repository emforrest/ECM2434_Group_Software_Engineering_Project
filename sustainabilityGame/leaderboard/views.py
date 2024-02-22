from django.shortcuts import render

# Render Leaderboard webpages here

from django.http import HttpResponse

    

def leaderboard(request):
    user_names = ["Sam", "Jack", "Guilia", "Eleanor", "Charles", "Deigo", "Matt", "Solomon", "Achim"]
    user_co2saved = [15, 12, 11, 10 , 9, 8, 8, 8, 8, 5]
    #return HttpResponse("This is the leaderboard page.")
    return render(request, "leaderboard/leaderboard.html", {'user_names':user_names}, {"user_co2saved":user_co2saved})
