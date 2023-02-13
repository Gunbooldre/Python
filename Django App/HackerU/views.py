from django.http import HttpResponse


from django.http import HttpResponse
from django.shortcuts import render

# def home(request):
#     return HttpResponse("Hello Wolrd")

def home (request):
    name = "Dias"
    return render(request, "home.html", {'name':name})


def about (request):
    name = "About us"
    return render(request, "about.html", {'name':name})