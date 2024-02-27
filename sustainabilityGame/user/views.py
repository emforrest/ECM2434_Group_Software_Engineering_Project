"""Contains the functions related to endpoints with the /user/ prefix, including rendering the three webpages and handling a user's upload.
authors: Sam Townley, Eleanor Forrest
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import Profile

from common.utils import locationToDistance, getCampusCoords, distanceToCO2, convertTravelType


@login_required
def home(request):
    """
    Return the /user/home page with the information about the current user such as their name and email address.

    Parameters:
    request - the HTTP request containing information about the current user

    Return:
    The function returns the rendering of the home webpage using the provided information    
    """
    firstName = request.user.first_name
    lastName = request.user.last_name
    name = firstName + " " + lastName
    email = request.user.email
    username = request.user.username
    myDate = request.user.date_joined
    co2Saved = request.user.profile.total_saving
    context = context = {"name": name,
                         "email": email,
                         "username": username,
                         "myDate": myDate,
                         "co2Saved" : co2Saved}
                         "myDate": myDate}
    return render(request, "user/home.html", context)

@login_required
def settings(request):
    """
    Return the /user/settings page with the information about the current user such as their name and email address.

    Parameters:
    request - the HTTP request containing information about the current user

    Return:
    The function returns the rendering of the settings webpage using the provided information    
    """
    firstName = request.user.first_name
    lastName = request.user.last_name
    email = request.user.email
    username = request.user.username
    myDate = request.user.date_joined
    context = context = {"firstName": firstName,
                         "lastName" : lastName,
                         "email": email,
                         "username": username,
                         "myDate": myDate}
    return render(request, "user/settings.html", context)

@login_required
def upload(request):
    """
    Return the user/upload page with the current user's information, and process the information a user inputs into the HTML form

    Parameters:
    request - the HTTP request containing information about the current user

    Return:
    The function returns the rendering of the upload webpage using the provided information    
    """
    username = request.user.username
    context = context = {"username": username}

    #Deal with a POST request from the form
    if request.method == "POST":
        
        print(request.POST.get("oncampus"))
        print(request.POST.get("autocomplete"))
        print(request.POST.get("lat"))
        print(request.POST.get("lng"))
        print(request.POST.get("transport"))
        
        origin = getCampusCoords(request.POST.get('oncampus'))
        if origin == {}:
            raise RuntimeError("On-campus location not found!")
        
        transport = convertTravelType(request.POST.get('transport'))
        if transport is None:
            raise RuntimeError("Transport not found!")
        
        #Use the hidden form fields to access the off campus coordinates, then calculate the distance between these and the on-campus ones.
        distance = locationToDistance(origin['latitude'], origin['longitude'], float(request.POST.get('lat')), float(request.POST.get('lng')), transport)
        print(distance)
        
        #Calculate the amount of carbon dioxide saved
        savings = distanceToCO2(distance, transport)
        print(savings)
        
        #Add the result to the user's record
        request.user.profile.total_saving += savings
        request.user.profile.save()
        
    return render(request, "user/upload.html", context)
