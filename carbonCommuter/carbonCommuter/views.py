#render app templates here
from django.shortcuts import render
#from django.shortcuts import render_to_response
from django.template import RequestContext

'''def custom_404(request, exception):
    return render(request, 'main/404.html', status=404)'''

def error_400(request, *args, **argv):
    response = render(request,'main/400.html', status=400)
    response.status_code = 400
    return response

def error_403(request, *args, **argv):
    return render(request,'main/403.html', {}, status=403)

def error_404(request, *args, **argv):
    return render(request,'main/404.html', {}, status=404)

def error_500(request, *args, **argv):
    return render(request,'main/500.html', {}, status=500)