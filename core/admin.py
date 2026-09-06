from django.contrib import admin
from .models import ContactMessage

@admin.register(ContactMessage)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at') # Columns you see in the list
    readonly_fields = ('name', 'email', 'message', 'created_at') # Prevent editing