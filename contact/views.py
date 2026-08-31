import time
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .forms import ContactForm
from .models import ContactSettings


def get_client_ip(request):
    x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded:
        return x_forwarded.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


def check_rate_limit(request, limit_per_hour):
    ip = get_client_ip(request)
    cache_key = f'contact_rl_{ip}'
    now = int(time.time())
    window_start = now - 3600
    session = request.session
    history = session.get(cache_key, [])
    history = [t for t in history if t > window_start]
    if len(history) >= limit_per_hour:
        return False
    history.append(now)
    session[cache_key] = history
    return True


@require_POST
def send(request):
    cfg = ContactSettings.get()
    if not check_rate_limit(request, cfg.rate_limit_per_hour):
        return JsonResponse({'error': 'Too many submissions. Please wait before trying again.'}, status=429)

    form = ContactForm(request.POST)
    if form.is_valid():
        msg = form.save(commit=False)
        msg.ip_address = get_client_ip(request)
        msg.save()
        return JsonResponse({'success': True, 'message': cfg.success_message})
    return JsonResponse({'error': 'Please check your input and try again.', 'errors': form.errors}, status=400)
