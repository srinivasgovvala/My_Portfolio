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
