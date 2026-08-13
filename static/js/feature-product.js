/**
 * CareerReality Feature Product — scoped design system & interactions.
 * Loaded only on new feature pages; does not modify global production JS.
 */
(function () {
  'use strict';

  function initStepWizards() {
    document.querySelectorAll('[data-cr-wizard]').forEach(function (wizard) {
      var steps = wizard.querySelectorAll('[data-cr-step]');
      var panels = wizard.querySelectorAll('[data-cr-panel]');
      var progress = wizard.querySelector('[data-cr-stepper-progress]');
      var current = 0;

      if (!steps.length || !panels.length) return;
      // Signals to CSS that JS can drive navigation, so panels may collapse.
      wizard.classList.add('is-enhanced');

      function showStep(idx) {
        current = Math.max(0, Math.min(idx, steps.length - 1));
        steps.forEach(function (s, i) {
          s.classList.toggle('is-active', i === current);
          s.classList.toggle('is-complete', i < current);
          s.setAttribute('aria-selected', i === current ? 'true' : 'false');
        });
        panels.forEach(function (p, i) {
          p.hidden = i !== current;
          if (i === current) {
            p.classList.add('cr-wizard__panel');
          }
        });
        if (progress && steps.length > 1) {
          var pct = (current / (steps.length - 1)) * 100;
          progress.style.width = pct + '%';
        }
        var activeStep = steps[current];
        if (activeStep && window.matchMedia('(max-width: 768px)').matches) {
          activeStep.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
        }
        var prev = wizard.querySelector('[data-cr-prev]');
        var next = wizard.querySelector('[data-cr-next]');
        var isLast = current === panels.length - 1;
        if (prev) prev.hidden = current === 0;
        if (next) {
          next.textContent = isLast
            ? (wizard.getAttribute('data-cr-submit-label') || 'Analyze')
            : 'Continue';
          // Only the final step should submit; earlier steps just advance.
          next.setAttribute('type', isLast ? 'submit' : 'button');
        }
      }

      steps.forEach(function (btn, i) {
        btn.addEventListener('click', function () { showStep(i); });
      });
      var prevBtn = wizard.querySelector('[data-cr-prev]');
      var nextBtn = wizard.querySelector('[data-cr-next]');
      if (prevBtn) prevBtn.addEventListener('click', function () { showStep(current - 1); });
      if (nextBtn) nextBtn.addEventListener('click', function (event) {
        if (current < panels.length - 1) {
          event.preventDefault();
          showStep(current + 1);
        }
      });

      // Land the user on the first step that actually has a problem.
      var firstErrorPanel = -1;
      panels.forEach(function (panel, i) {
        if (firstErrorPanel === -1 && panel.querySelector('.cr-error, [aria-invalid="true"]')) {
          firstErrorPanel = i;
        }
      });
      showStep(firstErrorPanel === -1 ? 0 : firstErrorPanel);
    });
  }

  function initErrorSummary() {
    var summary = document.querySelector('[data-cr-error-summary]');
    if (!summary) return;
    summary.focus();
    summary.querySelectorAll('[data-cr-error-link]').forEach(function (link) {
      link.addEventListener('click', function (event) {
        var target = document.querySelector(link.getAttribute('href'));
        if (!target) return;
        event.preventDefault();
        var panel = target.closest('[data-cr-panel]');
        if (panel && panel.hidden) {
          var wizard = panel.closest('[data-cr-wizard]');
          var panels = wizard ? Array.prototype.slice.call(wizard.querySelectorAll('[data-cr-panel]')) : [];
          var steps = wizard ? wizard.querySelectorAll('[data-cr-step]') : [];
          var idx = panels.indexOf(panel);
          if (idx > -1 && steps[idx]) steps[idx].click();
        }
        target.focus();
      });
    });
  }

  function initResultFocus() {
    var result = document.querySelector('[data-cr-result]');
    if (!result) return;
    // Only pull focus after a submission, never on a fresh page load.
    if (!document.referrer || document.referrer.split('?')[0] !== location.href.split('?')[0]) {
      if (!window.performance || !performance.getEntriesByType) return;
      var nav = performance.getEntriesByType('navigation')[0];
      if (!nav || nav.type !== 'navigate') return;
    }
    result.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  function initOfferTabs() {
    document.querySelectorAll('[data-cr-offer-tabs]').forEach(function (root) {
      var tabs = root.querySelectorAll('[data-cr-offer-tab]');
      var panels = root.querySelectorAll('[data-cr-offer-panel]');
      function activate(idx) {
        tabs.forEach(function (t, i) {
          t.classList.toggle('is-active', i === idx);
          t.setAttribute('aria-selected', i === idx ? 'true' : 'false');
        });
        panels.forEach(function (p, i) {
          p.classList.toggle('is-active', i === idx);
          p.hidden = i !== idx;
        });
      }
      tabs.forEach(function (tab, i) {
        tab.addEventListener('click', function () { activate(i); });
      });
      activate(0);
    });
  }

  function initFormLoading() {
    document.querySelectorAll('form[data-cr-loading]').forEach(function (form) {
      form.addEventListener('submit', function () {
        var msg = form.getAttribute('data-cr-loading') || 'Analyzing your profile…';
        var overlay = document.createElement('div');
        overlay.className = 'cr-loading-overlay';
        overlay.setAttribute('role', 'status');
        overlay.innerHTML = '<div class="cr-loading-overlay__box"><div class="cr-loading-spinner"></div><p>' + msg + '</p></div>';
        document.body.appendChild(overlay);
      });
    });
  }

  function initPromptChips() {
    document.querySelectorAll('[data-cr-prompt]').forEach(function (chip) {
      chip.addEventListener('click', function () {
        var ta = document.querySelector(chip.getAttribute('data-cr-target'));
        if (ta) {
          ta.value = chip.textContent.trim();
          ta.focus();
        }
      });
    });
  }

  function initRadarCharts() {
    document.querySelectorAll('#cr-radar-polygon[data-values]').forEach(function (poly) {
      try {
        var vals = JSON.parse(poly.getAttribute('data-values'));
        var cx = 120, cy = 120, r = 80;
        var angles = [ -Math.PI / 2, -Math.PI / 6, Math.PI / 6, Math.PI / 2, 5 * Math.PI / 6, -5 * Math.PI / 6 ];
        var pts = vals.map(function (v, i) {
          var ratio = Math.min(1, Math.max(0, v / 100));
          var a = angles[i % angles.length];
          return (cx + r * ratio * Math.cos(a)) + ',' + (cy + r * ratio * Math.sin(a));
        });
        poly.setAttribute('points', pts.join(' '));
      } catch (e) { /* graceful fallback to list */ }
    });
  }

  function initScoreAnimation() {
    document.querySelectorAll('[data-cr-animate-score]').forEach(function (el) {
      var target = parseFloat(el.getAttribute('data-cr-animate-score')) || 0;
      var duration = 800;
      var start = performance.now();
      function tick(now) {
        var p = Math.min(1, (now - start) / duration);
        var val = Math.round(target * p * 10) / 10;
        el.textContent = val;
        if (p < 1) requestAnimationFrame(tick);
      }
      requestAnimationFrame(tick);
    });
  }

  function initPrioritySliders() {
    document.querySelectorAll('[data-cr-priority]').forEach(function (input) {
      var out = document.querySelector('[data-cr-priority-out="' + input.name + '"]');
      function sync() {
        if (out) out.textContent = input.value;
      }
      input.addEventListener('input', sync);
      sync();
    });
  }

  function initCrsTabs() {
    document.querySelectorAll('[data-cr-crs-tabs]').forEach(function (root) {
      var tabs = root.querySelectorAll('[data-cr-crs-tab]');
      var container = root.closest('#reality-score') || root.parentElement;
      var rows = container.querySelectorAll('[data-cr-crs-panel]');
      function activate(key) {
        tabs.forEach(function (t) {
          var match = t.getAttribute('data-cr-crs-tab') === String(key);
          t.classList.toggle('is-active', match);
          t.setAttribute('aria-selected', match ? 'true' : 'false');
        });
        rows.forEach(function (row) {
          if (key === 'all') {
            row.hidden = false;
          } else {
            row.hidden = row.getAttribute('data-cr-crs-panel') !== String(key);
          }
        });
      }
      tabs.forEach(function (tab) {
        tab.addEventListener('click', function () {
          activate(tab.getAttribute('data-cr-crs-tab'));
        });
      });
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    initStepWizards();
    initErrorSummary();
    initResultFocus();
    initOfferTabs();
    initCrsTabs();
    initFormLoading();
    initPromptChips();
    initRadarCharts();
    initScoreAnimation();
    initPrioritySliders();
  });
})();
