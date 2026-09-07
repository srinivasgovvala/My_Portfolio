from datetime import timedelta
from django.utils import timezone
from django.db import models


class ChatbotSettings(models.Model):
    is_enabled = models.BooleanField(default=True)
    model = models.CharField(max_length=100, default='google/gemini-2.5-flash')
    max_tokens = models.PositiveIntegerField(default=1024)
    temperature = models.FloatField(default=0.4)
    rate_limit_per_hour = models.PositiveIntegerField(default=20)
    welcome_message = models.TextField(default="Hi. I'm Srinivas AI. Ask me about Nagasrinivas's projects, skills, education, technologies or development work.")
    system_prompt_extra = models.TextField(blank=True, help_text='Additional instructions appended to the system prompt')

    class Meta:
        verbose_name = 'Chatbot Settings'
        verbose_name_plural = 'Chatbot Settings'

    def __str__(self):
        return 'Chatbot Settings'

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class ChatMessage(models.Model):
    session_key = models.CharField(max_length=40)
    user_message = models.TextField()
    ai_response = models.TextField()
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Chat {self.session_key[:8]} — {self.created_at}'

    @classmethod
    def prune_old_messages(cls, days=30):
        """Automatically delete chat messages older than `days` (default: 30 days)."""
        cutoff = timezone.now() - timedelta(days=days)
        deleted_count, _ = cls.objects.filter(created_at__lt=cutoff).delete()
        return deleted_count

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            try:
                ChatMessage.prune_old_messages(days=30)
            except Exception:
                pass
