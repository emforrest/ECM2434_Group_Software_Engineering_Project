
"""Contains the functions related to endpoints with the /user/ prefix, including rendering the three webpages and handling a user's upload.

Authors: 
- Sam Townley
- Eleanor Forrest
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from common.utils import locationToDistance, getCampusCoords, distanceToCO2
from common.travelTypes import TravelType
from user.models import Journey
from main.models import Location


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
    context = {"username": username}

    #Deal with a POST request from the form
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
        distance = locationToDistance(origin['latitude'], origin['longitude'], float(request.POST.get('lat')), float(request.POST.get('lng')), transport)     
        savings = distanceToCO2(distance/1000, transport)
        print(savings)
        
        # Create a new Location object if it doesn't yet exist.
        location, created = Location.objects.get_or_create(lat = float(request.POST.get('lat')),
                                                  lng = float(request.POST.get('lng')),
                                                  address = request.POST.get('autocomplete'),
                                                  postcode = request.POST.get('postcode'))
        if created:
            location.save()
        
        # Create a new entry in the journey's table
        journey = Journey(user = request.user,
                          distance = distance/1000,
                          origin = location, 
                          destination = request.POST.get('oncampus'),
                          transport = request.POST.get('transport'))
        journey.save()
        
        # Increment the total savings stored inside the users profile model by the additonal carbon savings
        request.user.profile.total_saving += savings
        request.user.profile.save()
        return redirect("success", journey_id=journey.id)
        
    return render(request, "user/upload.html", context)


@login_required
def upload_success(request, journey_id: int):
    print(journey_id)
    return render(request, "user/success.html")