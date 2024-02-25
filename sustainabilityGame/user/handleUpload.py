from django.http import HttpResponse

def handleUpload(request):
    if request.method == "POST":
        print("ok itprinted")