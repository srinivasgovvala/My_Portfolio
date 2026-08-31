from django.db import models


CATEGORY_CHOICES = [
    ('programming', 'Programming'),
    ('web', 'Web'),
    ('data_ml', 'Data / ML'),
    ('database', 'Database'),
    ('cloud', 'Cloud'),
    ('tools', 'Tools'),
    ('ai_tools', 'AI Development Tools'),
]

PROFICIENCY_CHOICES = [
    ('primary', 'Primary'),
    ('working', 'Working Knowledge'),
    ('familiar', 'Familiar'),
]


class Skill(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    proficiency = models.CharField(max_length=20, choices=PROFICIENCY_CHOICES, default='working')
    icon = models.CharField(max_length=100, blank=True, help_text='SVG icon name or emoji')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['category', 'order']

    def __str__(self):
        return f'{self.name} ({self.get_category_display()})'


class Technology(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True, help_text='What has Nagasrinivas used it for?')
    related_project = models.CharField(max_length=200, blank=True, help_text='e.g. ResumeAI, Toxic Comment Classification')
    color = models.CharField(max_length=20, default='#9333ea', help_text='Hex color for the node')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['category', 'order']
        verbose_name_plural = 'Technologies'

    def __str__(self):
        return self.name
