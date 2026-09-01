// Home page: typing animation + modern contact form AJAX
(function() {
  // Hero typing animation
  const nameEl = document.getElementById('hero-name');
  const roleEl = document.getElementById('hero-role');
  const rolesData = window.HERO_ROLES || ['Fresher Software Developer', 'Python Developer', 'Django Developer', 'AI & ML Enthusiast', 'Full-Stack Developer'];

  const NAME = 'Nagasrinivas Govvala';
  let charIndex = 0;
  let roleIndex = 0;
  let roleCharIndex = 0;
  let phase = 'name';
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
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      nameEl.textContent = NAME;
      if (roleEl) roleEl.textContent = rolesData[0];
    } else {
      typeName();
    }
  }

  // Modern Contact Form Logic
  const contactForm = document.getElementById('contact-form');
  const contactFeedback = document.getElementById('contact-feedback');
  const contactBtnText = document.getElementById('contact-btn-text');
  const contactSubmit = document.getElementById('contact-submit');

  if (contactForm) {
    contactForm.addEventListener('submit', async (e) => {
      e.preventDefault();

      const nameInput = document.getElementById('id_name');
      const emailInput = document.getElementById('id_email');
      const subjectInput = document.getElementById('id_subject');
      const messageInput = document.getElementById('id_message');

      const name = nameInput ? nameInput.value.trim() : '';
      const email = emailInput ? emailInput.value.trim() : '';
      const subject = subjectInput ? subjectInput.value.trim() : '';
      const message = messageInput ? messageInput.value.trim() : '';

      // Client-side validation
      if (!name || name.length < 2) {
        showFeedback('Please enter your name (at least 2 characters).', 'error');
        if (nameInput) nameInput.focus();
        return;
      }

      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!email || !emailRegex.test(email)) {
        showFeedback('Please enter a valid email address.', 'error');
        if (emailInput) emailInput.focus();
        return;
      }

      if (!subject) {
        showFeedback('Please enter a subject.', 'error');
        if (subjectInput) subjectInput.focus();
        return;
      }

      if (!message || message.length < 5) {
        showFeedback('Please write a message (at least 5 characters).', 'error');
        if (messageInput) messageInput.focus();
        return;
      }

      // UI Loading state
      if (contactSubmit) contactSubmit.disabled = true;
      if (contactBtnText) contactBtnText.textContent = 'Sending Message...';
      showFeedback('Sending your message, please wait...', 'info');

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

        if (res.ok && data.success) {
          showFeedback(data.message || "Thank you for reaching out! I'll get back to you shortly.", 'success');
          contactForm.reset();
        } else {
          showFeedback(data.error || 'Something went wrong. Please check your inputs.', 'error');
        }
      } catch (err) {
        showFeedback('Network error. Please try again or send an email directly to srinivasgovvala128@gmail.com.', 'error');
      } finally {
        if (contactSubmit) contactSubmit.disabled = false;
        if (contactBtnText) contactBtnText.textContent = 'Send Message';
      }
    });
  }

  function showFeedback(msg, type) {
    if (!contactFeedback) return;
    contactFeedback.textContent = msg;
    contactFeedback.className = `form-feedback ${type}`;
    if (type === 'success') {
      contactFeedback.style.color = '#38ef7d';
    } else if (type === 'error') {
      contactFeedback.style.color = '#ff6584';
    } else {
      contactFeedback.style.color = '#a78bfa';
    }
  }
})();
