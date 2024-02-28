"""Contains the function to render the login webpage, and allows the user to login and logout of their account.
Authors: 
- Abi Hinton
- Sam Townley
"""

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from user.models import Profile


def login_view(request):
    """
    Return the /login page which allows the user to login to their account, and then redirects to the /user/ page.
    Once the user enters their details into the form, this function checks both the username and password match up to a record in the 
    database, before logging the user in to their account. If the details do not match, the user is asked to re-enter their details, 
    with a corresponding error message.
    Parameters:
    request - the HTTP POST request containing the inputted data by the user
    Return:
    The function returns the rendering of the login webpage, and once an user has been successfully logged in, redirects the rendering
    to the /user/ page.
    """
    if request.method == 'POST':
        #accessing the data from the POST request
        username = request.POST.get("username")
        password = request.POST.get("password")
        #checking the user details inputted against the database
        user = authenticate(request, username=username, password=password)
        if user is None:
            print("Invalid username or password")
            context = {"error": "Invalid username or password"}
            return render(request, "login/login.html", context)
        login(request, user) #log user into server
        
        # Create profile for user if they are a legacy user
        print("login")
        if not(hasattr(user, 'profile')):
            print("creating profile")
            profile = Profile(user=user)
            profile.save()
        #redirect to /user/ page once account has been successfully logged in
        return redirect("/user/")
    return render(request, "login/login.html")

def logout_view(request):
    """
    Return the /login/logout page which allows the user to logout to their account, and then redirects back to the login page.
    It double checks to ensure the user definitely wants to logout, before logging the user out of their account.
    Parameters:
    request - the HTTP POST request containing the inputted data by the user (not used)
    Return:
    The function returns the rendering of the logout page, and if the user confirms to logout, returns the rendering back to the user page.
    """
    if request.method == 'POST':
        logout(request) #log user out of account
        return redirect("/login/")
    return render(request, "login/logout.html")