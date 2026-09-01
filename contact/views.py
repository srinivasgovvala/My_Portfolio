import time
import logging
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from .forms import ContactForm
from .models import ContactSettings

logger = logging.getLogger(__name__)


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

        # Send email notification to portfolio owner
        recipient_email = cfg.notification_email or getattr(settings, 'CONTACT_EMAIL', '') or getattr(settings, 'EMAIL_HOST_USER', '')

        if recipient_email and getattr(settings, 'EMAIL_HOST_USER', ''):
            email_subject = f"[Portfolio Contact] {msg.subject} from {msg.name}"
            email_body = f"""You have received a new contact submission from your portfolio website!

👤 Name: {msg.name}
📧 Email: {msg.email}
📝 Subject: {msg.subject}
🌐 Sender IP: {msg.ip_address}

💬 Message:
{msg.message}

--------------------------------------------------
Reply directly to this email to respond to {msg.name} ({msg.email}).
"""
            try:
                email = EmailMessage(
                    subject=email_subject,
                    body=email_body,
                    from_email=settings.DEFAULT_FROM_EMAIL or settings.EMAIL_HOST_USER,
                    to=[recipient_email],
                    reply_to=[msg.email],
                )
                email.send(fail_silently=False)
                logger.info(f"Contact notification email sent successfully to {recipient_email}")
            except Exception as e:
                logger.error(f"Failed to send contact notification email: {e}")
                # Message is safely stored in database, so user still gets a success response

        return JsonResponse({'success': True, 'message': cfg.success_message})
    return JsonResponse({'error': 'Please check your input and try again.', 'errors': form.errors}, status=400)
