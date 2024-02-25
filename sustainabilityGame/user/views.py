from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Render user webpages here

from django.http import HttpResponse

#@login_required
def home(request):
    firstName = request.user.first_name
    lastName = request.user.last_name
    name = firstName + " " + lastName
    email = request.user.email
    username = request.user.username
    myDate = request.user.date_joined
    context = context = {"name": name,
                         "email": email,
                         "username": username,
                         "myDate": myDate}
    #return HttpResponse("This is the user homepage.")
    return render(request, "user/home.html", context)

@login_required
def settings(request):
    #return HttpResponse("This is the user settings page.")
    return render(request, "user/settings.html")

@login_required
def upload(request):
    #return HttpResponse("This is the user upload page.")
    return render(request, "user/upload.html")
