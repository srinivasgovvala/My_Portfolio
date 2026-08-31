from django.contrib import admin
from .models import Education


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ['degree', 'field', 'institution', 'year', 'grade', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    ordering = ['-year']
