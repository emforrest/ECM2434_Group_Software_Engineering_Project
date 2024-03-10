"""Contains the functions related to endpoints with the /user/ prefix, including rendering the three webpages and handling a user's upload.
Authors: 
- Sam Townley
- Eleanor Forrest
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from datetime import datetime

from common.travelTypes import TravelType
from user.models import Journey
from main.models import Location
from common.utils import locationToDistance, getCampusCoords, distanceToCO2

@login_required
def home(request):
    """Return the /user/home page with the information about the current user such as their name and email address.
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
    active_journey = False
    context = context = {"name": name,
                         "email": email,
                         "username": username,
                         "myDate": myDate,
                         "co2Saved": co2Saved,
                         "myDate": myDate,
                         "started": active_journey}
    return render(request, "user/home.html", context)


@login_required
def settings(request):
    """Return the /user/settings page with the information about the current user such as their name and email address.
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
            context["error"] = "This user already exists!"
            return render(request, "user/settings.html", context)

        #checking if email is already being used with a registered account
        userFilterEmail = User.objects.filter(email=email)
        if (userFilterEmail.exists() and (email != request.user.email)):
            context["error"] = "This email is already being used"
            return render(request, "user/settings.html", context)

        #checking if password is correct 
        user = authenticate(request, username=request.user.username, password=password1)
        if user is None:
            context = {"error": "Invalid password"}
            return render(request, "user/settings.html", context)

        request.user.first_name = first_name
        request.user.last_name = last_name
        request.user.email = email
        request.user.username = username
        request.user.save()
        co2Saved = request.user.profile.total_saving
        name = first_name + " " + last_name
        
        context = context = {"name": name,
                            "email": email,
                            "username": username,
                            "myDate": myDate,
                            "co2Saved": co2Saved,
                            "myDate": myDate}
        return render(request, "user/home.html", context)
    return render(request, "user/settings.html", context)  


@login_required
def create_journey(request):
    """
    The function returns the rendering of the upload webpage using the provided information    
    """
    username = request.user.username
    started = False
    context = context =  {"username": username}
    
    if started:
        return render(request, "user/start_journey.html", context)
    else:
        return render(request, "user/end_journey.html", context)
    
        # Get name of location on campus from form and map it to a latitude and longitude dict stored inside common/campusCoordinates.json
        #origin = getCampusCoords(request.POST.get('oncampus'))
        #if origin == {}:
        #    raise RuntimeError("On-campus location not found!")

        # Convert the string representation of the transport type to a TravelType object.
        #transport = TravelType.from_str(request.POST.get('transport'))
        #if transport is None:
        #   raise RuntimeError("Transport not found!")

        # Convert both sets of latitude/longitude coordinates to a distance, and then calculate the carbon saved based on that distance, using the methods defined in common/utils.py
        #distance = locationToDistance(origin['latitude'], origin['longitude'], float(request.POST.get('lat')),
        #                              float(request.POST.get('lng')), transport)
        #savings = distanceToCO2(distance / 1000, transport)
        #print(savings)
        
        # Create a new Location object if it doesn't yet exist.
        #try:
        #    location = Location.objects.get(address = request.POST.get('autocomplete'))
        #except Location.DoesNotExist:
        #    location = Location.objects.create(lat = request.POST.get('lat'),
        #                                       lng = request.POST.get('lng'),
        #                                       address = request.POST.get('autocomplete'))
        #    location.save()
        #except Exception as ex:
        #    raise ex
        
        # Create a new entry in the journey's table
        #journey = Journey(user = request.user,
        #                  distance = distance/1000,
        #                  origin = location, 
        #                  destination = request.POST.get('oncampus'),
        #                  transport = request.POST.get('transport'))
        #journey.save()
        
        # Increment the total savings stored inside the users profile model by the additonal carbon savings
        #request.user.profile.total_saving += savings
        #request.user.profile.save()
        #return redirect("success", journey_id=journey.id)


@login_required
def journey_created(request, journey_id: int):
    
    # Get journey object and calculate CO2 savings
    journey = Journey.objects.get(id=journey_id)
    savings = distanceToCO2(journey.distance, journey.transport)
    
    # Add journey information to context so it can be displayed on frontend
    context = {
        "distance": journey.distance,
        "co2_saved": savings,
        "transport": journey.transport
    }
    return render(request, "user/success.html", context)


@login_required
def start_journey(request):
    
    if request.method == "POST":
        print("Got start request")
        print(request.POST.get("address"))

        # Convert the string representation of the transport type to a TravelType object.
        transport = TravelType.from_str(request.POST.get('transport'))
        if transport is None:
           raise RuntimeError("Transport not found!")
        
        # Create a new Location object if it doesn't yet exist.
        #try:
        #    location = Location.objects.get(address = request.POST.get('address'))
        #except Location.DoesNotExist:
        #    location = Location.objects.create(lat = request.POST.get('lat'),
        #                                       lng = request.POST.get('lng'),
        #                                       address = request.POST.get('address'))
        #    location.save()
        #except Exception as ex:
        #    raise ex
        
        # Create a new entry in the journey's table
        #journey = Journey(user = request.user,
        #                  origin = location, 
        #                  transport = request.POST.get('transport'),
        #                  time_started = datetime.now())
        #journey.save()
        return redirect("dashboard")
    else:
        return render(request, "user/start_journey.html")
        

@login_required
def end_journey(request):
    
    if request.method == "POST":
        print("Got end request")
        return redirect("dashboard")
    else:
        return render(request, "user/end_journey.html")