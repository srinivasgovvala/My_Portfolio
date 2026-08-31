from django.contrib import admin
from .models import Project, ProjectTechnology, ProjectScreenshot, FutureProject


class ProjectScreenshotInline(admin.TabularInline):
    model = ProjectScreenshot
    extra = 1
    fields = ['image', 'caption', 'order']


@admin.register(ProjectTechnology)
class ProjectTechnologyAdmin(admin.ModelAdmin):
    list_display = ['name', 'color']
    search_fields = ['name']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'is_featured', 'is_completed', 'order']
    list_editable = ['is_featured', 'is_completed', 'order']
    list_filter = ['is_featured', 'is_completed', 'category']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['technologies']
    inlines = [ProjectScreenshotInline]
    fieldsets = [
        ('Basic Info', {'fields': ['title', 'slug', 'category', 'short_description', 'full_description']}),
        ('Case Study', {'fields': ['problem', 'solution', 'features', 'architecture', 'challenges', 'result', 'learning']}),
        ('Media', {'fields': ['thumbnail', 'hover_gif', 'video']}),
        ('Links', {'fields': ['github_url', 'live_url']}),
        ('Technologies', {'fields': ['technologies']}),
        ('Settings', {'fields': ['is_featured', 'is_completed', 'order']}),
    ]


@admin.register(FutureProject)
class FutureProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'progress_percentage', 'order', 'is_active']
    list_editable = ['status', 'order', 'is_active']
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = [
        ('Basic Info', {'fields': ['title', 'slug', 'concept', 'description']}),
        ('Status', {'fields': ['status', 'progress_percentage']}),
        ('Media & Tech', {'fields': ['thumbnail', 'technologies_planned']}),
        ('Settings', {'fields': ['order', 'is_active']}),
    ]
