from django.shortcuts import render

# Render Login webpages here

from django.http import HttpResponse


def login(request):
    #return HttpResponse("This is the log in page.")
    return render(request, "login/login.html")
