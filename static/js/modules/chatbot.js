// AI Chatbot
(function() {
  const fab = document.getElementById('chatbot-toggle');
  const panel = document.getElementById('chatbot-panel');
  const closeBtn = document.getElementById('chatbot-close');
  const messages = document.getElementById('chatbot-messages');
  const form = document.getElementById('chatbot-form');
  const input = document.getElementById('chatbot-input');
  const aiToggleNav = document.getElementById('aiToggleNav');
  const sendBtn = form ? form.querySelector('.chatbot-send') : null;

  if (!fab || !panel) return;

  let openedAt = 0;

  function openChat() {
    panel.hidden = false;
    fab.setAttribute('aria-expanded', 'true');
    openedAt = Date.now();
    // Only auto-focus on desktop devices to avoid jarring keyboard pop-up & viewport scroll jumps on mobile
    const isMobile = window.innerWidth <= 768 || ('ontouchstart' in window && window.innerWidth <= 1024);
    if (input && !isMobile) {
      setTimeout(() => input.focus(), 150);
    }
  }

  function closeChat() {
    panel.hidden = true;
    fab.setAttribute('aria-expanded', 'false');
  }

  function toggleChat(e) {
    if (e) {
      e.preventDefault();
      e.stopPropagation();
    }
    if (panel.hidden) {
      openChat();
    } else {
      closeChat();
    }
  }

  fab.addEventListener('click', toggleChat);

  if (closeBtn) {
    closeBtn.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();
      closeChat();
    });
  }

  if (aiToggleNav) {
    aiToggleNav.addEventListener('click', toggleChat);
  }

  // Escape key
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && !panel.hidden) {
      closeChat();
    }
  });

  // Close when clicking outside chatbot (safe against mobile taps and DOM unmounts)
  document.addEventListener('click', (e) => {
    if (panel.hidden) return;
    if (Date.now() - openedAt < 350) return; // Guard against the initial opening tap
    const target = e.target;
    if (!target) return;

    const isInsidePanel = panel.contains(target) || (target.closest && target.closest('#chatbot-panel'));
    const isInsideFab = fab.contains(target) || (target.closest && target.closest('#chatbot-toggle, .chatbot-fab'));
    const isInsideNavToggle = aiToggleNav && (aiToggleNav.contains(target) || (target.closest && target.closest('#aiToggleNav, .ai-toggle')));

    if (!isInsidePanel && !isInsideFab && !isInsideNavToggle) {
      closeChat();
    }
  });

  // Escape HTML to prevent XSS
  function escapeHtml(str) {
    return str
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  // Robust Markdown & Link to HTML converter
  function parseMarkdown(raw) {
    if (!raw) return '';

    // 1. Separate inline bullet points onto new lines if crammed together
    let text = raw.replace(/([^\n])\s+[\*\-]\s+/g, '$1\n- ');

    // 2. Extract and protect Markdown links [label](url) with placeholders
    const mdLinks = [];
    text = text.replace(/\[([^\]]+)\]\((https?:\/\/[^\s\)\"\'<>]+)\)/g, (match, label, url) => {
      const id = mdLinks.length;
      mdLinks.push({ label: label, url: url });
      return `%%MD_LINK_${id}%%`;
    });

    // 3. Escape HTML entities
    text = escapeHtml(text);

    // 4. Convert bare URLs into clickable links
    text = text.replace(/https?:\/\/[^\s\)\"\'<>]+/g, (url) => {
      let clean = url;
      let suffix = '';
      while (/[.,;:!?)]$/.test(clean)) {
        suffix = clean.slice(-1) + suffix;
        clean = clean.slice(0, -1);
      }
      return `<a href="${clean}" target="_blank" rel="noopener noreferrer" class="chat-link">${clean} <span class="link-arrow">↗</span></a>${suffix}`;
    });

    // 5. Restore protected Markdown links
    for (let i = 0; i < mdLinks.length; i++) {
      const item = mdLinks[i];
      const cleanLabel = escapeHtml(item.label);
      const cleanUrl = item.url.replace(/"/g, '&quot;');
      const htmlLink = `<a href="${cleanUrl}" target="_blank" rel="noopener noreferrer" class="chat-link">${cleanLabel} <span class="link-arrow">↗</span></a>`;
      text = text.replace(`%%MD_LINK_${i}%%`, htmlLink);
    }

    // 6. Inline code `code`
    text = text.replace(/`([^`]+)`/g, '<code class="chat-inline-code">$1</code>');

    // 7. Bold: **text** or __text__
    text = text.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
    text = text.replace(/__([^_]+)__/g, '<strong>$1</strong>');

    // 8. Italic: *text* or _text_
    text = text.replace(/(^|[^\*])\*([^\*]+)\*([^\*]|$)/g, '$1<em>$2</em>$3');

    // 9. Process lines for lists and paragraphs
    const lines = text.split('\n');
    const result = [];
    let inList = false;

    for (let i = 0; i < lines.length; i++) {
      const line = lines[i].trim();
      if (!line) {
        if (inList) {
          result.push('</ul>');
          inList = false;
        }
        continue;
      }

      // Check for bullet list item (* or -)
      const bulletMatch = line.match(/^[\*\-]\s+(.+)/);
      if (bulletMatch) {
        if (!inList) {
          result.push('<ul class="chat-list">');
          inList = true;
        }
        result.push(`<li>${bulletMatch[1]}</li>`);
      } else {
        if (inList) {
          result.push('</ul>');
          inList = false;
        }
        result.push(`<p>${line}</p>`);
      }
    }

    if (inList) {
      result.push('</ul>');
    }

    return result.join('');
  }

  function appendMsg(text, role) {
    const wrapper = document.createElement('div');
    wrapper.className = `chat-msg ${role}`;
    const bubble = document.createElement('div');
    bubble.className = 'chat-bubble';

    if (role === 'ai') {
      bubble.innerHTML = parseMarkdown(text);
    } else {
      bubble.textContent = text;
    }

    wrapper.appendChild(bubble);
    messages.appendChild(wrapper);
    messages.scrollTop = messages.scrollHeight;
    return wrapper;
  }

  function showTyping() {
    const wrapper = document.createElement('div');
    wrapper.className = 'chat-msg ai';
    wrapper.id = 'chat-typing-indicator';
    wrapper.innerHTML = '<div class="chat-typing"><span></span><span></span><span></span></div>';
    messages.appendChild(wrapper);
    messages.scrollTop = messages.scrollHeight;
  }

  function hideTyping() {
    const t = document.getElementById('chat-typing-indicator');
    if (t) t.remove();
  }

  // Suggestion chips
  document.querySelectorAll('.suggestion-chip').forEach(chip => {
    chip.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();
      if (input) input.value = chip.dataset.msg;
      if (form) form.dispatchEvent(new Event('submit'));
    });
  });

  if (form) {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const msg = input ? input.value.trim() : '';
      if (!msg) return;
      if (input) input.value = '';
      if (sendBtn) sendBtn.disabled = true;

      // Hide suggestions
      const suggestionsEl = messages.querySelector('.chat-suggestions');
      if (suggestionsEl) suggestionsEl.remove();

      appendMsg(msg, 'user');
      showTyping();

      const csrf = (window.Utils && typeof window.Utils.getCsrfToken === 'function')
        ? window.Utils.getCsrfToken()
        : (window.CSRF_TOKEN || document.querySelector('#chatbot-form [name=csrfmiddlewaretoken]')?.value);

      const headers = {
        'Content-Type': 'application/json',
      };
      if (csrf) {
        headers['X-CSRFToken'] = csrf;
      }

      try {
        const res = await fetch('/chatbot/ask/', {
          method: 'POST',
          headers: headers,
          body: JSON.stringify({ message: msg }),
        });
        const data = await res.json();
        hideTyping();
        if (data.response) {
          appendMsg(data.response, 'ai');
        } else {
          appendMsg(data.error || 'AI assistant is temporarily unavailable. Please try again later.', 'error');
        }
      } catch (_) {
        hideTyping();
        appendMsg('AI assistant is temporarily unavailable. Please try again later.', 'error');
      } finally {
        if (sendBtn) sendBtn.disabled = false;
        const isMobile = window.innerWidth <= 768 || ('ontouchstart' in window && window.innerWidth <= 1024);
        if (input && !isMobile) input.focus();
      }
    });
  }
})();
