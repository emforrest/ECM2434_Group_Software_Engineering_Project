"""Contains the function to render the admin webpage.
Authors: 
- Abi Hinton
- Eleanor Forrest
- Sam Townley
"""

from django.shortcuts import render
from main.models import Location
from django.http import HttpResponse
from adminUser.models import Event
from datetime import datetime

from user.models import Journey
from django.utils import timezone

def mainAdmin(request):
    """
    Return the /adminUser page which allows the user to see admin functionality
    Parameters:
    request - the HTTP POST request containing the inputted data by the user
    Return:
    The function returns the rendering of the admin home webpage
    """
    #Check if there is an active and incomplete event
    activeEvent = Event.objects.filter(endDate__gt=timezone.now()).filter(complete=False).exists()
    return render(request, "adminUser/mainAdmin.html", {'activeEvent': activeEvent})


def chooseEvent(request):
    """Return the adminUser/chooseEvent page with buttons for each event type
    
    Args:
        request: The HTTP request 
    
    Returns:
        render - The function returns the rendering of the chooseEvent webpage
        HttpResponse - Error code 403 if the user accessed this page incorrectly
    """
    buttonClicked = request.GET.get('buttonClicked')
    if buttonClicked:
        return render(request, "adminUser/chooseEvent.html")
    else:
        return HttpResponse(status = 403)


def confirmEvent(request):
    """Produce the confirmEvent page based on which button was selected in chooseEvent, where users can choose related targets
    
    Args:
        request: The HTTP request 
    
    Returns:
        render : the rendering of the confirmEvent page
        HttpResponse : A 400 error code is returned if this page was accessed without selecting an event type
    """
    eventType = request.GET.get('eventID')
    fieldsInfo = {} #each event has different associated fields and text
    if eventType == '1':
        fieldsInfo = {'field1': {'label': 'Enter a target amount of CO2 to be saved:', 'type':'range', 'max' : 50}}
    elif eventType == '2':
        fieldsInfo = {'field1': {'label': 'Enter a target number of total journeys:', 'type':'range', 'max' : 50}}
    elif eventType == '3':
        fieldsInfo = {'field1':{'label':'Select a building:', 'type':'dropdown'}, 'field2':{'label':'Enter a target number of times to visit the building:', 'type':'range', 'max' : 30}}
    elif eventType == '4':
        fieldsInfo = {}
    else:
        return HttpResponse(status=400)
    return render(request, "adminUser/confirmEvent.html", {'fieldsInfo': fieldsInfo, 'eventType': eventType, 'locations': Location.objects.filter(on_campus=True)})


def submitEvent(request):
    """Uses the provided information to create a new event

    Args:
        request: The HTTP request object containing information about the request.
    
    Returns:
        HttpResponse : Error code 400 is returned if there is no eventType, or 405 if the method is not POST
    """
    if request.method=="POST":
        eventType = request.POST.get('eventID')

        #Get the required information and create an Event in the database
        if eventType == '1' or eventType == '2':
            target = request.POST.get('field1')
            endDate = request.POST.get('endDate')
            Event.objects.create(type=eventType, target=target, endDate=endDate)
            return success(request)

        elif eventType == '3':
            target = request.POST.get('field2')
            building = request.POST.get('oncampus')
            endDate = request.POST.get('endDate')
            Event.objects.create(type=eventType, target=target,building=building, endDate=endDate)
            return success(request)

        elif eventType == '4':
            target = len(Location.objects.filter(on_campus = True))
            endDate = request.POST.get('endDate')
            Event.objects.create(type=eventType, target=target, endDate=endDate)
            return success(request)

        else:
            return HttpResponse(status=400)
    else:
        return HttpResponse(status=405) 


def success(request):
    """Produce a success page based on the created event

    Args:
        request: The HTTP request object containing information about the request.
    
    Returns:
        HttpResponse : Error code 400 is returned if there is no eventType,  or 405 if the method is not POST
    """
    if request.method=="POST":
        eventType = request.POST.get('eventID')
        if eventType not in ['1', '2', '3', '4']:
            return HttpResponse(status=400)
        else:
            #Determine a suitable information message about the event
            if eventType == '1':
                message = f"Save {request.POST.get('field1')} kilograms of CO2 by {datetime.strptime(request.POST.get('endDate'), '%Y-%m-%d').strftime('%d-%m-%Y')}."
            elif eventType == '2':
                message = f"Log {request.POST.get('field1')} total journeys by {datetime.strptime(request.POST.get('endDate'), '%Y-%m-%d').strftime('%d-%m-%Y')}."
            elif eventType == '3':
                message = f"Visit {request.POST.get('oncampus')}, {request.POST.get('field2')} times by {datetime.strptime(request.POST.get('endDate'), '%Y-%m-%d').strftime('%d-%m-%Y')}." 
            else:
                message = f"Visit every location on campus by {datetime.strptime(request.POST.get('endDate'), '%Y-%m-%d').strftime('%d-%m-%Y')}."
            return render(request, "adminUser/success.html", context={'eventMessage' : message})
    else:
        return HttpResponse(status=405)
    

def verify_suspicious_journey(request):
    """Produce the journey verification page

    Args:
        request: The HTTP request object containing information about the request.
    
    Returns:
        render : the rendered webpage
    """
    context = {'journeys': Journey.objects.filter(flagged=True)}
    return render(request, "adminUser/verify_journey.html", context=context)


def approve_journey(request):
    """A POST endpoint for approving that a journey is not suspicious

    Args:
        request: The HTTP request object containing information about the request.
        
    Returns:
        render: The rendered HTML template.
    """
    # Only handle POST requests
    if request.method == "POST":
        
        # Get the journey id from the request body
        id = request.POST.get("id")
        if id in ["", None]:
            return HttpResponse(status=400)
        
        # Return 404 if the journey object cannot be found
        journey = Journey.objects.get(id=id)
        if journey is None:
            return HttpResponse(status=404)
        
        # Update the flagged parameter inside the journey
        journey.flagged = False
        journey.save()
        return HttpResponse(status=201)
    
    # Return 404 for any other request method
    else:
        return HttpResponse(status=404)