from django import template
from django.utils.safestring import mark_safe

register = template.Library()

# Accurate, real brand SVG logos (viewBox, SVG body)
_LOGOS = {
    # Python - Official dual color
    'python': (
        '0 0 110 110',
        '<path d="M54.3 2C24.4 2 26 15 26 15l.1 13.5h28.6v4.1H14.2S2 31 2 61.3s10.6 29.5 10.6 29.5h6.3v-14s-.3-16.8 16.5-16.8h28.7s16-.3 16-15.5V17.8S101.9 2 54.3 2zm-15.8 9.1c3.1 0 5.6 2.5 5.6 5.6s-2.5 5.6-5.6 5.6-5.6-2.5-5.6-5.6 2.5-5.6 5.6-5.6z" fill="#3776AB"/><path d="M55.7 108c29.9 0 28.3-13 28.3-13l-.1-13.5H55.3v-4.1h40.5s12.2 1.6 12.2-28.7-10.6-29.5-10.6-29.5h-6.3v14s.3 16.8-16.5 16.8H45.9s-16 .3-16 15.5v21.7S8.1 108 55.7 108zm15.8-9.1c-3.1 0-5.6-2.5-5.6-5.6s2.5-5.6 5.6-5.6 5.6 2.5 5.6 5.6-2.5 5.6-5.6 5.6z" fill="#FFD43B"/>'
    ),
    # Django - Official green mark
    'django': (
        '0 0 256 256',
        '<path d="M72.9 0h36.7v170.8c-18.8 3.6-32.7 5-47.7 5-44.8 0-68.3-20.2-68.3-59.2 0-37.5 24.9-61.8 63.2-61.8 6 0 10.5.5 16 1.9V0zm0 88.6c-4.2-.9-8.4-1.4-12.7-1.4-18.6 0-29.3 11.5-29.3 31.6 0 19.6 10.3 30.4 29.1 30.4 4.2 0 7.6-.2 12.9-.9V88.6zm63.2-5.7h36.7v108.4c0 37.6-2.8 55.7-11 71.3-8.4 15.4-19.4 25.1-42.2 35.7L85 282.2c22.8-10.6 33.8-19.4 40.8-33.3 7.2-14.2 9.8-30.8 9.8-74.2V82.9zm36.7-53.3v36.8h-36.7V29.6h36.7z" fill="#092E20"/>'
    ),
    # Django REST Framework
    'django rest framework': (
        '0 0 256 256',
        '<rect width="256" height="256" rx="40" fill="#A30000"/><text x="128" y="105" text-anchor="middle" fill="#FFFFFF" font-family="monospace, sans-serif" font-weight="900" font-size="64">REST</text><path d="M48 140h160v6h-160zM48 160h110v6h-110zM48 180h140v6h-140z" fill="#FFFFFF" opacity="0.85"/>'
    ),
    'drf': (
        '0 0 256 256',
        '<rect width="256" height="256" rx="40" fill="#A30000"/><text x="128" y="105" text-anchor="middle" fill="#FFFFFF" font-family="monospace, sans-serif" font-weight="900" font-size="64">REST</text><path d="M48 140h160v6h-160zM48 160h110v6h-110zM48 180h140v6h-140z" fill="#FFFFFF" opacity="0.85"/>'
    ),
    # Next.js - Official Dark Badge
    'next.js': (
        '0 0 128 128',
        '<circle cx="64" cy="64" r="64" fill="#000"/><path d="M89.7 94.6L44.8 37.3H37v53.4h7.5V50l41.6 53.2c1.2-.8 2.4-1.7 3.6-2.6zM83.4 37.3h7.5v32.5l-7.5-9.6V37.3z" fill="#FFF"/>'
    ),
    'nextjs': (
        '0 0 128 128',
        '<circle cx="64" cy="64" r="64" fill="#000"/><path d="M89.7 94.6L44.8 37.3H37v53.4h7.5V50l41.6 53.2c1.2-.8 2.4-1.7 3.6-2.6zM83.4 37.3h7.5v32.5l-7.5-9.6V37.3z" fill="#FFF"/>'
    ),
    # JavaScript
    'javascript': (
        '0 0 630 630',
        '<rect width="630" height="630" fill="#F7DF1E"/><path d="M423.2 492.2c12.7 20.7 29.2 36.1 58.4 36.1 24.5 0 40.2-12.3 40.2-29.2 0-20.3-16.1-27.5-43.1-39.3l-14.8-6.3c-42.7-18.2-71.2-41-71.2-89.2 0-44.4 33.8-78.2 86.6-78.2 37.6 0 64.6 13.1 84 47.3l-46 29.5c-10.1-18.2-21-25.4-38-25.4-17.3 0-28.3 11-28.3 25.4 0 17.7 11 25 36.4 35.9l14.8 6.3c50.3 21.6 78.9 43.6 78.9 93.1 0 53.3-41.9 82.5-98.3 82.5-55.1 0-90.7-26.2-108.1-60.6l48.5-27.9zm-223.4 5.3c9.3 16.5 17.7 30.5 38.1 30.5 19.5 0 31.7-7.6 31.7-37.2V294.6h60v197.8c0 61.2-35.9 89.1-88.2 89.1-47.3 0-74.8-24.5-88.7-54l47.1-30z" fill="#000"/>'
    ),
    'js': (
        '0 0 630 630',
        '<rect width="630" height="630" fill="#F7DF1E"/><path d="M423.2 492.2c12.7 20.7 29.2 36.1 58.4 36.1 24.5 0 40.2-12.3 40.2-29.2 0-20.3-16.1-27.5-43.1-39.3l-14.8-6.3c-42.7-18.2-71.2-41-71.2-89.2 0-44.4 33.8-78.2 86.6-78.2 37.6 0 64.6 13.1 84 47.3l-46 29.5c-10.1-18.2-21-25.4-38-25.4-17.3 0-28.3 11-28.3 25.4 0 17.7 11 25 36.4 35.9l14.8 6.3c50.3 21.6 78.9 43.6 78.9 93.1 0 53.3-41.9 82.5-98.3 82.5-55.1 0-90.7-26.2-108.1-60.6l48.5-27.9zm-223.4 5.3c9.3 16.5 17.7 30.5 38.1 30.5 19.5 0 31.7-7.6 31.7-37.2V294.6h60v197.8c0 61.2-35.9 89.1-88.2 89.1-47.3 0-74.8-24.5-88.7-54l47.1-30z" fill="#000"/>'
    ),
    # HTML5
    'html': (
        '0 0 512 512',
        '<path d="M71 460L30 0h452l-41 460-185 52z" fill="#E34F26"/><path d="M256 472l149-41 35-391H256z" fill="#EF652A"/><path d="M256 208h-74l-5-58h79V94H114l16 172h126zm0 148l-65-18-4-47h-56l7 89 118 33z" fill="#EBEBEB"/><path d="M256 208h74l-7 78-67 18v57l118-33 16-178H256zm0-114v56h142l5-56z" fill="#FFF"/>'
    ),
    'html5': (
        '0 0 512 512',
        '<path d="M71 460L30 0h452l-41 460-185 52z" fill="#E34F26"/><path d="M256 472l149-41 35-391H256z" fill="#EF652A"/><path d="M256 208h-74l-5-58h79V94H114l16 172h126zm0 148l-65-18-4-47h-56l7 89 118 33z" fill="#EBEBEB"/><path d="M256 208h74l-7 78-67 18v57l118-33 16-178H256zm0-114v56h142l5-56z" fill="#FFF"/>'
    ),
    # CSS3
    'css': (
        '0 0 512 512',
        '<path d="M71 460L30 0h452l-41 460-185 52z" fill="#1572B6"/><path d="M256 472l149-41 35-391H256z" fill="#33A9DC"/><path d="M256 208h-74l-5-58h79V94H114l16 172h126zm0 148l-65-18-4-47h-56l7 89 118 33z" fill="#EBEBEB"/><path d="M256 208h74l-7 78-67 18v57l118-33 16-178H256zm0-114v56h142l5-56z" fill="#FFF"/>'
    ),
    'css3': (
        '0 0 512 512',
        '<path d="M71 460L30 0h452l-41 460-185 52z" fill="#1572B6"/><path d="M256 472l149-41 35-391H256z" fill="#33A9DC"/><path d="M256 208h-74l-5-58h79V94H114l16 172h126zm0 148l-65-18-4-47h-56l7 89 118 33z" fill="#EBEBEB"/><path d="M256 208h74l-7 78-67 18v57l118-33 16-178H256zm0-114v56h142l5-56z" fill="#FFF"/>'
    ),
    # PostgreSQL - Official Elephant Logo
    'postgresql': (
        '0 0 256 256',
        '<path d="M128 12c-63.5 0-115 51.5-115 115 0 35 15.6 66.4 40.3 87.4 3.7-18.7 13.9-46.5 35.8-63.9-3.7-5.9-6-12.8-6-20.2 0-21.6 17.5-39.1 39.1-39.1 2.3 0 4.6.2 6.8.6 4.3-15.5 18.6-26.9 35.5-26.9 20.3 0 36.7 16.4 36.7 36.7 0 1.2-.1 2.4-.2 3.6 18.5 7.6 31.5 25.8 31.5 47 0 17.5-9 32.9-22.6 41.9 19.5-16.7 31.9-41.5 31.9-69.1 0-63.5-51.5-115-113.8-115z" fill="#336791"/><path d="M138 238c35.6-5.8 66.2-26.5 84.4-56.1-5.1-4.2-11.7-6.9-19-6.9-10.4 0-19.4 5.4-24.5 13.5-6.7 10.6-18.3 17.7-31.5 17.7-3.2 0-6.3-.4-9.4-1.2v33z" fill="#336791"/>'
    ),
    # MySQL - Official Dolphin
    'mysql': (
        '0 0 256 256',
        '<path d="M128 16c-61.9 0-112 50.1-112 112 0 48.7 31 90.1 74.4 105.4-1.6-9.1-1.3-19.9 2-29.4 6.8-19.7 23.3-33.3 42.4-38.6 17.4-4.8 35.2-1.7 48.9 8.2 12.3 8.9 19.6 22.8 20.3 38.1 19.9-17.7 32-43.3 32-71.7 0-61.9-50.1-112-108-112z" fill="#00758F"/><path d="M172 174c-12-14-31-18-48-13-17 5-30 18-36 34-3 9-3 18-1 27 13 4 27 6 41 6 15 0 29-2 42-7-1-16-7-33-18-47z" fill="#F29111"/>'
    ),
    # Scikit-learn
    'scikit-learn': (
        '0 0 256 256',
        '<rect width="256" height="256" rx="40" fill="#F7931E" opacity="0.12"/><path d="M80 60h40l60 68-60 68H80l60-68z" fill="#035586"/><circle cx="160" cy="128" r="28" fill="#F7931E"/><path d="M130 94l50 34-50 34z" fill="#3894C9"/>'
    ),
    # Pandas
    'pandas': (
        '0 0 256 256',
        '<rect width="256" height="256" rx="40" fill="#150458" opacity="0.12"/><rect x="58" y="40" width="30" height="176" rx="8" fill="#150458"/><rect x="168" y="40" width="30" height="176" rx="8" fill="#E70488"/><rect x="58" y="105" width="140" height="46" rx="8" fill="#FFD43B"/>'
    ),
    # NumPy
    'numpy': (
        '0 0 256 256',
        '<rect width="256" height="256" rx="40" fill="#013243" opacity="0.15"/><path d="M128 32l84 48v96l-84 48-84-48V80z" fill="#4DABCF" opacity="0.25" stroke="#4DABCF" stroke-width="8"/><path d="M92 86v84l36-52v52h24V86l-36 52V86z" fill="#013243" stroke="#4DABCF" stroke-width="4"/>'
    ),
    # Matplotlib
    'matplotlib': (
        '0 0 256 256',
        '<rect width="256" height="256" rx="40" fill="#11557C" opacity="0.15"/><path d="M38 200h180M38 200V56" stroke="#11557C" stroke-width="12" stroke-linecap="round"/><path d="M56 170l40-60 40 40 40-70 40 30" fill="none" stroke="#FF6F00" stroke-width="14" stroke-linecap="round" stroke-linejoin="round"/><circle cx="96" cy="110" r="10" fill="#11557C"/><circle cx="136" cy="150" r="10" fill="#11557C"/><circle cx="176" cy="80" r="10" fill="#11557C"/>'
    ),
    # NLP / Machine Learning
    'nlp': (
        '0 0 256 256',
        '<rect width="256" height="256" rx="40" fill="#7C3AED" opacity="0.15"/><circle cx="64" cy="80" r="16" fill="#00F3FF"/><circle cx="64" cy="176" r="16" fill="#00F3FF"/><circle cx="128" cy="128" r="20" fill="#7C3AED"/><circle cx="192" cy="80" r="16" fill="#A855F7"/><circle cx="192" cy="176" r="16" fill="#A855F7"/><path d="M64 80l64 48M64 176l64-48M128 128l64-48M128 128l64 48M64 80l128 0M64 176l128 0" stroke="#00F3FF" stroke-width="6" opacity="0.65"/>'
    ),
    'machine learning': (
        '0 0 256 256',
        '<rect width="256" height="256" rx="40" fill="#7C3AED" opacity="0.15"/><circle cx="64" cy="80" r="16" fill="#00F3FF"/><circle cx="64" cy="176" r="16" fill="#00F3FF"/><circle cx="128" cy="128" r="20" fill="#7C3AED"/><circle cx="192" cy="80" r="16" fill="#A855F7"/><circle cx="192" cy="176" r="16" fill="#A855F7"/><path d="M64 80l64 48M64 176l64-48M128 128l64-48M128 128l64 48M64 80l128 0M64 176l128 0" stroke="#00F3FF" stroke-width="6" opacity="0.65"/>'
    ),
    # OpenRouter API / AI
    'openrouter api': (
        '0 0 256 256',
        '<rect width="256" height="256" rx="40" fill="#6366F1" opacity="0.18"/><path d="M128 48L208 94V162L128 208L48 162V94L128 48Z" fill="none" stroke="#6366F1" stroke-width="12" stroke-linejoin="round"/><circle cx="128" cy="128" r="28" fill="#6366F1"/><circle cx="128" cy="48" r="12" fill="#A5B4FC"/><circle cx="208" cy="94" r="12" fill="#A5B4FC"/><circle cx="208" cy="162" r="12" fill="#A5B4FC"/><circle cx="128" cy="208" r="12" fill="#A5B4FC"/><circle cx="48" cy="162" r="12" fill="#A5B4FC"/><circle cx="48" cy="94" r="12" fill="#A5B4FC"/>'
    ),
    'openrouter': (
        '0 0 256 256',
        '<rect width="256" height="256" rx="40" fill="#6366F1" opacity="0.18"/><path d="M128 48L208 94V162L128 208L48 162V94L128 48Z" fill="none" stroke="#6366F1" stroke-width="12" stroke-linejoin="round"/><circle cx="128" cy="128" r="28" fill="#6366F1"/><circle cx="128" cy="48" r="12" fill="#A5B4FC"/><circle cx="208" cy="94" r="12" fill="#A5B4FC"/><circle cx="208" cy="162" r="12" fill="#A5B4FC"/><circle cx="128" cy="208" r="12" fill="#A5B4FC"/><circle cx="48" cy="162" r="12" fill="#A5B4FC"/><circle cx="48" cy="94" r="12" fill="#A5B4FC"/>'
    ),
    # AWS Cloud / AWS - Official AWS smile + letters
    'aws cloud': (
        '0 0 256 256',
        '<path d="M78.6 133.4c0-7.8 5.6-13 14.8-13 5.4 0 10.4 1.8 14.4 4.8v-17c-4.4-2.2-10-3.4-16.2-3.4-18.4 0-30.8 11.2-30.8 28.2 0 24.8 29.8 20.6 29.8 30.6 0 8.4-6.4 13.8-16.4 13.8-6.6 0-13-2.6-18-7.2l-9.2 12.6c6.6 6.4 16.4 9.8 26.6 9.8 20.8 0 34.6-11.8 34.6-29 0-25.2-29.6-21.2-29.6-30.2zm58.2-46.6h17.6l24.4 75.8 22.8-75.8h17.6l23 75.8 24.6-75.8h17.8l-32.8 98.4h-18l-23.4-74.6-23.4 74.6h-18.2l-32-98.4z" fill="#232F3E"/><path d="M48.2 212.8c66.4 34.8 146.4 20.2 188.8-12.8 4.2-3.2 2.2-7.8-3-5-44.8 23.4-122.2 30-181.8-8-5-3.2-9 1.4-4 5.8z" fill="#FF9900"/><path d="M242.4 191.6c-4.4-6-29.4-4.4-36.2-3.2-3.4.6-3.8 3.8-.8 5.8 19 12.8 34.8 8.8 38.6 3.6 1.4-1.8 1.8-4.2-1.6-6.2z" fill="#FF9900"/>'
    ),
    'aws': (
        '0 0 256 256',
        '<path d="M78.6 133.4c0-7.8 5.6-13 14.8-13 5.4 0 10.4 1.8 14.4 4.8v-17c-4.4-2.2-10-3.4-16.2-3.4-18.4 0-30.8 11.2-30.8 28.2 0 24.8 29.8 20.6 29.8 30.6 0 8.4-6.4 13.8-16.4 13.8-6.6 0-13-2.6-18-7.2l-9.2 12.6c6.6 6.4 16.4 9.8 26.6 9.8 20.8 0 34.6-11.8 34.6-29 0-25.2-29.6-21.2-29.6-30.2zm58.2-46.6h17.6l24.4 75.8 22.8-75.8h17.6l23 75.8 24.6-75.8h17.8l-32.8 98.4h-18l-23.4-74.6-23.4 74.6h-18.2l-32-98.4z" fill="#FF9900"/><path d="M48.2 212.8c66.4 34.8 146.4 20.2 188.8-12.8 4.2-3.2 2.2-7.8-3-5-44.8 23.4-122.2 30-181.8-8-5-3.2-9 1.4-4 5.8z" fill="#FF9900"/><path d="M242.4 191.6c-4.4-6-29.4-4.4-36.2-3.2-3.4.6-3.8 3.8-.8 5.8 19 12.8 34.8 8.8 38.6 3.6 1.4-1.8 1.8-4.2-1.6-6.2z" fill="#FF9900"/>'
    ),
    # Git / GitHub
    'git / github': (
        '0 0 256 256',
        '<path d="M128 2C57.3 2 0 59.3 0 130c0 56.6 36.7 104.6 87.5 121.5 6.4 1.2 8.7-2.8 8.7-6.2v-21.6c-35.6 7.7-43.1-17.2-43.1-17.2-5.8-14.8-14.2-18.7-14.2-18.7-11.6-7.9.9-7.8.9-7.8 12.8.9 19.6 13.2 19.6 13.2 11.4 19.6 30 13.9 37.3 10.6 1.2-8.3 4.5-13.9 8.2-17.1-28.4-3.2-58.3-14.2-58.3-63.3 0-14 5-25.4 13.2-34.4-1.3-3.2-5.7-16.3 1.3-33.9 0 0 10.8-3.5 35.3 13.2 10.2-2.8 21.2-4.3 32.2-4.3 10.9 0 22 1.4 32.2 4.3 24.5-16.7 35.2-13.2 35.2-13.2 7 17.6 2.6 30.7 1.3 33.9 8.2 9 13.2 20.4 13.2 34.4 0 49.2-30 60-58.5 63.2 4.6 4 8.7 11.8 8.7 23.7v35.1c0 3.4 2.3 7.5 8.8 6.2C219.4 234.5 256 186.5 256 130 256 59.3 198.7 2 128 2z" fill="#F05032"/>'
    ),
    'git': (
        '0 0 256 256',
        '<path d="M240.6 116.8L139.2 15.4c-8.5-8.5-22.3-8.5-30.8 0L87.8 36.1l32.2 32.2c8.8-3 19.2-.9 26 5.9 6.8 6.8 8.9 17.2 5.9 26l31.1 31.1c8.8-3 19.2-.9 26 5.9 9.6 9.6 9.6 25.1 0 34.7s-25.1 9.6-34.7 0c-7.3-7.3-9.2-18.4-5.5-27.7l-29-29v76.2c2.4 1.2 4.7 2.9 6.6 4.8 9.6 9.6 9.6 25.1 0 34.7s-25.1 9.6-34.7 0-9.6-25.1 0-34.7c2.5-2.5 5.6-4.3 8.9-5.3V82.8c-3.3-1-6.4-2.8-8.9-5.3-7.2-7.2-9.1-18.1-5.6-27.3L72.2 20.6 15.4 77.4c-8.5 8.5-8.5 22.3 0 30.8l101.4 101.4c8.5 8.5 22.3 8.5 30.8 0l93-93c8.5-8.5 8.5-22.3 0-30.8z" fill="#F05032"/>'
    ),
    'github': (
        '0 0 256 256',
        '<path d="M128 2C57.3 2 0 59.3 0 130c0 56.6 36.7 104.6 87.5 121.5 6.4 1.2 8.7-2.8 8.7-6.2v-21.6c-35.6 7.7-43.1-17.2-43.1-17.2-5.8-14.8-14.2-18.7-14.2-18.7-11.6-7.9.9-7.8.9-7.8 12.8.9 19.6 13.2 19.6 13.2 11.4 19.6 30 13.9 37.3 10.6 1.2-8.3 4.5-13.9 8.2-17.1-28.4-3.2-58.3-14.2-58.3-63.3 0-14 5-25.4 13.2-34.4-1.3-3.2-5.7-16.3 1.3-33.9 0 0 10.8-3.5 35.3 13.2 10.2-2.8 21.2-4.3 32.2-4.3 10.9 0 22 1.4 32.2 4.3 24.5-16.7 35.2-13.2 35.2-13.2 7 17.6 2.6 30.7 1.3 33.9 8.2 9 13.2 20.4 13.2 34.4 0 49.2-30 60-58.5 63.2 4.6 4 8.7 11.8 8.7 23.7v35.1c0 3.4 2.3 7.5 8.8 6.2C219.4 234.5 256 186.5 256 130 256 59.3 198.7 2 128 2z" fill="#FFFFFF"/>'
    ),
    # SQL / Database
    'sql': (
        '0 0 256 256',
        '<rect width="256" height="256" rx="40" fill="#00758F" opacity="0.15"/><ellipse cx="128" cy="64" rx="72" ry="24" fill="#00758F" opacity="0.4" stroke="#00F3FF" stroke-width="8"/><path d="M56 64v64c0 13.3 32.2 24 72 24s72-10.7 72-24V64" fill="none" stroke="#00F3FF" stroke-width="8"/><path d="M56 128v64c0 13.3 32.2 24 72 24s72-10.7 72-24v-64" fill="none" stroke="#00F3FF" stroke-width="8"/>'
    ),
    # Google OAuth
    'google oauth': (
        '0 0 256 256',
        '<path d="M225.4 130.8c0-7.7-.7-15.1-2-22.2H128v42h54.7c-2.4 12.8-9.6 23.6-20.4 30.9v25.7h33c19.3-17.8 30.1-44 30.1-76.4z" fill="#4285F4"/><path d="M128 230c27.6 0 50.7-9.1 67.6-24.8l-33-25.7c-9.1 6.1-20.8 9.8-34.6 9.8-26.6 0-49.2-18-57.2-42.1H36.3v26.5C53.3 207.6 88.1 230 128 230z" fill="#34A853"/><path d="M70.8 147.2c-2-6.1-3.2-12.6-3.2-19.2s1.1-13.1 3.2-19.2V82.3H36.3C29.3 96.2 25.3 111.7 25.3 128s4 31.8 11 45.7l34.5-26.5z" fill="#FBBC05"/><path d="M128 67.8c15 0 28.5 5.2 39.1 15.3l29.3-29.3C178.6 37.1 155.5 26 128 26 88.1 26 53.3 48.4 36.3 82.3l34.5 26.5c8-24.1 30.6-41 57.2-41z" fill="#EA4335"/>'
    ),
    'google': (
        '0 0 256 256',
        '<path d="M225.4 130.8c0-7.7-.7-15.1-2-22.2H128v42h54.7c-2.4 12.8-9.6 23.6-20.4 30.9v25.7h33c19.3-17.8 30.1-44 30.1-76.4z" fill="#4285F4"/><path d="M128 230c27.6 0 50.7-9.1 67.6-24.8l-33-25.7c-9.1 6.1-20.8 9.8-34.6 9.8-26.6 0-49.2-18-57.2-42.1H36.3v26.5C53.3 207.6 88.1 230 128 230z" fill="#34A853"/><path d="M70.8 147.2c-2-6.1-3.2-12.6-3.2-19.2s1.1-13.1 3.2-19.2V82.3H36.3C29.3 96.2 25.3 111.7 25.3 128s4 31.8 11 45.7l34.5-26.5z" fill="#FBBC05"/><path d="M128 67.8c15 0 28.5 5.2 39.1 15.3l29.3-29.3C178.6 37.1 155.5 26 128 26 88.1 26 53.3 48.4 36.3 82.3l34.5 26.5c8-24.1 30.6-41 57.2-41z" fill="#EA4335"/>'
    ),
    # ReportLab / PDF
    'reportlab': (
        '0 0 256 256',
        '<rect width="256" height="256" rx="40" fill="#E11D48" opacity="0.15"/><path d="M64 48h88l48 48v112H64z" fill="#E11D48" opacity="0.25" stroke="#E11D48" stroke-width="8"/><path d="M152 48v48h48" fill="none" stroke="#E11D48" stroke-width="8"/><text x="128" y="165" text-anchor="middle" fill="#FFFFFF" font-family="monospace, sans-serif" font-weight="bold" font-size="36">PDF</text>'
    ),
    # Tailwind CSS
    'tailwind': (
        '0 0 256 256',
        '<path d="M128 56c-35.2 0-57.6 17.6-66.4 52.8 13.6-17.6 28.8-24 46.4-20 10.4 2.4 17.6 10.4 25.6 18.4 12.8 13.6 28 28.8 60.8 28.8 35.2 0 57.6-17.6 66.4-52.8-13.6 17.6-28.8 24-46.4 20-10.4-2.4-17.6-10.4-25.6-18.4-12.8-13.6-28-28.8-60.8-28.8zM61.6 136c-35.2 0-57.6 17.6-66.4 52.8 13.6-17.6 28.8-24 46.4-20 10.4 2.4 17.6 10.4 25.6 18.4 12.8 13.6 28 28.8 60.8 28.8 35.2 0 57.6-17.6 66.4-52.8-13.6 17.6-28.8 24-46.4 20-10.4-2.4-17.6-10.4-25.6-18.4-12.8-13.6-28-28.8-60.8-28.8z" fill="#38BDF8"/>'
    ),
    'tailwind css': (
        '0 0 256 256',
        '<path d="M128 56c-35.2 0-57.6 17.6-66.4 52.8 13.6-17.6 28.8-24 46.4-20 10.4 2.4 17.6 10.4 25.6 18.4 12.8 13.6 28 28.8 60.8 28.8 35.2 0 57.6-17.6 66.4-52.8-13.6 17.6-28.8 24-46.4 20-10.4-2.4-17.6-10.4-25.6-18.4-12.8-13.6-28-28.8-60.8-28.8zM61.6 136c-35.2 0-57.6 17.6-66.4 52.8 13.6-17.6 28.8-24 46.4-20 10.4 2.4 17.6 10.4 25.6 18.4 12.8 13.6 28 28.8 60.8 28.8 35.2 0 57.6-17.6 66.4-52.8-13.6 17.6-28.8 24-46.4 20-10.4-2.4-17.6-10.4-25.6-18.4-12.8-13.6-28-28.8-60.8-28.8z" fill="#38BDF8"/>'
    ),
    # React
    'react': (
        '0 0 256 256',
        '<circle cx="128" cy="128" r="24.6" fill="#61DAFB"/><g stroke="#61DAFB" stroke-width="9.6" fill="none"><ellipse rx="88" ry="33.6" cx="128" cy="128"/><ellipse rx="88" ry="33.6" cx="128" cy="128" transform="rotate(60 128 128)"/><ellipse rx="88" ry="33.6" cx="128" cy="128" transform="rotate(120 128 128)"/></g>'
    ),
}


