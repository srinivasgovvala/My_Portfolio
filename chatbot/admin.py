from django.contrib import admin, messages
from django.utils.html import format_html
from django.template.defaultfilters import truncatechars
from .models import ChatbotSettings, ChatMessage


@admin.register(ChatbotSettings)
class ChatbotSettingsAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Behavior', {'fields': ['is_enabled', 'model', 'max_tokens', 'temperature']}),
        ('Limits', {'fields': ['rate_limit_per_hour']}),
        ('Content', {'fields': ['welcome_message', 'system_prompt_extra']}),
    ]


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['short_session', 'short_user_message', 'short_ai_response', 'created_at', 'ip_address']
    readonly_fields = ['session_key', 'user_message', 'ai_response', 'ip_address', 'created_at']
    list_filter = ['created_at']
    search_fields = ['session_key', 'user_message', 'ai_response', 'ip_address']
    date_hierarchy = 'created_at'
    actions = ['prune_30_days']

    def changelist_view(self, request, extra_context=None):
        # Automatically prune chat logs older than 30 days on admin view
        try:
            ChatMessage.prune_old_messages(days=30)
        except Exception:
            pass
        return super().changelist_view(request, extra_context=extra_context)

    @admin.display(description='Session')
    def short_session(self, obj):
        return (obj.session_key or 'anon')[:8]

    @admin.display(description='Visitor Question')
    def short_user_message(self, obj):
        return truncatechars(obj.user_message, 50)

    @admin.display(description='AI Answer')
    def short_ai_response(self, obj):
        return truncatechars(obj.ai_response, 60)

    @admin.action(description='Delete all chat history older than 30 days')
    def prune_30_days(self, request, queryset):
        deleted = ChatMessage.prune_old_messages(days=30)
        self.message_user(request, f'Successfully purged {deleted} chat log(s) older than 30 days.', messages.SUCCESS)
