from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile

# Render user webpages here
from common.utils import locationToDistance, getCampusCoords, distanceToCO2, convertTravelType


@login_required
def home(request):
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
    context = context = {"username": username}
    #return HttpResponse("This is the user upload page.")
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
        
        distance = locationToDistance(origin['latitude'], origin['longitude'], float(request.POST.get('lat')), float(request.POST.get('lng')), transport)
        print(distance)
        
        savings = distanceToCO2(distance, transport)
        print(savings)
        
        request.user.profile.total_saving += savings
        request.user.profile.save()
        
    return render(request, "user/upload.html", context)
