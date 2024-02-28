"""Contains the functions related to endpoints with the /user/ prefix, including rendering the three webpages and handling a user's upload.
Authors: 
- Sam Townley
- Eleanor Forrest
"""

from common.travelTypes import TravelType
from common.utils import locationToDistance, getCampusCoords, distanceToCO2
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


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
                         "co2Saved": co2Saved,
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
                         "lastName": lastName,
                         "email": email,
                         "username": username,
                         "myDate": myDate}
    return render(request, "user/settings.html", context)


@login_required
def upload(request):
    """
@@ -74,28 +52,8 @@ def upload(request):
    The function returns the rendering of the upload webpage using the provided information    
    """
    username = request.user.username
    context = {"username": username}

    # Deal with a POST request from the form
    if request.method == "POST":

        # Get name of location on campus from form and map it to a latitude and longitude dict stored inside common/campusCoordinates.json
        origin = getCampusCoords(request.POST.get('oncampus'))
        if origin == {}:
            raise RuntimeError("On-campus location not found!")

        # Convert the string representation of the transport type to a TravelType object.
        transport = TravelType.from_str(request.POST.get('transport'))
        if transport is None:
            raise RuntimeError("Transport not found!")

        # Convert both sets of latitude/longitude coordinates to a distance, and then calculate the carbon saved based on that distance, using the methods defined in common/utils.py
        distance = locationToDistance(origin['latitude'], origin['longitude'], float(request.POST.get('lat')),
                                      float(request.POST.get('lng')), transport)
        savings = distanceToCO2(distance / 1000, transport)
        print(savings)

        # Increment the total savings stored inside the users profile model by the additonal carbon savings

        request.user.profile.total_saving += savings
        request.user.profile.save()

    return render(request, "user/upload.html", context)