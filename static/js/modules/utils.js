// Utility helpers
const $ = (sel, ctx = document) => ctx.querySelector(sel);
const $$ = (sel, ctx = document) => [...ctx.querySelectorAll(sel)];

function debounce(fn, ms = 150) {
  let timer;
  return (...args) => { clearTimeout(timer); timer = setTimeout(() => fn(...args), ms); };
}

function throttle(fn, ms = 100) {
  let last = 0;
  return (...args) => {
    const now = Date.now();
    if (now - last >= ms) { last = now; fn(...args); }
  };
}

function getCookie(name) {
  const match = document.cookie.match(new RegExp('(?:^|; )' + name + '=([^;]*)'));
  return match ? decodeURIComponent(match[1]) : null;
}

function getCsrfToken() {
  if (window.CSRF_TOKEN && typeof window.CSRF_TOKEN === 'string' && window.CSRF_TOKEN.length >= 32) {
    return window.CSRF_TOKEN;
  }
  const meta = document.querySelector('meta[name="csrf-token"]');
  if (meta && meta.content && meta.content.length >= 32) {
    return meta.content;
  }
  const input = document.querySelector('[name=csrfmiddlewaretoken]');
  if (input && input.value && input.value.length >= 32) {
    return input.value;
  }
  const cookie = getCookie('csrftoken');
  if (cookie && cookie.length >= 32) {
    return cookie;
  }
  return null;
}

// Intersection Observer for reveal animations
const revealObserver = new IntersectionObserver(
  (entries) => entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('visible'); revealObserver.unobserve(e.target); } }),
  { threshold: 0.1, rootMargin: '0px 0px -50px 0px' }
);

document.addEventListener('DOMContentLoaded', () => {
  $$('.reveal').forEach(el => revealObserver.observe(el));
});

window.Utils = { $, $$, debounce, throttle, getCookie, getCsrfToken };
