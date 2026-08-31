from django.db import models
from django.utils.text import slugify


STATUS_CHOICES = [
    ('concept', 'Concept'),
    ('research', 'Research'),
    ('development', 'Development'),
    ('testing', 'Testing'),
    ('live', 'Live'),
]


class ProjectTechnology(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=20, default='#9333ea')

    class Meta:
        verbose_name_plural = 'Project Technologies'

    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    category = models.CharField(max_length=200)
    short_description = models.TextField(max_length=300)
    full_description = models.TextField()
    problem = models.TextField(blank=True)
    solution = models.TextField(blank=True)
    features = models.TextField(blank=True, help_text='One feature per line')
    architecture = models.TextField(blank=True)
    challenges = models.TextField(blank=True)
    result = models.TextField(blank=True)
    learning = models.TextField(blank=True)
    technologies = models.ManyToManyField(ProjectTechnology, blank=True)
    thumbnail = models.ImageField(upload_to='projects/thumbnails/', blank=True, null=True)
    hover_gif = models.FileField(upload_to='projects/gifs/', blank=True, null=True)
    video = models.FileField(upload_to='projects/videos/', blank=True, null=True)
    github_url = models.URLField(blank=True)
    live_url = models.URLField(blank=True)
    is_featured = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def features_list(self):
        return [f.strip() for f in self.features.split('\n') if f.strip()]


class ProjectScreenshot(models.Model):
    project = models.ForeignKey(Project, related_name='screenshots', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='projects/screenshots/')
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.project.title} — Screenshot {self.order}'


class FutureProject(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    concept = models.CharField(max_length=300)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='concept')
    progress_percentage = models.PositiveIntegerField(blank=True, null=True, help_text='Leave blank to hide progress bar')
    thumbnail = models.ImageField(upload_to='projects/future/', blank=True, null=True)
    technologies_planned = models.CharField(max_length=500, blank=True, help_text='Comma-separated')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_technologies_list(self):
        return [t.strip() for t in self.technologies_planned.split(',') if t.strip()]
