import os
import time
import json
import logging
import urllib.request
import urllib.error
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import ensure_csrf_cookie
from django.core.mail import EmailMessage
from django.conf import settings
from .forms import ContactForm
from .models import ContactSettings

logger = logging.getLogger(__name__)


def get_client_ip(request):
    """Resolves client IP address across standard proxies (Vercel, Cloudflare, AWS)."""
    cf_ip = request.META.get('HTTP_CF_CONNECTING_IP')
    if cf_ip:
        return cf_ip.strip()
    x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded:
        return x_forwarded.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', '127.0.0.1')


def is_rate_limited(request, limit_per_hour=30):
    """Checks if current IP has exceeded the hourly submission threshold."""
    ip = get_client_ip(request)
    cache_key = f'contact_rl_{ip}'
    now = int(time.time())
    window_start = now - 3600
    session = request.session
    history = [t for t in session.get(cache_key, []) if t > window_start]
    session[cache_key] = history
    return len(history) >= limit_per_hour


def record_submission(request):
    """Records a successful submission timestamp in user session."""
    ip = get_client_ip(request)
    cache_key = f'contact_rl_{ip}'
    now = int(time.time())
    window_start = now - 3600
    session = request.session
    history = [t for t in session.get(cache_key, []) if t > window_start]
    history.append(now)
    session[cache_key] = history


def send_contact_notification(msg, recipient_email):
    """
    Sends email notification to portfolio owner.
    Supports Resend HTTP API (recommended for serverless) and Django SMTP.
    """
    email_subject = f"[Portfolio Contact] {msg.name} ({msg.email}) — {msg.subject}"
    timestamp_str = msg.created_at.strftime('%Y-%m-%d %I:%M %p') if getattr(msg, 'created_at', None) else 'Just now'

    email_body = f"""====================================================
📬 NEW CONTACT MESSAGE FROM YOUR PORTFOLIO
====================================================

👤 SENDER NAME   : {msg.name}
📧 SENDER EMAIL  : {msg.email}
📝 SUBJECT       : {msg.subject}
🌐 SENDER IP     : {msg.ip_address}
📅 DATE & TIME   : {timestamp_str}

====================================================
💬 MESSAGE:
====================================================

{msg.message}

====================================================
💡 TO REPLY:
Click "Reply" in your email client to respond directly to {msg.name} at {msg.email}.
====================================================
"""

    # 1. Try Resend HTTP API (if configured)
    resend_api_key = getattr(settings, 'RESEND_API_KEY', '') or os.environ.get('RESEND_API_KEY', '')
    if resend_api_key:
        try:
            url = 'https://api.resend.com/emails'
            headers = {
                'Authorization': f'Bearer {resend_api_key}',
                'Content-Type': 'application/json',
                'User-Agent': 'Django-Portfolio/1.0',
            }
            from_addr = getattr(settings, 'DEFAULT_FROM_EMAIL', '')
            if not from_addr or 'gmail.com' in from_addr or 'noreply' in from_addr:
                from_addr = f'"{msg.name} via Portfolio" <onboarding@resend.dev>'
            else:
                from_addr = f'"{msg.name} via Portfolio" <{from_addr}>'

            payload = json.dumps({
                'from': from_addr,
                'to': [recipient_email],
                'reply_to': f'"{msg.name}" <{msg.email}>',
                'subject': email_subject,
                'text': email_body,
            }).encode('utf-8')

            req = urllib.request.Request(url, data=payload, headers=headers, method='POST')
            with urllib.request.urlopen(req, timeout=10) as response:
                if response.status in (200, 201):
                    logger.info(f"Contact email dispatched via Resend API to {recipient_email}")
                    return True
        except Exception as e:
            logger.error(f"Resend API error: {e}")

    # 2. Fallback to standard SMTP (Gmail / SMTP backend)
    host_user = getattr(settings, 'EMAIL_HOST_USER', '') or os.environ.get('EMAIL_HOST_USER', '')
    host_pwd = getattr(settings, 'EMAIL_HOST_PASSWORD', '') or os.environ.get('EMAIL_HOST_PASSWORD', '')

    if host_user and host_pwd:
        try:
            from_header = f'"{msg.name} via Portfolio" <{settings.DEFAULT_FROM_EMAIL or host_user}>'
            email = EmailMessage(
                subject=email_subject,
                body=email_body,
                from_email=from_header,
                to=[recipient_email],
                reply_to=[f'"{msg.name}" <{msg.email}>'],
            )
            email.send(fail_silently=False)
            logger.info(f"Contact email dispatched via SMTP to {recipient_email}")
            return True
        except Exception as e:
            logger.error(f"SMTP error: {e}")
            return False

    return False


@require_POST
def send(request):
    """Handles contact form AJAX submissions."""
    cfg = ContactSettings.get()
    limit = max(cfg.rate_limit_per_hour, 30)

    # 1. Rate limiting check
    if is_rate_limited(request, limit):
        return JsonResponse(
            {
                'success': False,
                'error': 'Rate limit reached. Please wait a few minutes before submitting another message.'
            },
            status=429
        )

    # 2. Form validation
    form = ContactForm(request.POST)
    if not form.is_valid():
        first_error = 'Please check your inputs and try again.'
        for field, errors in form.errors.items():
            if errors:
                first_error = errors[0]
                break
        return JsonResponse(
            {
                'success': False,
                'error': first_error,
                'errors': form.errors.get_json_data()
            },
            status=400
        )

    # 3. Save contact message to database
    msg = form.save(commit=False)
    msg.ip_address = get_client_ip(request)
    msg.save()

    # 4. Record successful submission for rate limiting
    record_submission(request)

    # 5. Dispatch notification email
    recipient = cfg.notification_email or getattr(settings, 'CONTACT_EMAIL', '') or getattr(settings, 'EMAIL_HOST_USER', '')
    if recipient and cfg.email_notifications:
        send_contact_notification(msg, recipient)

    # 6. Return success response
    success_msg = cfg.success_message or "Thank you for reaching out! I'll get back to you shortly."
    return JsonResponse({'success': True, 'message': success_msg})
