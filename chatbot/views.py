import json
import time
import logging
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.conf import settings
from django.core.cache import cache
import urllib.request
import urllib.error
from .models import ChatbotSettings, ChatMessage
from core.models import PersonalProfile
from projects.models import Project, FutureProject
from profile_app.models import Technology
from education.models import Education
from experience.models import Experience

logger = logging.getLogger(__name__)

CONTEXT_CACHE_KEY = 'portfolio_chatbot_context'
CONTEXT_CACHE_TTL = 300  # 5 minutes


def get_portfolio_context():
    cached_ctx = cache.get(CONTEXT_CACHE_KEY)
    if cached_ctx:
        return cached_ctx

    try:
        profile = PersonalProfile.get()
    except Exception:
        profile = None

    projects = Project.objects.filter(is_completed=True).prefetch_related('technologies')
    future = FutureProject.objects.filter(is_active=True)
    techs = Technology.objects.filter(is_active=True)
    educations = Education.objects.filter(is_active=True)
    experiences = Experience.objects.filter(is_active=True)

    full_name = profile.full_name if profile else 'Nagasrinivas Govvala'
    title = 'Fresher Software Developer (Actively Seeking Full-Time Roles)'
    location = profile.location if profile else 'Hyderabad, Telangana, India'
    email = profile.email if profile else 'nagasrinivas@email.com'
    github = profile.github_url if profile else 'https://github.com/NagasrinivasGovvala'
    linkedin = profile.linkedin_url if profile else 'https://linkedin.com/in/nagasrinivas-govvala'
    available = True
    about = (
        'Nagasrinivas Govvala is a fresher looking for a software developer role from Hyderabad. '
        'He specializes in Python, Django, Machine Learning, and NLP, focusing on production-oriented web applications. '
        'He actively uses AI-assisted development tools like Claude and ChatGPT in his workflow. '
        'Nagasrinivas is currently seeking full-time software developer job opportunities.'
    )

    ctx = f"""PORTFOLIO DATA FOR {full_name.upper()}:

PROFILE:
- Name: {full_name}
- Role / Status: Fresher looking for a software developer role from Hyderabad (Not currently employed, actively seeking full-time job opportunities)
- Location: {location}
- Email: {email}
- GitHub: {github}
- LinkedIn: {linkedin}
- Specialization: Python, Django, Machine Learning, and NLP, focusing on production-oriented web applications
- AI Tools: Actively uses AI-assisted development tools like Claude and ChatGPT
- Summary: {about}

EDUCATION:
"""
    for edu in educations:
        ctx += f"- {edu.degree} in {edu.field} | {edu.institution} ({edu.year}) — Grade: {edu.grade}\n"

    ctx += "\nEXPERIENCE:\n"
    for exp in experiences:
        ctx += f"- {exp.title} at {exp.organization} ({exp.get_exp_type_display()}): {exp.description[:180]}\n"

    ctx += "\nCOMPLETED PROJECTS:\n"
    for p in projects:
        techs_list = ', '.join(t.name for t in p.technologies.all())
        desc = p.short_description
        if 'pid' in p.title.lower():
            desc = 'A professional corporate website developed for the PID-Control startup company by leveraging AI tools like Claude, OpenCode, and ChatGPT in the development process.'
            if 'Claude' not in techs_list:
                techs_list = f'{techs_list}, Claude, OpenCode, ChatGPT'
        ctx += f"- Project: **{p.title}** ({p.category})\n  Description: {desc}\n  Tech Stack: {techs_list}\n"
        if p.github_url:
            ctx += f"  GitHub: {p.github_url}\n"
        if p.live_url:
            ctx += f"  Live: {p.live_url}\n"

    ctx += "\nFUTURE / IN-DEVELOPMENT PROJECTS:\n"
    for fp in future:
        ctx += f"- {fp.title}: {fp.concept} (Status: {fp.get_status_display()})\n"

    ctx += "\nSKILLS & TECHNOLOGIES:\n"
    for t in techs:
        ctx += f"- {t.name} ({t.get_category_display()})\n"

    cache.set(CONTEXT_CACHE_KEY, ctx, CONTEXT_CACHE_TTL)
    return ctx


def get_client_ip(request):
    x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded:
        return x_forwarded.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


