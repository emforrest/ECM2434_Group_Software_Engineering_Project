from django.shortcuts import render

# Render user webpages here

from django.http import HttpResponse

def create(request):
    return HttpResponse("This is the group create page.")

def join(request):
    code = request.GET.get('code', 0)
    return HttpResponse((f"This is the group join page with code {code}."))