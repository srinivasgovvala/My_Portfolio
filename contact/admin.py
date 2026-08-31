from django.contrib import admin
from .models import ContactMessage, ContactSettings


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'is_read', 'created_at']
    list_editable = ['is_read']
    list_filter = ['is_read', 'created_at']
    readonly_fields = ['name', 'email', 'subject', 'message', 'ip_address', 'created_at']


@admin.register(ContactSettings)
class ContactSettingsAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Notifications', {'fields': ['email_notifications', 'notification_email']}),
        ('Limits', {'fields': ['rate_limit_per_hour']}),
        ('Content', {'fields': ['success_message']}),
    ]
