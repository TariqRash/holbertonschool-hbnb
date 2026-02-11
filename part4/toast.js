/* ============================================
   HBnB - Toast Notification System (JS)
   Usage: showToast('success', 'Title', 'Message')
   Types: success, error, warning, info
   ============================================ */

(function () {
  'use strict';

  // SVG icons for each toast type (Lucide-style)
  const ICONS = {
    success: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>',
    error: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>',
    warning: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>',
    info: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>'
  };

  let container = null;

  /**
   * Ensure toast container exists
   */
  function ensureContainer() {
    if (!container || !document.body.contains(container)) {
      container = document.createElement('div');
      container.className = 'toast-container';
      container.setAttribute('role', 'alert');
      container.setAttribute('aria-live', 'polite');
      document.body.appendChild(container);
    }
    return container;
  }

  /**
   * Show a toast notification
   * @param {string} type - 'success' | 'error' | 'warning' | 'info'
   * @param {string} title - Toast title
   * @param {string} message - Toast message
   * @param {number} [duration=4000] - Auto-dismiss duration in ms (0 = no auto-dismiss)
   */
  function showToast(type, title, message, duration) {
    if (duration === undefined) duration = 4000;
    const c = ensureContainer();

    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.style.position = 'relative';
    toast.style.overflow = 'hidden';

    toast.innerHTML = `
      <span class="toast-icon">${ICONS[type] || ICONS.info}</span>
      <div class="toast-content">
        <div class="toast-title">${escapeToastHTML(title)}</div>
        <div class="toast-message">${escapeToastHTML(message)}</div>
      </div>
      <button class="toast-close" aria-label="Close">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
      </button>
      ${duration > 0 ? '<div class="toast-progress"></div>' : ''}
    `;

    // Close on click
    const closeBtn = toast.querySelector('.toast-close');
    closeBtn.addEventListener('click', function (e) {
      e.stopPropagation();
      dismissToast(toast);
    });

    toast.addEventListener('click', function () {
      dismissToast(toast);
    });

    c.appendChild(toast);

    // Progress bar animation
    if (duration > 0) {
      const progress = toast.querySelector('.toast-progress');
      if (progress) {
        progress.style.width = '100%';
        // Force reflow
        progress.offsetWidth;
        progress.style.transitionDuration = duration + 'ms';
        progress.style.width = '0%';
      }

      toast._timeout = setTimeout(function () {
        dismissToast(toast);
      }, duration);
    }

    // Limit to 5 visible toasts
    while (c.children.length > 5) {
      dismissToast(c.children[0]);
    }

    return toast;
  }

  /**
   * Dismiss a toast with exit animation
   */
  function dismissToast(toast) {
    if (toast._dismissed) return;
    toast._dismissed = true;

    if (toast._timeout) clearTimeout(toast._timeout);

    toast.classList.add('toast-exit');
    setTimeout(function () {
      if (toast.parentNode) {
        toast.parentNode.removeChild(toast);
      }
    }, 300);
  }

  /**
   * Escape HTML for toast content
   */
  function escapeToastHTML(str) {
    if (!str) return '';
    const div = document.createElement('div');
    div.appendChild(document.createTextNode(str));
    return div.innerHTML;
  }

  // Expose globally
  window.showToast = showToast;
})();
