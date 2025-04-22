from django.contrib import admin
from .models import Contact
from .forms import ContactForm

class ContactAdmin(admin.ModelAdmin):
    form = ContactForm
    list_display = ('name', 'email', 'subject', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'email', 'subject', 'message')

admin.site.register(Contact, ContactAdmin)
