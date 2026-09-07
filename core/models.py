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
    about_short = models.TextField(default='A fresher software developer who builds real applications.')
    about_long = models.TextField(default='')
    profile_image = models.ImageField(upload_to='profile/', blank=True, null=True)
    resume = models.FileField(upload_to='resume/', blank=True, null=True)
    available_for_work = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Personal Profile'
        verbose_name_plural = 'Personal Profile'

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        self.pk = 1
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
        if not obj.resume:
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
