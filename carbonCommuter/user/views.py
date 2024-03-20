
"""Contains the functions related to endpoints with the /user/ prefix, including rendering the three webpages and handling a user's upload.

Authors: 
- Sam Townley
- Eleanor Forrest
- Abi Hinton
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.db.models import Sum

from common.utils import leaderboardWinner


import logging
from datetime import datetime, timedelta


from user.models import Journey, Follower
from user.models import Badges, UserBadge
from main.models import Location
from adminUser.models import Event
from common.travelTypes import TravelType
from common.utils import get_route, calculate_co2, get_distance_to_campus, format_time_between

LOGGER = logging.getLogger(__name__)

@login_required
def home(request):
    """Return the /user/home page with the information about the current user such as their 
    name and email address, and any badges they have earned.
    
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
    badgesList = []
    for badge in userBadge:
        #for every badge retrieved earlier, adding their name into list so can add the correct opacity
        badgeName = Badges.objects.get(id=badge.badge_id).name
        badgesList.append(badgeName)
    #determine opacity of all badges
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
    washingtonSingerOpac = determine_opacity("Washington Singer", badgesList)
    sevenDaysOpac = determine_opacity("7days", badgesList)
    fourteenDaysOpac = determine_opacity("14days", badgesList)
    thirtyDaysOpac = determine_opacity("30days", badgesList)
    fiftyDaysOpac = determine_opacity("50days", badgesList)
    seventyFiveDaysOpac = determine_opacity("75days", badgesList)
    hundredDaysOpac = determine_opacity("100days", badgesList)
    topLeaderboardOpac = determine_opacity("topLeaderboard", badgesList)
    weekLeaderboardOpac = determine_opacity("weekLeaderboard", badgesList)
    monthLeaderboardOpac = determine_opacity("monthLeaderboard", badgesList)

     #get a list of users this user is following
    followingUsers = User.objects.filter(followers__follower=request.user).values_list('username', flat=True)

    #get information about the current event
    eventBool = False
    eventMessage = ''
    eventProgress = -1
    eventTarget = -1
    eventComplete = False
    activeEventExists = Event.objects.filter(complete=False).exists()
    if activeEventExists:
        eventBool = True
        event = Event.objects.filter(complete=False).last()
        eventType = event.type
        eventProgress = event.progress
        eventTarget = event.target
        eventComplete = event.complete
        if not eventComplete:
            #Check if the event is now complete
            if eventProgress >= eventTarget or event.endDate < timezone.now().date():
                eventComplete = True
                event.complete = True
                event.save()
        if eventComplete:
            eventMessage = "Event complete! You did it!"
        else:
            if eventType == 1:
                eventMessage = f"Save {event.target} kilograms of CO2 by {event.endDate.strftime('%d-%m-%Y')}."
            elif eventType == 2:
                eventMessage = f"Log {event.target} total journeys by {event.endDate.strftime('%d-%m-%Y')}."
            elif eventType == 3:
                eventMessage = f"Visit {event.building}, {event.target} times by {event.endDate.strftime('%d-%m-%Y')}." 
            else:
                eventMessage = f"Visit every location on campus by {event.endDate.strftime('%d-%m-%Y')}."

    check_leaderboard()

    #adding opacity of badges to context so can be displayed correctly to the user
    context = context = {"full_name": name,
                         "co2Saved": co2Saved,
                         "started": started,
                         "sevenDaysOpac": sevenDaysOpac,
                         "fourteenDaysOpac": fourteenDaysOpac,
                         "thirtyDaysOpac": thirtyDaysOpac,
                         "fiftyDaysOpac": fiftyDaysOpac,
                         "seventyFiveDaysOpac": seventyFiveDaysOpac,
                         "hundredDaysOpac": hundredDaysOpac, 
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
                         "washingtonSingerOpac": washingtonSingerOpac,
                         "topLeaderboardOpac": topLeaderboardOpac,
                         "weekLeaderboardOpac": weekLeaderboardOpac,
                         "monthLeaderboardOpac": monthLeaderboardOpac, 
                         "followingUsers": followingUsers,
                         "eventMessage" : eventMessage,
                         "eventProgress" : eventProgress,
                         "eventTarget" : eventTarget,
                         "eventBool" : eventBool
                         }

    return render(request, "user/home.html", context)


