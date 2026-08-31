from django.contrib import admin
from .models import Skill, Technology


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'proficiency', 'order', 'is_active']
    list_editable = ['order', 'is_active', 'proficiency']
    list_filter = ['category', 'proficiency']
    ordering = ['category', 'order']


@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'related_project', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['category']
    ordering = ['category', 'order']
