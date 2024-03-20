"""Contains the function to render the admin webpage.
Authors: 
- Abi Hinton
- Eleanor Forrest
"""

from django.shortcuts import render
from main.models import Location
from django.http import HttpResponse
from adminUser.models import Event
from datetime import datetime
from django.utils import timezone

NUM_BUILDINGS = 27

def mainAdmin(request):
    """
    Return the /adminUser page which allows the user to see that they are an admin on the website
    Parameters:
    request - the HTTP POST request containing the inputted data by the user
    Return:
    The function returns the rendering of the admin home webpage
    """
    ##Event.objects.all().delete() 
    #Check if there is an active event
    activeEvent = Event.objects.filter(endDate__gt=timezone.now()).exists()
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
    fieldsInfo = {}
    if eventType == '1':
        fieldsInfo = {'field1': {'label': 'Enter a target amount of CO2 to be saved:', 'type':'text'}}
    elif eventType == '2':
        fieldsInfo = {'field1': {'label': 'Enter a target number of total journeys:', 'type':'text'}}
    elif eventType == '3':
        fieldsInfo = {'field1':{'label':'Select a building:', 'type':'dropdown'}, 'field2':{'label':'Enter a target number of times to visit the building:', 'type':'text'}}
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
            target = NUM_BUILDINGS
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

##Event.objects.all().delete() 
##print(Event.objects.all())