def determine_opacity(badge, badgesList):
    """Returns the opacity integer for the badge, depending on whether the user has already earned the badge

    Args:
        badge: The name of the badge being checked
        badgesList: The list of badges the user has collected 
    Returns:
        opacity: the opacity of the badge depending on whether the user has collected it
    """
    if badge in badgesList:
        opacity = 1 #completely visible to user
    else:
        opacity = 0.15 #blurred to the user
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
    # Set any context required for rendering the template
    context = {
        "tab": 1,
        "locations": Location.objects.filter(on_campus=True)
    }
    
    # Check the user has an active journey, and if so, return an unauthorized error
    journey = request.user.profile.active_journey
    if journey is not None:
        LOGGER.warning(f"User [{request.user.username}:{request.user.id}]: Tried to access the start journey page with an active journey.")
        return redirect('end')
    
    # If method is POST, handle form submission
    if request.method == "POST":

        # Convert the string representation of the transport type to a TravelType object.
        transport = TravelType.from_str(request.POST.get('transport'))
        if transport is None:
            LOGGER.error(f"Transport method '{request.POST.get('transport')}' doesn't exist!")
            context["error"] = "Method of transport doesn't exist!"
            context["tab"] = 3
            context['lat'] = request.POST.get('lat')
            context['long'] = request.POST.get('long')
            context['address'] = request.POST.get('address')
            return render(request, "upload/start_journey.html", context=context)
       
        # Check the POST request contains a valid latitude and longitude or address
        if request.POST.get('lat') in ["", None] or request.POST.get('long') in ["", None] or request.POST.get('address') in ["", None]:
            LOGGER.warning(f"Missing location information on form submission!")
            context["error"] = "Please enter a valid location before trying to start your journey!"
            context["tab"] = 2
            return render(request, "upload/start_journey.html", context=context)

        # Get the closest building to campus
        try:
            building, distance = get_distance_to_campus(float(request.POST.get('lat')), float(request.POST.get('long')))
        except Exception as ex:
            LOGGER.error("Failed to get closest building to start location.")
            LOGGER.exception(ex)
            context["error"] = "Sorry, something went wrong with our calculations. Please try getting your location again!"
            context["tab"] = 2
            return render(request, "upload/start_journey.html", context=context)
        
        # Check if it's within an acceptable range (300m)
        if distance <= 0.3:
            location = Location.objects.get(name=building)
        else:
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
                LOGGER.error("Failed to get/create a new location object outside of campus.")
                LOGGER.exception(ex)
                context["error"] = "Sorry, something went wrong on our end! Please try getting your location again."
                context["tab"] = 2
                return render(request, "upload/start_journey.html", context=context)
        
        # Add the location badge to the user if location on campus
        if (building != None):
            check_location(building, request.user)

        # Create a new entry in the journey's table
        journey = Journey(user = request.user,
                          origin = location, 
                          transport = str(transport),
                          time_started = timezone.now())
        journey.save()
        
        # Update the users active journey
        request.user.profile.active_journey = journey
        request.user.profile.save()
        
        # Render success page
        context = {
            "CO2_Savings": round(abs(TravelType.CAR.value - transport.value), 2)
        }
        return render(request, "upload/started.html", context=context)
    
    # Render the form if visited by a GET request
    else:
        return render(request, "upload/start_journey.html", context=context)
        

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
    # Set any context required for rendering the template
    context = {
        "tab": 1,
        "locations": Location.objects.filter(on_campus=True)
    }
    
    # Check the user has an active journey, and if not, return an unauthorized error
    journey = request.user.profile.active_journey
    if journey is None:
        LOGGER.warning(f"User [{request.user.username}:{request.user.id}]: Tried to access the end journey page without an active journey.")
        return redirect('start')
    
    # If method is POST, handle form submission
    if request.method == "POST":
        
        # Check the POST request contains a valid latitude and longitude or address
        if request.POST.get('lat') in ["", None] or request.POST.get('long') in ["", None] or request.POST.get('address') in ["", None]:
            LOGGER.warning(f"Missing location information on form submission!")
            context["error"] = "Please enter a valid location before trying to end your journey!"
            context["tab"] = 2
            return render(request, "upload/end_journey.html", context=context)
        
        # Get the closest building to campus
        try:
            building, distance = get_distance_to_campus(float(request.POST.get('lat')), float(request.POST.get('long')))
        except Exception as ex:
            LOGGER.error("Failed to get closest building to end location.")
            LOGGER.exception(ex)
            context["error"] = "Sorry, something went wrong with our calculations. Please try getting your location again!"
            context["tab"] = 2
            return render(request, "upload/end_journey.html", context=context)
        
        # Get (or create) a Location object for the specified location if off campus
        if distance <= 0.3:
            location = Location.objects.get(name=building)
        else:
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
                LOGGER.error("Failed to get/create a new location object outside of campus.")
                LOGGER.exception(ex)
                context["error"] = "Sorry, something went wrong on our end! Please try getting your location again."
                context["tab"] = 2
                return render(request, "upload/end_journey.html", context=context)
        
        # add the location badge to the user if location on campus
        if (building != None):
            check_location(building, request.user)

        # Convert the string representation of the transport type to a TravelType object.
        transport = TravelType.from_str(journey.transport)
        if transport is None:
           LOGGER.critical("Uncaught exception: Transport type is not found during end journey function!")
           return HttpResponse(code=500)
        
        # Convert both sets of latitude/longitude coordinates to a distance, and then calculate the carbon saved based on that distance, using the methods defined in common/utils.py
        try:
            distance, time = get_route(journey.origin.lat, journey.origin.lng, location.lat, location.lng, transport)
            savings = calculate_co2(distance, transport)
        except Exception as ex:
            LOGGER.error("Failed to calculate route and carbon savings.")
            LOGGER.exception(ex)
            context["error"] = "Sorry, something went wrong with our calculations. Please try getting your location again!"
            context["tab"] = 2
            return render(request, "upload/end_journey.html", context=context)
        
        # Save calculations and final timestamp to current journey
        journey.destination = location
        journey.distance = distance
        journey.estimated_time = time
        journey.carbon_savings = savings
        journey.time_finished = timezone.now()
        journey.save()
        check_validity(journey)

        # Add to streak of the user
        pastJourneys = Journey.objects.all().filter(user_id=request.user.id) #accessing all the past journeys the user has made
        dateNow = timezone.now()
        checkStreak = False #boolean to check if a streak still exists
        for pastJourney in reversed(pastJourneys):
            #looping through past journeys in reverse so the most recent is first
            pastJourneyDate = pastJourney.time_finished
            difference = dateNow-pastJourneyDate
            if difference.seconds/60 > 1440:
                #if the difference between the last journey is more than 1440 minutes (24 hours), there is no streak
                break
            if (dateNow.weekday() - pastJourneyDate.weekday()) == 1:
                #checking there is a days difference between journeys
                checkStreak = True
                request.user.profile.streak = request.user.profile.streak + 1 
                break
        if not checkStreak:
            #if streak has been broken, set back to 0
            request.user.profile.streak = 0

        #check if user has earned any streak badges
        check_streak(request.user)

        #Add progres to the current event if there is one
        activeEventExists = Event.objects.filter(complete=False).exists()
        if activeEventExists:
            event = Event.objects.filter(complete=False)[0]
            eventType = event.type
            if eventType == 1:
                #target amount of CO2 saved
                event.progress += savings

            elif eventType == 2:
                #total number of journeys
                event.progress += 1

            elif eventType == 3:
                #visit one building a number of times
                campusBuilding1 = 'none'
                campusBuilding2 = 'none'
                if journey.origin.on_campus:
                    campusBuilding1 = journey.origin.name
                if journey.destination.on_campus:
                    campusBuilding2 = journey.destination.name

                if event.building == campusBuilding1 or event.building == campusBuilding2:
                    event.progress +=1
            
            elif eventType == 4:
                #visit every building once
                progressCount = 0
                startDate = event.startDate
                locationIDs = Location.objects.filter(on_campus = True).values_list('id', flat=True)
                recentJourneys = Journey.objects.filter(time_started__gt = startDate)
                for id in locationIDs:
                    for j in recentJourneys:
                        if j.origin_id == id or j.destination_id == id:
                            progressCount += 1
                            break
                print(progressCount)
                event.progress = progressCount
            event.save()
                        
        # Reset user's active journey flag by setting active journey to none
        request.user.profile.active_journey = None
        request.user.profile.save()
        
        # Render success page
        context = {
            "journey": journey,
            "transport": TravelType.from_str(journey.transport).to_str(),
            "time_taken": format_time_between(journey.time_finished, journey.time_started)
        }
        return render(request, "upload/finished.html", context=context)
    
    # Render the form if visited by a GET request
    else:
        return render(request, "upload/end_journey.html", context=context)
    

