from datetime import timedelta
from django.utils import timezone
from django.db import models


class ContactMessage(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    subject = models.CharField(max_length=300)
    message = models.TextField()
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} — {self.subject} ({self.created_at.strftime("%Y-%m-%d")})'

    @classmethod
    def prune_old_messages(cls, days=30):
        """Automatically delete contact messages older than `days` (default: 30 days)."""
        cutoff = timezone.now() - timedelta(days=days)
        deleted_count, _ = cls.objects.filter(created_at__lt=cutoff).delete()
        return deleted_count

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            try:
                ContactMessage.prune_old_messages(days=30)
            except Exception:
                pass


class ContactSettings(models.Model):
    email_notifications = models.BooleanField(default=True)
    notification_email = models.EmailField(blank=True)
    rate_limit_per_hour = models.PositiveIntegerField(default=5)
    success_message = models.TextField(default="Thanks for reaching out! I'll get back to you soon.")

    class Meta:
        verbose_name = 'Contact Settings'
        verbose_name_plural = 'Contact Settings'

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj
