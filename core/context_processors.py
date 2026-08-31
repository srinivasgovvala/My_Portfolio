from .models import SiteSettings, PersonalProfile, SEOSettings
from music.models import MusicTrack


def global_context(request):
    site = SiteSettings.get()
    profile = PersonalProfile.get()
    seo = SEOSettings.get()
    music_tracks = MusicTrack.objects.filter(is_active=True)
    return {
        'site': site,
        'profile': profile,
        'seo': seo,
        'music_tracks': music_tracks,
        'github_url': profile.github_url or 'https://github.com/NagasrinivasGovvala',
        'linkedin_url': profile.linkedin_url or 'https://linkedin.com/in/nagasrinivas-govvala',
        'contact_email': profile.email or 'nagasrinivas@email.com',
    }