@login_required
def journey(request, journey_id: int):
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
    
    # Check if the user has admin or is the user that created the journey
    if (journey.user.id != request.user.id) and (request.user.profile.gamemaster != True):
        return HttpResponse(status=403)
    
    # Calculate which number of the user's journeys it is
    journeys = list(Journey.objects.filter(user=journey.user).values_list('id', flat=True))
    journey_no = journeys.index(journey.id) + 1
    
    # Add journey information to context so it can be displayed on frontend
    context = {
        "journey": journey,
        "transport": TravelType.from_str(journey.transport).to_str(),
        "time_taken": format_time_between(journey.time_finished, journey.time_started),
        "journey_no": journey_no
    }
    return render(request, "user/journey.html", context)


@login_required
def delete_journey(request):
    
    # Get id of journey to delete
    if request.method == "POST":
        id = request.POST.get('id')
    else:
        id = request.GET.get('id')
    
    # Check the journey exists
    journey = Journey.objects.get(id=id)
    if journey is None:
        return HttpResponse(status=404)

    # Check if the user is authorized to delete the journey or is an admin
    if (journey.user != request.user) and (request.user.profile.gamemaster != True):
        return HttpResponse(status=403)
    
    if request.method == "POST":
        # Delete active journey if the user has one
        if (request.user.profile.active_journey is not None) and (journey.id == request.user.profile.active_journey.id):
            request.user.profile.active_journey = None
            request.user.profile.save()
            
        # Delete the journey and redirect to the user home page
        journey.delete()
        return redirect("dashboard")
    
    # Render template based on if the journey is being cancelled or not
    else:
        if (request.user.profile.active_journey is not None) and (journey.id == request.user.profile.active_journey.id):
            return render(request, "upload/cancel.html", context={"id": journey.id})
        else:
            return render(request, "upload/delete.html", context={"id": journey.id})


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
        users_journeys =Journey.objects.filter(id = request.user.id).values('user__id').annotate(total_carbon_saved=Sum('carbon_savings'))
        co2Saved = users_journeys[0]['total_carbon_saved']
        co2Saved = round(co2Saved, 2)
        #Work out the context
        if request.user.username == username:
            isCurrentUser = True
        else:
            isCurrentUser = False
        if Follower.objects.filter(follower=request.user, followedUser=user).exists():
            followingUser = True
        else:
            followingUser = False
        #work out badges for user
        userBadge = UserBadge.get_badges(request.user)
        badgesList = []
        for badge in userBadge:
            #for every badge retrieved earlier, adding their name into list
            badgeName = Badges.objects.get(id=badge.badge_id).name
            badgesList.append(badgeName)
        badgeImages = []
        for badge in badgesList:
            #adding image strings for each badge
            badgeImage = getBadgeImage(badge)
            if not badgeImage == None:
                badgeImages.append(badgeImage)
        context = {
            "username": username,
            "dateJoined" : user.date_joined,
            "co2Saved" : co2Saved,
            "isCurrentUser" : isCurrentUser,
            "followingUser" : followingUser,
            "userToFollow" : user,
            "badgeImages" : badgeImages
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
        #if badgeLocation is valid, then will add the badge to the users collection
        badgeID = Badges.objects.get(name=location).id
        add_badge(badgeID, user)
    else:
        print("Invalid location")


def check_streak(user):
    """Adding the streak badge to the Badges table if the user has achieved a new high streak.
    
    Args: 
        user: The user to be able to get the badges for that specific user
    """
    streak = user.profile.streak
    badgeID = None
    if streak == 7:
        badgeID = Badges.objects.get(name="7days").id
    elif streak == 14:
        badgeID = Badges.objects.get(name="14days").id
    elif streak == 30:
        badgeID = Badges.objects.get(name="30days").id
    elif streak == 50:
        badgeID = Badges.objects.get(name="50days").id
    elif streak == 75:
        badgeID = Badges.objects.get(name="75days").id
    elif streak == 100:
        badgeID = Badges.objects.get(name="100days").id
    if badgeID != None:
        #if the user has achieved a streak listed, will add the badge
        add_badge(badgeID, user)

def check_leaderboard():
    today = datetime.now().astimezone()
    startWeekDate = (today + timedelta(days=-today.weekday(), weeks=-1)).replace(hour=0, minute=0, second=0, microsecond=0)
    endWeekDate = (startWeekDate + timedelta(6)).replace(hour=0, minute=0, second=0, microsecond=0)
    endMonthDate = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)
    startMonthDate = today.replace(day=1, month=endMonthDate.month, hour=0, minute=0, second=0, microsecond=0) 
    print("start week date: ", startWeekDate)
    print("end week date: ", endWeekDate)
    print("start month date: ", startMonthDate)
    print("end month date: ", endMonthDate)
    lastWeekJourneys = Journey.objects.filter(time_finished__gte=startWeekDate, time_finished__lte=endWeekDate).values('user__id').annotate(total_carbon_saved=Sum('carbon_savings')).order_by("-user_id")
    lastMonthJourneys = Journey.objects.filter(time_finished__gte=startMonthDate, time_finished__lte=endMonthDate).values('user__id').annotate(total_carbon_saved=Sum('carbon_savings')).order_by("-user_id")
    weeklyWinner = leaderboardWinner(lastWeekJourneys)
    monthlyWinner = leaderboardWinner(lastMonthJourneys)
    print("weekly Winner: ", weeklyWinner[0])
    print("monthly winner: ", monthlyWinner[0])
    add_badge(Badges.objects.get(name="weekLeaderboard").id, weeklyWinner[0])
    add_badge(Badges.objects.get(name="monthLeaderboard").id, monthlyWinner[0])

