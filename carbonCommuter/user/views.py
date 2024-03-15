
"""Contains the functions related to endpoints with the /user/ prefix, including rendering the three webpages and handling a user's upload.

Authors: 
- Sam Townley
- Eleanor Forrest
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import HttpResponse

import logging
from datetime import datetime

from user.models import Journey
from main.models import Location
from common.travelTypes import TravelType
from common.utils import get_route, calculate_co2, get_distance_to_campus, format_time_between

LOGGER = logging.getLogger(__name__)

@login_required
def home(request):
    """Return the /user/home page with the information about the current user such as their name and email address.
    
    Args:
        request: The HTTP request containing information about the current user
    
    Returns:
        The function returns the rendering of the home webpage using the provided information    
    """
    # Set the information about the user in the context and render the template with this
    name = request.user.first_name + " " + request.user.last_name
    co2Saved = request.user.profile.get_total_savings()
    started = request.user.profile.has_active_journey()
    context = context = {"full_name": name,
                         "co2Saved": co2Saved,
                         "started": started}
    return render(request, "user/home.html", context)


@login_required
def settings(request):
    """Return the /user/settings page with the information about the current user such as their name and email address.
    
    Args:
        request: The HTTP request containing information about the current user
    
    Returns:
        The function returns the rendering of the settings webpage using the provided information    
    """
    if request.method == "POST":
        #accessing the data from the POST request
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        username = request.POST.get("username")
        password1 = request.POST.get("password1")

        #checking user does not already exist
        user = authenticate(request, username=username, password=password1)
        userFilter = User.objects.filter(username=username)
        if (userFilter.exists() and (username != request.user.username)):
            context = {"error": "This user already exists!"}
            return render(request, "user/settings.html", context)

        #checking if email is already being used with a registered account
        userFilterEmail = User.objects.filter(email=email)
        if (userFilterEmail.exists() and (email != request.user.email)):
            context = {"error": "This email is already being used"}
            return render(request, "user/settings.html", context)

        #checking if password is correct 
        user = authenticate(request, username=request.user.username, password=password1)
        if user is None:
            context = {"error": "Invalid password"}
            return render(request, "user/settings.html", context)

        # Update the information inside the user table
        request.user.first_name = first_name
        request.user.last_name = last_name
        request.user.email = email
        request.user.username = username
        request.user.save()
        return redirect("dashboard")
    return render(request, "user/settings.html")  


@login_required
def start_journey(request):
    """Handles the form page for starting a new journey within the system.

    Args:
        request: The HTTP request object containing information about the request.

    Raises:
        RuntimeError: An error occured whilst handling the form.
        Exception: An unknown error occured whilst getting the location from the address.

    Returns:
        HttpResponse: An unsuccessful request was made. The status code will indicate why.
        Redirect: The form was submitted correctly and the user was redirected to the dashboard upon completion.
        Render: A get request was recieved and the form was rendered.
    """
    # Check the user has an active journey, and if so, return an unauthorized error
    journey = request.user.profile.active_journey
    if journey is not None:
        return HttpResponse(status=403)
    
    # If method is POST, handle form submission
    if request.method == "POST":

        # Convert the string representation of the transport type to a TravelType object.
        transport = TravelType.from_str(request.POST.get('transport'))
        if transport is None:
            LOGGER.error("Transport not found!")
            raise RuntimeError("Transport not found!")
       
        # Check the POST request contains a valid latitude and longitude or address
        if request.POST.get('lat') in ["", None] or request.POST.get('long') in ["", None]:
           raise RuntimeError("Missing latitude and longitude!")
        elif request.POST.get('address') in ["", None]:
            raise RuntimeError("Missing address string!")

        # Get the closest building to campus and check if it's within an acceptable range (300m)
        building, distance = get_distance_to_campus(float(request.POST.get('lat')), float(request.POST.get('long')))
        if distance <= 0.3:
            location = Location.objects.get(name=building)
        else:
            
            # Get (or create) a Location object for the specified location if off campus
            try:
                location = Location.objects.get(address = request.POST.get('address'))
            except Location.DoesNotExist:
                location = Location.objects.create(lat = float(request.POST.get('lat')),
                                                   lng = float(request.POST.get('long')),
                                                   address = request.POST.get('address'))
                location.save()
            except Exception as ex:
                raise ex
        
        # Create a new entry in the journey's table
        journey = Journey(user = request.user,
                          origin = location, 
                          transport = str(transport),
                          time_started = datetime.now())
        journey.save()
        
        # Update the users active journey
        request.user.profile.active_journey = journey
        request.user.profile.save()
        return redirect("dashboard")
    
    # Render the form if visited by a GET request
    else:
        return render(request, "user/start_journey.html")
        

@login_required
def end_journey(request):
    """Handles the form page for ending a current journey within the system.

    Args:
        request: The HTTP request object containing information about the request.

    Raises:
        RuntimeError: An error occured whilst handling the form.
        Exception: An unknown error occured whilst getting the location from the address.

    Returns:
        HttpResponse: An unsuccessful request was made. The status code will indicate why.
        Redirect: The form was submitted correctly and the user was redirected to the success page upon completion.
        Render: A get request was recieved and the form was rendered.
    """
    # Check the user has an active journey, and if not, return an unauthorized error
    journey = request.user.profile.active_journey
    if journey is None:
        return HttpResponse(status=403)
    
    # If method is POST, handle form submission
    if request.method == "POST":
        
        # Get the closest building to campus and check if it's within an acceptable range (300m)
        building, distance = get_distance_to_campus(float(request.POST.get('lat')), float(request.POST.get('long')))
        if distance <= 0.3:
            location = Location.objects.get(name=building)
        else:
            
            # Get (or create) a Location object for the specified location if off campus
            try:
                location = Location.objects.get(address = request.POST.get('address'))
            except Location.DoesNotExist:
                location = Location.objects.create(lat = float(request.POST.get('lat')),
                                                   lng = float(request.POST.get('long')),
                                                   address = request.POST.get('address'))
                location.save()
            except Exception as ex:
                raise ex
            
        # Convert the string representation of the transport type to a TravelType object.
        transport = TravelType.from_str(journey.transport)
        if transport is None:
           raise RuntimeError("Transport not found!")
        
        # Convert both sets of latitude/longitude coordinates to a distance, and then calculate the carbon saved based on that distance, using the methods defined in common/utils.py
        distance, time = get_route(journey.origin.lat, journey.origin.lng, location.lat, location.lng, transport)
        savings = calculate_co2(distance, transport)
        
        # Save calculations and final timestamp to current journey
        journey.destination = location
        journey.distance = distance
        journey.estimated_time = time
        journey.carbon_savings = savings
        journey.time_finished = datetime.now()
        journey.save()
        
        # Reset user's active journey flag by setting active journey to none
        request.user.profile.active_journey = None
        request.user.profile.save()
        return redirect("journey", journey_id=journey.id)
    
    # Render the form if visited by a GET request
    else:
        return render(request, "user/end_journey.html")
    

@login_required
def journey_created(request, journey_id: int):
    """Displays information about a completed journey once it's been submitted successfully to the system.

    Args:
        request: The HTTP request object containing information about the request.
        journey_id: The ID of the journey being processed. 

    Raises:
        RuntimeError: An error occured whilst handling the form.
        Exception: An unknown error occured whilst getting the location from the address.

    Returns:
        HttpResponse: An unsuccessful request was made. The status code will indicate why.
        Render: Renders the html for the page with the context generated inside the function.
    """
    # Check the journey exists
    journey = Journey.objects.get(id=journey_id)
    if journey is None:
        return HttpResponse(status=404)
    
    # Add journey information to context so it can be displayed on frontend
    context = {
        "journey": journey,
        "transport": TravelType.from_str(journey.transport).to_str(),
        "time_taken": format_time_between(journey.time_finished, journey.time_started)
    }
    return render(request, "user/success.html", context)

@login_required
def profile(request, username:str):
    """Displays the public profile of the user passed in.

    Args:
        request: The HTTP request object containing information about the request.
        username: The username of the user whose profile should be accessed. 

    Returns:
        HttpResponse: An unsuccessful request was made. The status code will indicate why.
        Render: Renders the html for the page with the context generated inside the function.
    """

    #Check the user exists
    userFilter = User.objects.filter(username=username)
    if userFilter.exists():
        user = userFilter[0]
        co2Saved = user.profile.get_total_savings()
        if request.user.username == username:
            isCurrentUser = True
        else:
            isCurrentUser = False
        context = {
            "username": username,
            "dateJoined" : user.date_joined,
            "co2Saved" : co2Saved,
            "isCurrentUser" : isCurrentUser,
        
        }
        return render(request, "user/profile.html", context)
    else:
        return HttpResponse(status=404)


    