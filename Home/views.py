from django.shortcuts import render

# Create your views here.

def Home(request):
    return render(request, 'Home.html')

def Animationone(request):
    return render(request, 'Animationone.html')

def Animationtwo(request):
    return render(request, 'Animationtwo.html')

def Animationthree(request):
    return render(request, 'Animationthree.html')

def Animationfour(request):
    return render(request, 'Animationfour.html')