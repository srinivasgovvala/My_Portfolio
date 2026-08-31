"""Update project media paths in the database."""
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio.settings.development')
django.setup()

from projects.models import Project
from core.models import PersonalProfile

# Update project thumbnails and GIFs
updates = {
    'resumeai': {
        'thumbnail': 'projects/thumbnails/resumeai-thumb.png',
        'hover_gif': 'projects/gifs/resumeai-hover.gif',
    },
    'toxic-comment-classification': {
        'thumbnail': 'projects/thumbnails/toxic-thumb.png',
        'hover_gif': 'projects/gifs/toxic-hover.gif',
    },
    'pid-controls': {
        'thumbnail': 'projects/thumbnails/pid-thumb.png',
        'hover_gif': 'projects/gifs/pid-hover.gif',
    },
}

for slug, media in updates.items():
    try:
        p = Project.objects.get(slug=slug)
        p.thumbnail = media['thumbnail']
        p.hover_gif = media['hover_gif']
        p.save()
        print(f"  Updated {slug}")
    except Project.DoesNotExist:
        print(f"  NOT FOUND: {slug}")

# Update profile resume
profile = PersonalProfile.get()
profile.resume = 'resume/resume.pdf'
profile.save()
print("  Updated resume")
print("Done.")
