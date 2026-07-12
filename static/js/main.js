document.addEventListener('DOMContentLoaded', () => {
    const mobileToggle = document.querySelector('.mobile-menu-toggle');
    const mobileNav = document.querySelector('.mobile-nav');
    const overlay = document.querySelector('.mobile-menu-overlay');
    const mobileNavClose = document.querySelector('.mobile-nav-close');
    const body = document.body;

    // ── Header scroll shadow ──
    const header = document.querySelector('.site-header');
    if (header) {
        let ticking = false;
        window.addEventListener('scroll', () => {
            if (!ticking) {
                requestAnimationFrame(() => {
                    header.classList.toggle('scrolled', window.scrollY > 10);
                    ticking = false;
                });
                ticking = true;
            }
        }, { passive: true });
    }

    // ── Desktop search toggle ──
    const searchToggle = document.querySelector('.nav-search-wrapper .nav-search-toggle');
    const searchForm = document.getElementById('nav-search-form');
    if (searchToggle && searchForm) {
        searchToggle.addEventListener('click', (e) => {
            e.stopPropagation();
            searchForm.classList.toggle('active');
            if (searchForm.classList.contains('active')) {
                searchForm.querySelector('input').focus();
            }
        });
        document.addEventListener('click', (e) => {
            if (!searchForm.contains(e.target) && !searchToggle.contains(e.target)) {
                searchForm.classList.remove('active');
            }
        });
    }

    // ── Mobile search toggle ──
    const mobileSearchToggle = document.querySelector('.nav-search-toggle--mobile');
    const mobileSearchPanel = document.getElementById('mobile-search-panel');
    if (mobileSearchToggle && mobileSearchPanel) {
        mobileSearchToggle.addEventListener('click', (e) => {
            e.stopPropagation();
            mobileSearchPanel.classList.toggle('active');
            if (mobileSearchPanel.classList.contains('active')) {
                mobileSearchPanel.querySelector('input').focus();
            } else {
                mobileSearchPanel.querySelector('input').blur();
            }
        });
        document.addEventListener('click', (e) => {
            if (!mobileSearchPanel.contains(e.target) && !mobileSearchToggle.contains(e.target)) {
                mobileSearchPanel.classList.remove('active');
            }
        });
    }

    function closeMenu() {
        if (mobileToggle) mobileToggle.classList.remove('active');
        if (mobileNav) mobileNav.classList.remove('active');
        if (overlay) overlay.classList.remove('active');
        body.classList.remove('menu-open');
    }

    function openMenu() {
        if (mobileToggle) mobileToggle.classList.add('active');
        if (mobileNav) mobileNav.classList.add('active');
        if (overlay) overlay.classList.add('active');
        body.classList.add('menu-open');
    }

    function toggleMenu() {
        if (mobileToggle && mobileToggle.classList.contains('active')) {
            closeMenu();
        } else {
            openMenu();
        }
    }

    if (mobileToggle) {
        mobileToggle.addEventListener('click', (e) => {
            e.stopPropagation();
            toggleMenu();
        });
    }

    if (mobileNavClose) {
        mobileNavClose.addEventListener('click', closeMenu);
    }

    if (overlay) {
        overlay.addEventListener('click', closeMenu);
    }

    // Close menu when a nav link is tapped
    if (mobileNav) {
        mobileNav.querySelectorAll('.mobile-nav-link, .mobile-pro-btn').forEach(link => {
            link.addEventListener('click', closeMenu);
        });
    }

    // ── Mobile drawer accordion ──
    const accordionTriggers = document.querySelectorAll('.mobile-nav-accordion-trigger');
    accordionTriggers.forEach(trigger => {
        trigger.addEventListener('click', () => {
            const panelId = trigger.getAttribute('aria-controls');
            const panel = document.getElementById(panelId);
            const isOpen = trigger.getAttribute('aria-expanded') === 'true';

            accordionTriggers.forEach(other => {
                if (other !== trigger) {
                    other.setAttribute('aria-expanded', 'false');
                    const otherPanel = document.getElementById(other.getAttribute('aria-controls'));
                    if (otherPanel) otherPanel.classList.remove('is-open');
                }
            });

            if (isOpen) {
                trigger.setAttribute('aria-expanded', 'false');
                if (panel) panel.classList.remove('is-open');
            } else {
                trigger.setAttribute('aria-expanded', 'true');
                if (panel) panel.classList.add('is-open');
            }
        });
    });

    // ── Bottom tab bar: active state ──
    const dockItems = document.querySelectorAll('.dock-item[data-dock-path]');
    const currentPath = window.location.pathname;

    dockItems.forEach(item => {
        const dockPath = item.getAttribute('data-dock-path');
        if (dockPath && (currentPath === dockPath || currentPath.startsWith(dockPath.replace(/\/$/, '') + '/'))) {
            item.classList.add('is-active');
        }
    });

    // Special case: company detail pages
    if (currentPath.startsWith('/companies/') && currentPath !== '/companies/write-review/') {
        dockItems.forEach(item => item.classList.remove('is-active'));
        const companiesItem = document.querySelector('.dock-item[data-dock-path="/companies/"]');
        if (companiesItem) companiesItem.classList.add('is-active');
    }

    // ── More bottom sheet ──
    const moreTrigger = document.getElementById('dock-more-trigger');
    const moreSheet = document.getElementById('more-sheet');
    const moreOverlay = document.getElementById('more-sheet-overlay');

    function openMoreSheet() {
        if (!moreSheet || !moreOverlay) return;
        moreSheet.classList.add('is-open');
        moreOverlay.classList.add('is-open');
        moreSheet.setAttribute('aria-hidden', 'false');
        moreOverlay.setAttribute('aria-hidden', 'false');
        if (moreTrigger) moreTrigger.setAttribute('aria-expanded', 'true');
        body.classList.add('sheet-open');
    }

    function closeMoreSheet() {
        if (!moreSheet || !moreOverlay) return;
        moreSheet.classList.remove('is-open');
        moreOverlay.classList.remove('is-open');
        moreSheet.setAttribute('aria-hidden', 'true');
        moreOverlay.setAttribute('aria-hidden', 'true');
        if (moreTrigger) moreTrigger.setAttribute('aria-expanded', 'false');
        body.classList.remove('sheet-open');
    }

    if (moreTrigger) {
        moreTrigger.addEventListener('click', (e) => {
            e.preventDefault();
            if (moreSheet && moreSheet.classList.contains('is-open')) {
                closeMoreSheet();
            } else {
                openMoreSheet();
            }
        });
    }

    if (moreOverlay) {
        moreOverlay.addEventListener('click', closeMoreSheet);
    }

    if (moreSheet) {
        moreSheet.querySelectorAll('.more-sheet-link').forEach(link => {
            link.addEventListener('click', closeMoreSheet);
        });
    }

    // ── Table data-label injection for mobile cards ──
    function injectTableLabels() {
        if (window.innerWidth > 768) return;

        document.querySelectorAll('table.editorial-table, table.salary-table').forEach(table => {
            const headers = Array.from(table.querySelectorAll('thead th')).map(th => th.textContent.trim());
            if (!headers.length) return;

            table.querySelectorAll('tbody tr').forEach(row => {
                row.querySelectorAll('td').forEach((td, i) => {
                    if (!td.hasAttribute('data-label') && headers[i]) {
                        td.setAttribute('data-label', headers[i]);
                    }
                });
            });
        });
    }

    injectTableLabels();
    window.addEventListener('resize', injectTableLabels);

    // Generic Dropdown Handler (Supports multiple)
    const dropdowns = document.querySelectorAll('.nav-dropdown');

    dropdowns.forEach(dropdown => {
        const trigger = dropdown.querySelector('.nav-dropdown-trigger');
        const content = dropdown.querySelector('.nav-dropdown-content');

        if (trigger && content) {
            let isOpen = false;

            trigger.addEventListener('click', (e) => {
                e.stopPropagation();
                e.preventDefault();

                dropdowns.forEach(other => {
                    if (other !== dropdown) {
                        const otherContent = other.querySelector('.nav-dropdown-content');
                        const otherTrigger = other.querySelector('.nav-dropdown-trigger');
                        if (otherContent) otherContent.style.display = 'none';
                        if (otherTrigger) otherTrigger.setAttribute('aria-expanded', 'false');
                    }
                });

                isOpen = !isOpen;

                if (isOpen) {
                    content.style.display = 'block';
                    trigger.setAttribute('aria-expanded', 'true');
                } else {
                    content.style.display = 'none';
                    trigger.setAttribute('aria-expanded', 'false');
                }
            });

            let hoverTimeout;
            dropdown.addEventListener('mouseenter', () => {
                clearTimeout(hoverTimeout);
                content.style.display = 'block';
            });
            dropdown.addEventListener('mouseleave', () => {
                hoverTimeout = setTimeout(() => {
                    content.style.display = 'none';
                    isOpen = false;
                    trigger.setAttribute('aria-expanded', 'false');
                }, 200);
            });
        }
    });

    document.addEventListener('click', (e) => {
        dropdowns.forEach(dropdown => {
            const content = dropdown.querySelector('.nav-dropdown-content');
            const trigger = dropdown.querySelector('.nav-dropdown-trigger');
            if (content && !dropdown.contains(e.target)) {
                content.style.display = 'none';
                if (trigger) trigger.setAttribute('aria-expanded', 'false');
            }
        });
    });

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            if (mobileNav && mobileNav.classList.contains('active')) {
                closeMenu();
            }
            if (moreSheet && moreSheet.classList.contains('is-open')) {
                closeMoreSheet();
            }
            if (mobileSearchPanel && mobileSearchPanel.classList.contains('active')) {
                mobileSearchPanel.classList.remove('active');
            }
            dropdowns.forEach(dropdown => {
                const content = dropdown.querySelector('.nav-dropdown-content');
                const trigger = dropdown.querySelector('.nav-dropdown-trigger');
                if (content) content.style.display = 'none';
                if (trigger) trigger.setAttribute('aria-expanded', 'false');
            });
            const sugBox = document.getElementById('search-suggestions');
            if (sugBox) sugBox.style.display = 'none';
        }
    });

    // ── Hide company review sticky CTA when form is visible ──
    const reviewSticky = document.querySelector('.cp-sticky-cta');
    const writeReviewSection = document.getElementById('write-review');
    if (reviewSticky && writeReviewSection && 'IntersectionObserver' in window) {
        const reviewObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                reviewSticky.classList.toggle('is-hidden', entry.isIntersecting);
            });
        }, { rootMargin: '-20% 0px -30% 0px', threshold: 0.1 });
        reviewObserver.observe(writeReviewSection);
    }

    // ── Swipe down to close More sheet ──
    if (moreSheet) {
        let sheetStartY = 0;
        moreSheet.addEventListener('touchstart', (e) => {
            sheetStartY = e.touches[0].clientY;
        }, { passive: true });
        moreSheet.addEventListener('touchend', (e) => {
            if (e.changedTouches[0].clientY - sheetStartY > 72) {
                closeMoreSheet();
            }
        }, { passive: true });
    }

    // --- Global Search Autocomplete ---
    const searchInput = document.getElementById('global-search-input');
    const suggestionsBox = document.getElementById('search-suggestions');

    if (searchInput && suggestionsBox) {
        let debounceTimer = null;

        searchInput.addEventListener('input', () => {
            clearTimeout(debounceTimer);
            const q = searchInput.value.trim();
            if (q.length < 2) {
                suggestionsBox.style.display = 'none';
                suggestionsBox.innerHTML = '';
                return;
            }
            debounceTimer = setTimeout(() => {
                fetch('/search/suggest/?q=' + encodeURIComponent(q))
                    .then(r => r.json())
                    .then(data => {
                        if (!data.results || data.results.length === 0) {
                            suggestionsBox.style.display = 'none';
                            suggestionsBox.innerHTML = '';
                            return;
                        }
                        suggestionsBox.innerHTML = data.results.map(item => {
                            const typeClass = {
                                article: 'badge-info',
                                company: 'badge-success',
                                news: 'badge-warning'
                            }[item.type] || 'badge-neutral';
                            return '<a href="' + item.url + '" class="search-suggestion-item">'
                                + '<span class="badge badge-sm ' + typeClass + '">' + item.type + '</span> '
                                + '<span>' + item.text + '</span></a>';
                        }).join('');
                        suggestionsBox.style.display = 'block';
                    })
                    .catch(() => {
                        suggestionsBox.style.display = 'none';
                    });
            }, 250);
        });

        document.addEventListener('click', (e) => {
            if (!searchInput.contains(e.target) && !suggestionsBox.contains(e.target)) {
                suggestionsBox.style.display = 'none';
            }
        });

        searchInput.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowDown' && suggestionsBox.style.display === 'block') {
                e.preventDefault();
                const first = suggestionsBox.querySelector('.search-suggestion-item');
                if (first) first.focus();
            }
        });

        suggestionsBox.addEventListener('keydown', (e) => {
            const focused = document.activeElement;
            if (e.key === 'ArrowDown') {
                e.preventDefault();
                const next = focused.nextElementSibling;
                if (next) next.focus();
            } else if (e.key === 'ArrowUp') {
                e.preventDefault();
                const prev = focused.previousElementSibling;
                if (prev) prev.focus();
                else searchInput.focus();
            } else if (e.key === 'Escape') {
                suggestionsBox.style.display = 'none';
                searchInput.focus();
            }
        });
    }
});
