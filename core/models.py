import os
from django.db import models


class SiteSettings(models.Model):
    site_name = models.CharField(max_length=200, default='Nagasrinivas Govvala')
    tagline = models.CharField(max_length=500, default='Building practical software with Python, Django, AI and modern web technologies.')
    favicon = models.ImageField(upload_to='site/', blank=True, null=True)
    logo_text = models.CharField(max_length=10, default='NG.')
    maintenance_mode = models.BooleanField(default=False)
    analytics_code = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'

    def __str__(self):
        return self.site_name

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class PersonalProfile(models.Model):
    full_name = models.CharField(max_length=200, default='Nagasrinivas Govvala')
    title = models.CharField(max_length=200, default='Fresher Software Developer')
    location = models.CharField(max_length=200, default='Hyderabad, Telangana, India')
    email = models.EmailField(default='nagasrinivas@email.com')
    github_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    about_short = models.TextField(default='A fresher software developer who builds real applications.', blank=True)
    about_long = models.TextField(default='', blank=True)
    profile_image = models.ImageField(upload_to='profile/', blank=True, null=True)
    resume = models.FileField(upload_to='resume/', blank=True, null=True, help_text="Upload a resume file (PDF recommended).")
    resume_file_data = models.BinaryField(blank=True, null=True, editable=False)
    resume_filename = models.CharField(max_length=255, default='Nagasrinivas_Govvala_Resume.pdf', blank=True)
    resume_external_url = models.URLField(blank=True, help_text="Optional external link (e.g. Google Drive, S3, Dropbox). If set, this URL is used for download.")
    available_for_work = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Personal Profile'
        verbose_name_plural = 'Personal Profile'

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        self.pk = 1

        # Check existing instance in the database to detect file changes
        old_instance = None
        try:
            old_instance = PersonalProfile.objects.filter(pk=1).first()
        except Exception:
            pass

        from django.core.files.uploadedfile import UploadedFile

        # Case 1: Resume was cleared (e.g. user checked 'Clear' in admin)
        if not self.resume:
            if old_instance and old_instance.resume:
                try:
                    if old_instance.resume.name and old_instance.resume.name != 'resume/resume.pdf':
                        old_instance.resume.delete(save=False)
                except Exception:
                    pass
            self.resume_file_data = None
            self.resume_filename = ''

        # Case 2: Resume file is provided
        else:
            f = getattr(self.resume, 'file', None)
            is_new_upload = isinstance(f, UploadedFile)

            # Delete old file from storage when a new file is uploaded
            if is_new_upload and old_instance and old_instance.resume:
                try:
                    old_path = getattr(old_instance.resume, 'name', None)
                    new_path = getattr(self.resume, 'name', None)
                    if old_path and old_path != new_path and old_path != 'resume/resume.pdf':
                        old_instance.resume.delete(save=False)
                except Exception:
                    pass

            # Replace database binary data with newly uploaded file bytes
            if f and (is_new_upload or not self.resume_file_data):
                try:
                    if hasattr(f, 'read'):
                        content = f.read()
                        if content:
                            self.resume_file_data = content
                            if self.resume.name:
                                self.resume_filename = os.path.basename(self.resume.name)
                    if hasattr(f, 'seek'):
                        f.seek(0)
                except Exception:
                    pass

        super().save(*args, **kwargs)

    @classmethod
    def get(cls):
        obj, created = cls.objects.get_or_create(
            pk=1,
            defaults={
                'full_name': 'Nagasrinivas Govvala',
                'title': 'Fresher Software Developer',
                'location': 'Hyderabad, Telangana, India',
                'github_url': 'https://github.com/NagasrinivasGovvala',
                'linkedin_url': 'https://linkedin.com/in/nagasrinivas-govvala',
                'resume': 'resume/resume.pdf',
            }
        )
        if not obj.resume and not obj.resume_file_data and not obj.resume_external_url and created:
            obj.resume = 'resume/resume.pdf'
            obj.save(update_fields=['resume'])
        return obj


class HeroRole(models.Model):
    role = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Hero Role'
        verbose_name_plural = 'Hero Roles'

    def __str__(self):
        return self.role


class SEOSettings(models.Model):
    page_title = models.CharField(max_length=200, default='Nagasrinivas Govvala | Fresher Software Developer')
    meta_description = models.TextField(max_length=300, default='Nagasrinivas Govvala — Fresher Software Developer from Hyderabad. Python, Django, AI/ML, Full-Stack web development.')
    og_image = models.ImageField(upload_to='seo/', blank=True, null=True)
    google_site_verification = models.CharField(max_length=200, blank=True)
    canonical_url = models.URLField(blank=True)

    class Meta:
        verbose_name = 'SEO Settings'
        verbose_name_plural = 'SEO Settings'

    def __str__(self):
        return self.page_title

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj
