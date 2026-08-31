// Home page: typing animation + contact form AJAX
(function() {
  // Hero typing animation
  const nameEl = document.getElementById('hero-name');
  const roleEl = document.getElementById('hero-role');
  const rolesData = window.HERO_ROLES || ['Fresher Software Developer', 'Python Developer', 'Django Developer', 'AI & ML Enthusiast', 'Full-Stack Developer'];

  const NAME = 'Nagasrinivas Govvala';
  let charIndex = 0;
  let roleIndex = 0;
  let roleCharIndex = 0;
  let phase = 'name'; // name -> pause -> role -> delete -> next
  let timeoutId = null;

  function typeName() {
    if (charIndex <= NAME.length) {
      if (nameEl) nameEl.textContent = NAME.slice(0, charIndex);
      charIndex++;
      timeoutId = setTimeout(typeName, charIndex < 5 ? 120 : 70);
    } else {
      setTimeout(startRole, 500);
    }
  }

  function startRole() {
    phase = 'type-role';
    typeRole();
  }

  function typeRole() {
    const role = rolesData[roleIndex % rolesData.length];
    if (roleCharIndex <= role.length) {
      if (roleEl) roleEl.textContent = role.slice(0, roleCharIndex);
      roleCharIndex++;
      timeoutId = setTimeout(typeRole, 60);
    } else {
      setTimeout(deleteRole, 2500);
    }
  }

  function deleteRole() {
    const role = rolesData[roleIndex % rolesData.length];
    if (roleCharIndex >= 0) {
      if (roleEl) roleEl.textContent = role.slice(0, roleCharIndex);
      roleCharIndex--;
      timeoutId = setTimeout(deleteRole, 35);
    } else {
      roleIndex++;
      roleCharIndex = 0;
      setTimeout(startRole, 300);
    }
  }

  if (nameEl) {
    // Respect reduced motion
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      nameEl.textContent = NAME;
      if (roleEl) roleEl.textContent = rolesData[0];
    } else {
      typeName();
    }
  }

  // Contact form AJAX
  const contactForm = document.getElementById('contact-form');
  const contactFeedback = document.getElementById('contact-feedback');
  const contactBtnText = document.getElementById('contact-btn-text');
  const contactSubmit = document.getElementById('contact-submit');

  if (contactForm) {
    contactForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      if (contactSubmit) contactSubmit.disabled = true;
      if (contactBtnText) contactBtnText.textContent = 'Sending...';
      if (contactFeedback) { contactFeedback.textContent = ''; contactFeedback.className = 'form-feedback'; }

      const formData = new FormData(contactForm);
      const csrf = (window.Utils && typeof window.Utils.getCsrfToken === 'function')
        ? window.Utils.getCsrfToken()
        : (window.CSRF_TOKEN || document.querySelector('#contact-form [name=csrfmiddlewaretoken]')?.value);

      const headers = {};
      if (csrf) {
        headers['X-CSRFToken'] = csrf;
      }

      try {
        const res = await fetch('/contact/send/', {
          method: 'POST',
          headers: headers,
          body: formData,
        });
        const data = await res.json();
        if (data.success) {
          contactFeedback.textContent = data.message || "Thanks! I'll get back to you soon.";
          contactFeedback.className = 'form-feedback success';
          contactForm.reset();
        } else {
          contactFeedback.textContent = data.error || 'Something went wrong. Please try again.';
          contactFeedback.className = 'form-feedback error';
        }
      } catch (_) {
        if (contactFeedback) {
          contactFeedback.textContent = 'Network error. Please try again or send an email directly.';
          contactFeedback.className = 'form-feedback error';
        }
      } finally {
        if (contactSubmit) contactSubmit.disabled = false;
        if (contactBtnText) contactBtnText.textContent = 'Send Message';
      }
    });
  }
})();
