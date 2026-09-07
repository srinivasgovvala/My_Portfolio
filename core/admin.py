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
    list_display = ['full_name', 'title', 'email', 'resume_status', 'available_for_work']
    readonly_fields = ['resume_preview']
    fieldsets = [
        ('Identity', {'fields': ['full_name', 'title', 'location', 'email']}),
        ('Social', {'fields': ['github_url', 'linkedin_url']}),
        ('Content', {'fields': ['about_short', 'about_long']}),
        ('Resume Settings', {
            'fields': ['resume', 'resume_external_url', 'resume_preview'],
            'description': 'Upload a new PDF resume or enter an external URL (Google Drive, Cloudinary, AWS S3, etc.). Changes take effect immediately on your portfolio website.'
        }),
        ('Files', {'fields': ['profile_image']}),
        ('Status', {'fields': ['available_for_work']}),
    ]

    def has_add_permission(self, request):
        return not PersonalProfile.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    @admin.display(description='Current Resume')
    def resume_preview(self, obj):
        if not obj:
            return "No profile available"
        from django.utils.html import format_html
        from django.urls import reverse
        download_url = reverse('core:download_resume')

        info = []
        if obj.resume_external_url:
            info.append(f'<strong>External Link:</strong> <a href="{obj.resume_external_url}" target="_blank" rel="noopener">{obj.resume_external_url}</a>')
        if obj.resume:
            info.append(f'<strong>Uploaded File:</strong> {obj.resume.name}')
        if obj.resume_file_data:
            size_kb = round(len(obj.resume_file_data) / 1024, 1)
            info.append(f'<strong>Stored in Database:</strong> {size_kb} KB')

        details = '<br>'.join(info) if info else 'Default system resume is currently active.'
        buttons = (
            f'<div style="margin-top:10px;display:flex;gap:10px;align-items:center;">'
            f'<a href="{download_url}?view=1" target="_blank" style="padding:6px 14px;background:#4f46e5;color:#fff;border-radius:4px;text-decoration:none;font-weight:600;font-size:12px;">Preview Live Resume</a>'
            f'<a href="{download_url}" target="_blank" style="padding:6px 14px;background:#2563eb;color:#fff;border-radius:4px;text-decoration:none;font-weight:600;font-size:12px;">Download Live Resume</a>'
            f'</div>'
        )
        return format_html(f'{details}{buttons}')

    @admin.display(description='Resume')
    def resume_status(self, obj):
        from django.utils.html import format_html
        from django.urls import reverse
        download_url = reverse('core:download_resume')
        if obj.resume_external_url:
            return format_html('<a href="{}" target="_blank" style="color:#2563eb;font-weight:600;">External Link ↗</a>', obj.resume_external_url)
        return format_html('<a href="{}?view=1" target="_blank" style="color:#4f46e5;font-weight:600;">View PDF ↗</a>', download_url)


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