def add_badge(badge, user):
    """Adding the corresponding badge to the database

    Args:
        badge: The badge to be added to the database
        user: The user to be able to get the badges for that specific user
    """
    if not UserBadge.objects.filter(user_id=user.id, badge_id=badge).exists():
        #if the badge does not already exist for the user
        newBadge = UserBadge(user_id=user.id, badge_id=badge)
        newBadge.save()
            
            
def check_validity(journey):
    # Initalise variables for validation checks
    flagged = False
    reason = ""
    
    # Check that the distance is valid based on the mode of transport
    if journey.distance >= 40 and journey.transport == "train":
        flagged = True
        reason += "Distance by train is too long! "
    elif journey.distance >= 20 and journey.transport == "bus":
        flagged = True
        reason += "Distance by bus is too long! "
    elif journey.distance >= 10 and journey.transport == "bike":
        flagged = True
        reason += "Distance cycled is too long! "
    elif journey.distance >= 5 and journey.transport == "walk":
        flagged = True
        reason += "Distance walked is too long! "
    
    # Save changes to the journey if it's been flagged for review
    if flagged:
        journey.flagged = True
        journey.reason = reason
        journey.save()


@login_required
def journeys(request):
    user_journeys = Journey.objects.filter(user=request.user).order_by('-time_started')
    context = {'user_journeys': user_journeys}

    # Fetch the user's journeys, ordered by the start time
    user_journeys = Journey.objects.filter(user=request.user).order_by('-time_started')

    # Format journeys for the template
    formatted_journeys = []
    for journey in user_journeys:
        formatted_journeys.append({
            'id': journey.id,
            'start_time': journey.format_time_started(),
            'end_time': journey.format_time_finished() if journey.time_finished else 'In Progress',
            'distance': journey.distance,
            'carbon_savings': journey.carbon_savings,
            'origin': journey.origin.address if journey.origin else 'Unknown',
            'destination': journey.destination.address if journey.destination else 'Unknown',
            'transport': journey.transport,
        })

    # Add the journeys to the context
    context['user_journeys'] = formatted_journeys
    return render(request, 'user/journeys.html', context)

  
