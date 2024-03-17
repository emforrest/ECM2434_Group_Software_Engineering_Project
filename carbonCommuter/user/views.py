
"""Contains the functions related to endpoints with the /user/ prefix, including rendering the three webpages and handling a user's upload.

Authors: 
- Sam Townley
- Eleanor Forrest
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse


import logging
from datetime import datetime

from user.models import Journey, Follower
from user.models import Journey
from user.models import Badges, UserBadge
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

    #setting values for opacity to show if user has the badges
    userBadge = UserBadge.get_badges(request.user)
    #userBadge = request.userBadge.get_badges()
    badgesList = []
    for badge in userBadge:
        badgeName = Badges.objects.get(id=badge.badge_id).name
        badgesList.append(badgeName)
        print(Badges.objects.get(id=badge.badge_id).name)
    #userBadges = userBadge.get_badges()
    amoryOpac = determine_opacity("Amory", badgesList)
    businessSchoolOpac = determine_opacity("Business School - Building One", badgesList)
    devonshireHouseOpac = determine_opacity("Devonshire House", badgesList)
    forumOpac = determine_opacity("Forum", badgesList)
    harrisonOpac = determine_opacity("Harrison", badgesList)
    innovationCentreOpac = determine_opacity("Innovation Centre", badgesList)
    laverOpac = determine_opacity("Laver", badgesList)
    lsiOpac = determine_opacity("Living Systems Institute", badgesList)
    peterChalkOpac = determine_opacity("Peter Chalk", badgesList)
    queensOpac = determine_opacity("Queens", badgesList)
    sportsParkOpac = determine_opacity("Sports Park", badgesList)
    swiotOpac = determine_opacity("South West Institute of Technology", badgesList)
    washingtonSinger = determine_opacity("Washington Singer", badgesList)
    '''sevenDaysOpac = determine_opacity(userBadges.sevenDays)
    fourteenDaysOpac = determine_opacity(userBadges.fourteenDays)
    thirtyDaysOpac = determine_opacity(userBadges.thirtyDays)
    fiftyDaysOpac = determine_opacity(userBadges.fiftyDays)
    seventyFiveDaysOpac = determine_opacity(userBadges.seventyFiveDays)
    hundredDaysOpac = determine_opacity(userBadges.hundredDays)'''


    context = context = {"full_name": name,
                         "co2Saved": co2Saved,
                         "started": started,
                         "sevenDaysOpac": 0.15,
                         "fourteenDaysOpac": 0.15,
                         "thirtyDaysOpac": 0.15,
                         "fiftyDaysOpac": 1,
                         "seventyFiveDaysOpac": 1,
                         "hundredDaysOpac": 1, 
                         "amoryOpac": amoryOpac, 
                         "businessSchoolOpac": businessSchoolOpac, 
                         "devonshireHouseOpac": devonshireHouseOpac, 
                         "forumOpac": forumOpac, 
                         "harrisonOpac": harrisonOpac, 
                         "innovationCentreOpac": innovationCentreOpac, 
                         "laverOpac": laverOpac, 
                         "lsiOpac": lsiOpac, 
                         "peterChalkOpac": peterChalkOpac,
                         "queensOpac": queensOpac,
                         "sportsParkOpac": sportsParkOpac,
                         "swiotOpac": swiotOpac,
                         "washingtonSinger": washingtonSinger}
    return render(request, "user/home.html", context)


def determine_opacity(badge, badgesList):
    if badge in badgesList:
        opacity = 1
    else:
        opacity = 0.15
    return opacity


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
            #set building to None as location not on campus
            building = None

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
        
        # add the location badge to the user if location on campus
        if (building != None):
            check_location(building, request.user)

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
            #set building to None as location not on campus
            building = None
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
        
        # add the location badge to the user if location on campus
        if (building != None):
            check_location(building, request.user)

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
        #Work out the context
        if request.user.username == username:
            isCurrentUser = True
        else:
            isCurrentUser = False
        if Follower.objects.filter(follower=request.user, followedUser=user).exists():
            followingUser = True
        else:
            followingUser = False

        context = {
            "username": username,
            "dateJoined" : user.date_joined,
            "co2Saved" : co2Saved,
            "isCurrentUser" : isCurrentUser,
            "followingUser" : followingUser,
            "userToFollow" : user,
        
        }
        return render(request, "user/profile.html", context)
    else:
        return HttpResponse(status=404)

def follow(request):
    """Handles the logic of following another user

    Args:
        request: The HTTP request object containing information about the request.

    Returns:
        HttpResponseRedirect: Refreshes the profile page the user is currently viewing
        HttpResponse: An unsuccessful request was made. The status code will indicate why.
    """
    if request.method == 'POST':
        data=request.POST
        action=data.get('follow')
        #Get the user that is being followed
        followedUser=User.objects.filter(username=data.get('followedUser'))[0]

        if action=="follow":
            #Create a Follow relationship
            follower=Follower.objects.create(follower=request.user, followedUser=followedUser)
            follower.save()
        elif action == "unfollow":
            #Remove a follow relationship
            follower=Follower.objects.get(follower=request.user, followedUser=followedUser)
            follower.delete()
        return HttpResponseRedirect(reverse('profile', kwargs={'username': followedUser}))
    else:
        return HttpResponse(status = 405)
    





    

def check_location(location, user):
    """Adding the location badge to the Badges table if the user has travelled to that location.

    Args:
        location: The location the user has logged, to add as a badge
        user: The user to be able to get the badges for that specific user
    """
    print("location = ", location)
    badgeLocation = False
    if location == "Amory":
        badgeLocation = True
    elif location == "Business School - Building One":
        badgeLocation = True
    elif location == "Devonshire House":
        badgeLocation = True
    elif location == "Forum":
        badgeLocation = True
    elif location == "Harrison":
        badgeLocation = True
    elif location == "Innovation Centre":
        badgeLocation = True
    elif location == "Laver":
        badgeLocation = True
    elif location == "Living Systems Institute":
        badgeLocation = True
    elif location == "Peter Chalk":
        badgeLocation = True
    elif location == "Queens":
        badgeLocation = True
    elif location == "Sports Park":
        badgeLocation = True
    elif location == "South West Institute of Technology":
        badgeLocation = True
    elif location == "Washington Singer":
        badgeLocation = True
    if badgeLocation:
        newBadge = UserBadge(user_id=user.id, badge_id=Badges.objects.get(name=location).id)
        newBadge.save()
    else:
        print("Invalid location")
    '''userBadges = Badges.objects.get(user=user)
    if location == "Amory":
        userBadges.amory = True
    elif location == "BusinessSchool":
        userBadges.businessSchool = True
    elif location == "DevonshireHouse":
        userBadges.devonshireHouse = True
    elif location == "Forum":
        userBadges.forum = True
    elif location == "Harrison":
        userBadges.harrison = True
    elif location == "InnovationCentre":
        userBadges.innovationCentre = True
    elif location == "Laver":
        userBadges.laver = True
    elif location == "LSI":
        userBadges.lsi = True
    elif location == "PeterChalk":
        userBadges.peterChalk = True
    elif location == "Queens":
        userBadges.queens = True
    elif location == "SportsPark":
        userBadges.sportsPark = True
    elif location == "Swiot":
        userBadges.swiot = True
    elif location == "WashingtonSinger":
        userBadges.washingtonSinger = True'''
