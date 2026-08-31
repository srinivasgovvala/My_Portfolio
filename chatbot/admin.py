from django.contrib import admin
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
    list_display = ['session_key', 'user_message', 'created_at']
    readonly_fields = ['session_key', 'user_message', 'ai_response', 'ip_address', 'created_at']
    list_filter = ['created_at']
