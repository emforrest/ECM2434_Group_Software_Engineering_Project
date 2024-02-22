from django.shortcuts import render

# Render user webpages here

from django.http import HttpResponse

def mainAdmin(request):
    #return HttpResponse("This is the group create page.")
    return render(request, "admin/mainAdmin.html")

