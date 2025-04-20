from django.shortcuts import render

# Create your views here.

def About(request):
    return render(request, 'About.html')

def Aboutparttwo(request):
    return render(request, 'AboutPage_part2.html')

def Aboutpartone(request):
    return render(request, 'Aboutone.html')
