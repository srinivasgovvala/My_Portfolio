// General animations — scroll reveals, tech tooltips, project GIF hover
(function() {
  // GSAP scroll reveals (progressive enhancement)
  if (typeof gsap !== 'undefined' && typeof ScrollTrigger !== 'undefined') {
    gsap.registerPlugin(ScrollTrigger);

    gsap.utils.toArray('.reveal').forEach((el) => {
      gsap.fromTo(el,
        { opacity: 0, y: 30 },
        {
          opacity: 1,
          y: 0,
          duration: 0.7,
          ease: 'power2.out',
          scrollTrigger: {
            trigger: el,
            start: 'top 90%',
            once: true,
          }
        }
      );
    });
  }

  // Tech node tooltips
  const tooltip = document.getElementById('tech-tooltip');
  const tooltipName = document.getElementById('tooltip-name');
  const tooltipDesc = document.getElementById('tooltip-desc');
  const tooltipProject = document.getElementById('tooltip-project');

  if (tooltip) {
    document.querySelectorAll('.tech-node').forEach(node => {
      function showTooltip(e) {
        const name = node.dataset.name || '';
        const desc = node.dataset.desc || '';
        const project = node.dataset.project || '';
        if (!name) return;

        tooltipName.textContent = name;
        tooltipDesc.textContent = desc;
        tooltipProject.textContent = project ? '→ ' + project : '';
        tooltip.hidden = false;
        moveTooltip(e);
      }

      function moveTooltip(e) {
        const x = Math.min(e.clientX + 12, window.innerWidth - 300);
        const y = Math.min(e.clientY + 12, window.innerHeight - 150);
        tooltip.style.left = x + 'px';
        tooltip.style.top = y + 'px';
      }

      node.addEventListener('mouseenter', showTooltip);
      node.addEventListener('mousemove', moveTooltip);
      node.addEventListener('mouseleave', () => { tooltip.hidden = true; });
      node.addEventListener('focus', showTooltip);
      node.addEventListener('blur', () => { tooltip.hidden = true; });
      node.addEventListener('keypress', e => { if (e.key === 'Enter') showTooltip(e); });
    });
  }

  // Project card click redirect + GIF replay on hover from starting
  document.querySelectorAll('.project-card').forEach(card => {
    const gifEl = card.querySelector('.project-gif');
    const caseStudyUrl = card.dataset.url;

    // Card click -> redirect to case study
    if (caseStudyUrl) {
      card.style.cursor = 'pointer';
      card.addEventListener('click', (e) => {
        // If clicking a direct external link (GitHub, Live demo) or its child, let that work naturally
        if (e.target.closest('a[target="_blank"]')) {
          return;
        }
        window.location.href = caseStudyUrl;
      });

      card.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
          if (e.target.closest('a[target="_blank"]')) return;
          window.location.href = caseStudyUrl;
        }
      });
    }

    if (!gifEl) return;

    const baseSrc = gifEl.dataset.src || gifEl.src;

    function startGifFromBeginning() {
      if (!baseSrc) return;
      // Re-assign src with cache-busting timestamp to guarantee restart from frame 0
      const sep = baseSrc.includes('?') ? '&' : '?';
      gifEl.src = baseSrc + sep + 't=' + Date.now();
      gifEl.classList.add('loaded');
    }

    // Desktop hover: restart GIF from beginning
    card.addEventListener('mouseenter', startGifFromBeginning);

    // Mobile tap (preview on first tap, navigate on second)
    let tapped = false;
    card.addEventListener('touchstart', (e) => {
      if (!tapped) {
        tapped = true;
        startGifFromBeginning();
        card.classList.add('preview-active');
        setTimeout(() => { tapped = false; card.classList.remove('preview-active'); }, 3500);
      }
    }, { passive: true });
  });

  // Intersection observer for lazy image loading
  const imgObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const img = entry.target;
        if (img.dataset.src) {
          img.src = img.dataset.src;
          imgObserver.unobserve(img);
        }
      }
    });
  }, { rootMargin: '200px' });

  document.querySelectorAll('img[data-src]').forEach(img => imgObserver.observe(img));
})();
