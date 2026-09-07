from django.contrib import admin, messages
from django.utils.html import format_html
from .models import ContactMessage, ContactSettings


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'status_badge', 'created_at', 'ip_address']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message', 'ip_address']
    readonly_fields = ['name', 'email', 'subject', 'message', 'ip_address', 'created_at']
    date_hierarchy = 'created_at'
    actions = ['mark_as_read', 'mark_as_unread', 'prune_30_days']

    def changelist_view(self, request, extra_context=None):
        # Automatically prune contact messages older than 30 days on admin view
        try:
            ContactMessage.prune_old_messages(days=30)
        except Exception:
            pass
        return super().changelist_view(request, extra_context=extra_context)

    @admin.display(description='Status')
    def status_badge(self, obj):
        if obj.is_read:
            return format_html('<span style="color:#059669;font-weight:600;">✓ Read</span>')
        return format_html('<span style="color:#dc2626;font-weight:700;">● Unread</span>')

    @admin.action(description='Mark selected messages as Read')
    def mark_as_read(self, request, queryset):
        count = queryset.update(is_read=True)
        self.message_user(request, f'{count} message(s) marked as read.', messages.SUCCESS)

    @admin.action(description='Mark selected messages as Unread')
    def mark_as_unread(self, request, queryset):
        count = queryset.update(is_read=False)
        self.message_user(request, f'{count} message(s) marked as unread.', messages.SUCCESS)

    @admin.action(description='Delete all contact messages older than 30 days')
    def prune_30_days(self, request, queryset):
        deleted = ContactMessage.prune_old_messages(days=30)
        self.message_user(request, f'Successfully purged {deleted} message(s) older than 30 days.', messages.SUCCESS)


@admin.register(ContactSettings)
class ContactSettingsAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Notifications', {'fields': ['email_notifications', 'notification_email']}),
        ('Limits', {'fields': ['rate_limit_per_hour']}),
        ('Content', {'fields': ['success_message']}),
    ]