@register.simple_tag
def tech_logo(name, color='#a78bfa', size=22):
    if not name:
        return ''
    key = name.lower().strip()
    entry = _LOGOS.get(key)

    # Try alternate fuzzy lookup if direct match fails
    if not entry:
        if 'python' in key:
            entry = _LOGOS.get('python')
        elif 'django rest' in key or 'drf' in key:
            entry = _LOGOS.get('django rest framework')
        elif 'django' in key:
            entry = _LOGOS.get('django')
        elif 'next' in key:
            entry = _LOGOS.get('next.js')
        elif 'react' in key:
            entry = _LOGOS.get('react')
        elif 'javascript' in key or 'js' in key:
            entry = _LOGOS.get('javascript')
        elif 'html' in key:
            entry = _LOGOS.get('html5')
        elif 'css' in key:
            entry = _LOGOS.get('css3')
        elif 'postgres' in key:
            entry = _LOGOS.get('postgresql')
        elif 'mysql' in key:
            entry = _LOGOS.get('mysql')
        elif 'sql' in key:
            entry = _LOGOS.get('sql')
        elif 'scikit' in key:
            entry = _LOGOS.get('scikit-learn')
        elif 'pandas' in key:
            entry = _LOGOS.get('pandas')
        elif 'numpy' in key:
            entry = _LOGOS.get('numpy')
        elif 'matplotlib' in key:
            entry = _LOGOS.get('matplotlib')
        elif 'nlp' in key or 'natural language' in key:
            entry = _LOGOS.get('nlp')
        elif 'openrouter' in key:
            entry = _LOGOS.get('openrouter api')
        elif 'aws' in key or 'cloud' in key:
            entry = _LOGOS.get('aws cloud')
        elif 'git' in key or 'github' in key:
            entry = _LOGOS.get('git / github')
        elif 'google' in key or 'oauth' in key:
            entry = _LOGOS.get('google oauth')
        elif 'reportlab' in key or 'pdf' in key:
            entry = _LOGOS.get('reportlab')
        elif 'tailwind' in key:
            entry = _LOGOS.get('tailwind')

    if entry:
        viewbox, paths = entry
        svg = (
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{viewbox}" '
            f'width="{size}" height="{size}" aria-hidden="true" focusable="false" '
            f'style="flex-shrink:0;vertical-align:middle;filter:drop-shadow(0 2px 4px rgba(0,0,0,0.4));">{paths}</svg>'
        )
        return mark_safe(svg)

    # Fallback: stylish glowing indicator
    return mark_safe(
        f'<span style="display:inline-block;width:{size}px;height:{size}px;'
        f'border-radius:50%;background:{color};'
        f'box-shadow:0 0 8px {color};flex-shrink:0;" aria-hidden="true"></span>'
    )
