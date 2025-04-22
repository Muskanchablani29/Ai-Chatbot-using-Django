from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Contact

def contact_view(request):
    if request.method == 'POST':
        try:
            contact = Contact(
                name=request.POST['name'],
                email=request.POST['email'],
                subject=request.POST['subject'],
                message=request.POST['message']
            )
            contact.save()
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')
        except Exception as e:
            messages.error(request, 'An error occurred while sending your message.')
    return render(request, 'Contact.html')
