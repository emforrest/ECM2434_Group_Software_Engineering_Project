from django.shortcuts import render
#Render Main frontend templates here
from django.http import HttpResponse
from django.template import loader


def main(request):
    #return HttpResponse("Hello, world. This is main.")
    #return render(request, "main/main.html")
    template = loader.get_template("main/main.html")
    return HttpResponse(template.render(request))
