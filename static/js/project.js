// Project sticky nav scroll highlighting
(function() {
  const navLinks = document.querySelectorAll('.project-nav-link');
  if (!navLinks.length) return;

  function onScroll() {
    const y = window.scrollY + 160;
    let current = null;
    navLinks.forEach(link => {
      const id = link.getAttribute('href').replace('#', '');
      const el = document.getElementById(id);
      if (el && el.offsetTop <= y) current = link;
    });
    navLinks.forEach(l => l.classList.remove('active'));
    if (current) current.classList.add('active');
  }

  window.addEventListener('scroll', onScroll, { passive: true });
})();

// Showcase tab toggle (Preview / GIF)
(function() {
  const tabs = document.querySelectorAll('.showcase-tab');
  if (!tabs.length) return;

  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      const targetId = tab.dataset.target;
      tabs.forEach(t => { t.classList.remove('active'); t.setAttribute('aria-selected', 'false'); });
      document.querySelectorAll('.showcase-panel').forEach(p => p.classList.remove('active'));
      tab.classList.add('active');
      tab.setAttribute('aria-selected', 'true');
      const panel = document.getElementById(targetId);
      if (panel) panel.classList.add('active');
    });
  });
})();

