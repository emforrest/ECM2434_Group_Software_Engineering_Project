"""Contains the function to render the register webpage, and sets a user up with their account, once passed all the validation checks.
Authors: 
- Abi Hinton
- Sam Townley
"""

from django.contrib.auth import authenticate, password_validation, login
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from user.models import Profile


def register(request):
    """
    Return the /register page which allows the user to create an account, and then redirects to the /user/ page.
    Once the user enters their details into the form, this function checks all the inputs are correct before creating an account in the 
    database. If the checks are not passed, the user is asked to enter their details again, and is given a corresponding error message.
    Parameters:
    request - the HTTP POST request containing the inputted data by the user
    Return:
    The function returns the rendering of the register webpage, and once an account has been successfully created, redirects the rendering
    to the /user/ page.
    """
    if request.method == 'POST':
        #accessing the data from the POST request
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        #checking whether the passwords match
        if password1 != password2:
            context = {"error": "The passwords do not match"}
            return render(request, "register/register.html", context)
        
        #checking user does not already exist
        user = authenticate(request, username=username, password=password1)
        userFilter = User.objects.filter(username=username)
        if user is not None or userFilter.exists():
            context = {"error": "This user already exists!"}
            return render(request, "register/register.html", context)
        
        #checking if email is already being used with a registered account
        userFilterEmail = User.objects.filter(email=email)
        if userFilterEmail.exists():
            context = {"error": "This email is already being used"}
            return render(request, "register/register.html", context)
        
        #validating password
        try:
            validatePass = password_validation.validate_password(password1)
        except ValidationError as error:
            context = {"error": error}
            return render(request, "register/register.html", context)
        
        #creating the new user and redirecting to user home page
        newUser = User.objects.create_user(first_name=first_name, 
                                      last_name=last_name, 
                                      email=email,
                                      username=username,
                                      password=password1)
        # Create profile on registration
        profile = Profile(user=newUser)
        profile.save()
        #log user into server
        userLogin = authenticate(request, username=username, password=password1)
        login(request, userLogin) 
        #redirect to /user/ page once account has been successfully created
        return redirect("/user/")
    
    return render(request, "register/register.html")

