from django.shortcuts import render
#Render Main frontend templates here
from django.http import HttpResponse


def main(request):
    #return HttpResponse("Hello, world. This is main.")
    #return render(request, "main/main.html")
    return HttpResponse(template.render(request))
