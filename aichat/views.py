from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return render(request, "index.html", {
        "user": request.user  # Pass user object to template
    })

# def Home(request):
#     return render(request, "Home.html")

def Chat(request):
    return render(request, "Chat.html", {
        "user": request.user
    })

def About(request):
    return render(request, "About.html", {
        "user": request.user
    })

def Contact(request):
    return render(request, "Contact.html", {
        "user": request.user
    })
