from django.db import models


class Education(models.Model):
    degree = models.CharField(max_length=200)
    field = models.CharField(max_length=200)
    institution = models.CharField(max_length=300)
    year = models.CharField(max_length=50, help_text='e.g. 2022-2025 or 2019-2022')
    grade = models.CharField(max_length=100, help_text='e.g. CGPA: 7.17 or Percentage: 70%')
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', '-id']

    def __str__(self):
        return f'{self.degree} — {self.institution} ({self.year})'
