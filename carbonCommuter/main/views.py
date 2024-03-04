from django.shortcuts import render, redirect
#Render Main frontend templates here
from django.http import HttpResponse
from django.template import loader


def main(request):
    if not request.user.is_authenticated:
        return render(request, "main/main.html")
    else:
        return redirect("/user/")
