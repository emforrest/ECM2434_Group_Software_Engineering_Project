from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from user.models import Profile


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        print(username, password)
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
        
        return redirect("/user/")
    return render(request, "login/login.html")

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect("/login/")
    return render(request, "login/logout.html")