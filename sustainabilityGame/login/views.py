from django.shortcuts import render

# Render Login webpages here

from django.http import HttpResponse


def register(request):
    return HttpResponse("This is the register page.")

def signIn(request):
    return HttpResponse("This is the sign in page.")