from django.shortcuts import render
#Render Main frontend templates here
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. This is main.")