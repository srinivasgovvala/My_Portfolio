from django.contrib import admin
from .models import MusicTrack


@admin.register(MusicTrack)
class MusicTrackAdmin(admin.ModelAdmin):
    list_display = ['title', 'artist', 'section', 'default_volume', 'order', 'is_active']
    list_editable = ['order', 'is_active', 'default_volume']
    list_filter = ['section', 'is_active']
