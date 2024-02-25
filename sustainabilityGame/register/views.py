from django.contrib.auth import authenticate, password_validation, login
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Render Login webpages here

from django.http import HttpResponse


def register(request):
    if request.method == 'POST':
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
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
        userLogin = authenticate(request, username=username, password=password1)
        login(request, userLogin) #log user into server
        return redirect("/user/")
    #return HttpResponse("This is the register page.")
    return render(request, "register/register.html")

