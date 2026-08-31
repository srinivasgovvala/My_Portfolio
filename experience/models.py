from django.db import models


class Experience(models.Model):
    TYPE_CHOICES = [
        ('part_time', 'Part-Time'),
        ('virtual_internship', 'Virtual Internship / Training'),
        ('internship', 'Internship / Training'),
        ('freelance', 'Freelance'),
        ('project', 'Project'),
    ]
    title = models.CharField(max_length=200)
    organization = models.CharField(max_length=200)
    exp_type = models.CharField(max_length=30, choices=TYPE_CHOICES, default='part_time')
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    is_current = models.BooleanField(default=False)
    description = models.TextField()
    technologies = models.CharField(max_length=500, blank=True, help_text='Comma-separated list')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', '-start_date']

    def __str__(self):
        return f'{self.title} at {self.organization}'


class Certification(models.Model):
    name = models.CharField(max_length=300)
    issuer = models.CharField(max_length=200)
    date = models.DateField(blank=True, null=True)
    credential_url = models.URLField(blank=True)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-date', 'order']

    def __str__(self):
        return f'{self.name} — {self.issuer}'
