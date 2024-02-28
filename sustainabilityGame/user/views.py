
"""Contains the functions related to endpoints with the /user/ prefix, including rendering the three webpages and handling a user's upload.

Authors: 
- Sam Townley
- Eleanor Forrest
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from common.utils import locationToDistance, getCampusCoords, distanceToCO2
from common.travelTypes import TravelType


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
                         "co2Saved" : co2Saved,
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
    
        request.user.profile.total_saving += savings
        request.user.profile.save()

    return render(request, "user/upload.html", context)