def getBadgeImage(badgeName):
    if badgeName == "Amory":
        return "/media/badges/locations/amory.png"
    elif badgeName == "Business School - Building One":
        return "/media/badges/locations/business.png"
    elif badgeName == "Devonshire House":
        return "/media/badges/locations/DH.png"
    elif badgeName == "Forum":
        return "/media/badges/locations/forum.png"
    elif badgeName == "Harrison":
        return "/media/badges/locations/harrison.png"
    elif badgeName == "Innovation Centre":
        return "/media/badges/locations/innovationCentre.png"
    elif badgeName == "Laver":
        return "/media/badges/locations/laver.png"
    elif badgeName == "Living Systems Institute":
        return "/media/badges/locations/LSI.png"
    elif badgeName == "Peter Chalk":
        return "/media/badges/locations/peterChalk.png"
    elif badgeName == "Queens":
        return "/media/badges/locations/queens.png"
    elif badgeName == "Sports Park":
        return "/media/badges/locations/sportsPark.png"
    elif badgeName == "South West Institute of Technology":
        return "/media/badges/locations/swiot.png"
    elif badgeName == "Washington Singer":
        return "/media/badges/locations/washingtonSinger.png"
    elif badgeName == "7days":
        return "/media/badges/streaks/7days.png"
    elif badgeName == "14days":
        return "/media/badges/streaks/14days.png"
    elif badgeName == "30days":
        return "/media/badges/streaks/30days.png"
    elif badgeName == "50days":
        return "/media/badges/streaks/50days.png"
    elif badgeName == "75days":
        return "/media/badges/streaks/75days.png"
    elif badgeName == "100days":
        return "/media/badges/streaks/100days.png"
    elif badgeName == "topLeaderboard":
        return "/media/badges/leaderboard/overall.png"
    elif badgeName == "weekLeaderboard":
        return "/media/badges/leaderboard/weekly.png"
    elif badgeName == "monthLeaderboard":
        return "/media/badges/leaderboard/monthly.png"
    else:
        return None

