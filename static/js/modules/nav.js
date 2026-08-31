// Navigation behavior
(function() {
  const nav = document.getElementById('main-nav');
  const hamburger = document.getElementById('hamburger');
  const mobileMenu = document.getElementById('mobileMenu');
  const mobileClose = document.getElementById('mobileMenuClose');

  // Scroll behavior
  const onScroll = window.Utils ? window.Utils.throttle(() => {
    nav.classList.toggle('scrolled', window.scrollY > 60);
  }, 80) : () => { nav.classList.toggle('scrolled', window.scrollY > 60); };

  window.addEventListener('scroll', onScroll, { passive: true });

  // Active link on scroll
  const sections = [['#about','about'],['#skills','skills'],['#projects','projects'],['#future','future'],['#education','education'],['#contact','contact']];
  const navLinks = document.querySelectorAll('.nav-links a');

  function updateActiveLink() {
    const scrollY = window.scrollY + 120;
    let current = '';
    sections.forEach(([id]) => {
      const el = document.querySelector(id);
      if (el && el.offsetTop <= scrollY) current = id.slice(1);
    });
    navLinks.forEach(a => {
      const href = a.getAttribute('href');
      a.classList.toggle('active', href && href.includes(current) && current !== '');
    });
  }
  window.addEventListener('scroll', updateActiveLink, { passive: true });

  // Hamburger / mobile menu
  function openMenu() {
    hamburger.classList.add('open');
    mobileMenu.classList.add('open');
    hamburger.setAttribute('aria-expanded', 'true');
    mobileMenu.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
  }
  function closeMenu() {
    hamburger.classList.remove('open');
    mobileMenu.classList.remove('open');
    hamburger.setAttribute('aria-expanded', 'false');
    mobileMenu.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
  }

  if (hamburger) hamburger.addEventListener('click', openMenu);
  if (mobileClose) mobileClose.addEventListener('click', closeMenu);
  document.querySelectorAll('.mobile-nav-link').forEach(a => a.addEventListener('click', closeMenu));

  // AI toggle
  const aiToggle = document.getElementById('aiToggleNav');
  if (aiToggle) {
    aiToggle.addEventListener('click', () => {
      const panel = document.getElementById('chatbot-panel');
      if (panel) {
        panel.hidden = !panel.hidden;
        panel.removeAttribute('hidden') || (panel.hidden = false);
      }
    });
  }
})();
