from django.contrib.auth import logout
from django.http.response import HttpResponseRedirect
from django.shortcuts import render


# Create your views here.
def wasaboo(request):
    return render(request, "index.html")


def dashboard(request):
    return render(request, "home.html")

def logout_view(request):
    logout(request) 
    return HttpResponseRedirect('/login/')
