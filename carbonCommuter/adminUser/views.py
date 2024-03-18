"""Contains the function to render the admin webpage.
Authors: 
- Abi Hinton
"""

from django.shortcuts import render

# Render user webpages here

from django.http import HttpResponse

def mainAdmin(request):
    """
    Return the /adminUser page which allows the user to see that they are an admin on the website
    Parameters:
    request - the HTTP POST request containing the inputted data by the user
    Return:
    The function returns the rendering of the admin home webpage
    """
    return render(request, "adminUser/mainAdmin.html")

def chooseEvent(request):
    return render(request, "adminUser/chooseEvent.html")

def confirmEvent(request):
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
        return HttpResponse(status=404)
    return render(request, "adminUser/confirmEvent.html", {'fieldsInfo': fieldsInfo})

def submitEvent(request):
    pass

