from django.contrib import admin
from .models import Experience, Certification


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ['title', 'organization', 'exp_type', 'start_date', 'is_current', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['exp_type', 'is_current']


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ['name', 'issuer', 'date', 'order', 'is_active']
    list_editable = ['order', 'is_active']
