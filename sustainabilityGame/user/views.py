from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Render user webpages here
from common.utils import locationToDistance, getCampusCoords, distanceToCO2
from common.travelTypes import TravelType


@login_required
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
    #return HttpResponse("This is the user settings page.")
    return render(request, "user/settings.html", context)

@login_required
def upload(request):
    username = request.user.username
    context = {"username": username}
    if request.method == "POST":
        
        # Get name of location on campus from form and map it to a latitude and longitude dict stored inside common/campusCoordinates.json
        origin = getCampusCoords(request.POST.get('oncampus'))
        if origin == {}:
            raise RuntimeError("On-campus location not found!")
        
        # Convert the string representation of the transport type to a TravelType object.
        transport = TravelType.from_str(request.POST.get('transport'))
        if transport is None:
            raise RuntimeError("Transport not found!")
        
        # Convert both sets of latitude/longitude coordinates to a distance, and then calculate the carbon saved based on that distance, using the method defined in common/utils.py
        distance = locationToDistance(origin['latitude'], origin['longitude'], float(request.POST.get('lat')), float(request.POST.get('lng')), transport)     
        savings = distanceToCO2(distance/1000, transport)
        print(savings)
        
        # Increment the total savings stored inside the users profile model by the additonal carbon savings
        request.user.profile.total_saving += savings
        request.user.profile.save()
        
    return render(request, "user/upload.html", context)
