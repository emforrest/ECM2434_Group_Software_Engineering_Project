from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

# Render Login webpages here

from django.http import HttpResponse


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        print(username, password)
        user = authenticate(request, username=username, password=password)
        if user is None:
            context = {"error": "Invalid username or password"}
            return render(request, "login/login.html", context)
        #login(request, user) #log user into server
        return redirect("/user/")

    #return HttpResponse("This is the log in page.")
    return render(request, "login/login.html")
