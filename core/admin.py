from django.contrib import admin
from .models import SiteSettings, PersonalProfile, HeroRole, SEOSettings


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Branding', {'fields': ['site_name', 'tagline', 'logo_text', 'favicon']}),
        ('Options', {'fields': ['maintenance_mode', 'analytics_code']}),
    ]


@admin.register(PersonalProfile)
class PersonalProfileAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Identity', {'fields': ['full_name', 'title', 'location', 'email']}),
        ('Social', {'fields': ['github_url', 'linkedin_url']}),
        ('Content', {'fields': ['about_short', 'about_long']}),
        ('Files', {'fields': ['profile_image', 'resume']}),
        ('Status', {'fields': ['available_for_work']}),
    ]


@admin.register(HeroRole)
class HeroRoleAdmin(admin.ModelAdmin):
    list_display = ['role', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    ordering = ['order']


@admin.register(SEOSettings)
class SEOSettingsAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Meta', {'fields': ['page_title', 'meta_description', 'og_image']}),
        ('Technical', {'fields': ['canonical_url', 'google_site_verification']}),
    ]
