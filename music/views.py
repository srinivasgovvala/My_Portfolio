from django.http import JsonResponse
from .models import MusicTrack


def track_list(request):
    section = request.GET.get('section', 'default')
    tracks = MusicTrack.objects.filter(is_active=True, section=section)
    if not tracks.exists():
        tracks = MusicTrack.objects.filter(is_active=True, section='default')
    data = [
        {
            'id': t.pk,
            'title': t.title,
            'artist': t.artist,
            'url': request.build_absolute_uri(t.audio_file.url) if t.audio_file else None,
            'volume': t.default_volume,
        }
        for t in tracks if t.audio_file
    ]
    return JsonResponse({'tracks': data})
