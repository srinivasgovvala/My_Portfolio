from django.db import models


class MusicTrack(models.Model):
    SECTION_CHOICES = [
        ('home', 'Home / Hero'),
        ('projects', 'Projects'),
        ('case_study', 'Case Study'),
        ('future', 'Future Projects'),
        ('contact', 'Contact'),
        ('default', 'Default / Global'),
    ]
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=200, blank=True)
    audio_file = models.FileField(upload_to='music/')
    section = models.CharField(max_length=20, choices=SECTION_CHOICES, default='default')
    default_volume = models.FloatField(default=0.4, help_text='0.0 to 1.0')
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['section', 'order']

    def __str__(self):
        return f'{self.title} [{self.get_section_display()}]'
