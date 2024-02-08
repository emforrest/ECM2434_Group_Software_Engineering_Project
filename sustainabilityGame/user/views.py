from django.shortcuts import render

# Render user webpages here

from django.http import HttpResponse


def home(request):
    return HttpResponse("This is the user homepage.")

def settings(request):
    return HttpResponse("This is the user settings page.")

def upload(request):
    return HttpResponse("This is the user upload page.")