def check_rate_limit(request, limit_per_hour):
    ip = get_client_ip(request)
    cache_key = f'chatbot_rl_{ip}'
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
def ask(request):
    cfg = ChatbotSettings.get()
    if not cfg.is_enabled:
        return JsonResponse({'error': 'AI assistant is temporarily unavailable.'}, status=503)

    if not check_rate_limit(request, cfg.rate_limit_per_hour):
        return JsonResponse({'error': 'Too many requests. Please wait before asking again.'}, status=429)

    try:
        data = json.loads(request.body)
        user_msg = data.get('message', '').strip()[:500]
    except (json.JSONDecodeError, KeyError):
        return JsonResponse({'error': 'Invalid request.'}, status=400)

    if not user_msg:
        return JsonResponse({'error': 'Message cannot be empty.'}, status=400)

    api_key = settings.OPENROUTER_API_KEY
    if not api_key:
        return JsonResponse({'response': "AI assistant isn't configured yet. You can reach Nagasrinivas directly via the contact form or at his email."}, status=200)

    portfolio_ctx = get_portfolio_context()
    system_prompt = f"""You are Srinivas AI, the smart and helpful portfolio assistant for Nagasrinivas Govvala (Software Developer).
Your job is to answer visitor questions accurately, concisely, and engagingly using ONLY the portfolio data provided below.

FORMATTING RULES:
- Always answer directly without filler intros (do NOT say "Sure!", "Certainly!", "Here is what I found").
- When asked to introduce or tell about Nagasrinivas, start with: "**Nagasrinivas Govvala** is a fresher looking for a software developer role from Hyderabad."
- Keep responses compact: 2 to 4 concise bullet points or 1-2 brief paragraphs (under 90 words total).
- Each bullet point MUST be on its own separate line starting with "- ". Never cram multiple bullet points onto one line.
- Always format URLs as clean Markdown links: [Project Name Live Demo](url) or [GitHub Repo](url).
- Use clean Markdown: bold project titles and skills (e.g. **ResumeAI**, **Django**).
- If asked about projects, highlight the key purpose and core tech stack.
- If asked about something not in the portfolio data, reply politely: "I don't have that information in Nagasrinivas's portfolio."
{cfg.system_prompt_extra}

--- PORTFOLIO DATA ---
{portfolio_ctx}
--- END PORTFOLIO DATA ---
"""

    models_to_try = [cfg.model]
    for fallback in ['google/gemini-2.5-flash', 'mistralai/mistral-small-24b-instruct-2501', 'meta-llama/llama-3.3-70b-instruct']:
        if fallback not in models_to_try:
            models_to_try.append(fallback)

    ai_text = None
    last_error = None
    max_tokens_to_gen = min(cfg.max_tokens or 220, 220)
    gen_temperature = 0.2

    for model_name in models_to_try:
        payload = json.dumps({
            'model': model_name,
            'max_tokens': max_tokens_to_gen,
            'temperature': gen_temperature,
            'messages': [
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': user_msg},
            ],
        }).encode('utf-8')

        try:
            referer = request.build_absolute_uri('/')
        except Exception:
            referer = 'http://localhost:8000/'

        req = urllib.request.Request(
            settings.OPENROUTER_API_URL,
            data=payload,
            headers={
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json',
                'HTTP-Referer': referer,
                'X-Title': 'Nagasrinivas Portfolio AI',
            },
            method='POST',
        )

        try:
            with urllib.request.urlopen(req, timeout=6) as resp:
                result = json.loads(resp.read().decode('utf-8'))
                ai_text = result['choices'][0]['message']['content'].strip()
                break
        except urllib.error.HTTPError as e:
            last_error = e
            error_body = e.read().decode('utf-8', errors='ignore')
            logger.warning("OpenRouter error with model %s (code %s): %s", model_name, e.code, error_body)
            continue
        except Exception as e:
            last_error = e
            logger.warning("OpenRouter request exception with model %s: %s", model_name, e)
            continue

    if not ai_text:
        logger.error("All chatbot models failed. Last error: %s", last_error)
        return JsonResponse({'error': 'AI assistant is temporarily unavailable. Please try again later.'}, status=503)

    ChatMessage.objects.create(
        session_key=request.session.session_key or 'anon',
        user_message=user_msg,
        ai_response=ai_text,
        ip_address=get_client_ip(request),
    )

    return JsonResponse({'response': ai_text})
