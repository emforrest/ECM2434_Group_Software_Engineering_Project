from django.shortcuts import render

# Render user webpages here

from django.http import HttpResponse


def home(request):
    #return HttpResponse("This is the user homepage.")
    return render(request, "user/home.html")

def settings(request):
    #return HttpResponse("This is the user settings page.")
    return render(request, "user/settings.html")

def upload(request):
    #return HttpResponse("This is the user upload page.")
    return render(request, "user/upload.html")
