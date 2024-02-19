from django.shortcuts import render

# Render Leaderboard webpages here

from django.http import HttpResponse


def leaderboard(request):
    return HttpResponse("This is the leaderboard page.")