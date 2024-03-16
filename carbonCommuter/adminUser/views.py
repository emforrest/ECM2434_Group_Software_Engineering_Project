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

def createEvent(request):
    return render(request, "adminUser/createEvent.html")

