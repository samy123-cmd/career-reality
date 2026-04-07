document.addEventListener('DOMContentLoaded', () => {
    const mobileToggle = document.querySelector('.mobile-menu-toggle');
    const mobileNav = document.querySelector('.mobile-nav');
    const overlay = document.querySelector('.mobile-menu-overlay');
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
            }
        });
        document.addEventListener('click', (e) => {
            if (!mobileSearchPanel.contains(e.target) && !mobileSearchToggle.contains(e.target)) {
                mobileSearchPanel.classList.remove('active');
            }
        });
    }

    function toggleMenu() {
        const isActive = mobileToggle.classList.contains('active');

        if (isActive) {
            closeMenu();
        } else {
            openMenu();
        }
    }

    function openMenu() {
        mobileToggle.classList.add('active');
        mobileNav.classList.add('active');
        overlay.classList.add('active');
        body.classList.add('menu-open');
    }

    function closeMenu() {
        mobileToggle.classList.remove('active');
        mobileNav.classList.remove('active');
        overlay.classList.remove('active');
        body.classList.remove('menu-open');
    }

    // Event Listeners
    if (mobileToggle) {
        mobileToggle.addEventListener('click', (e) => {
            e.stopPropagation();
            toggleMenu();
        });
    }

    if (overlay) {
        overlay.addEventListener('click', closeMenu);
    }

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

                // Close others
                dropdowns.forEach(other => {
                    if (other !== dropdown) {
                        const otherContent = other.querySelector('.nav-dropdown-content');
                        const otherTrigger = other.querySelector('.nav-dropdown-trigger');
                        if (otherContent) otherContent.style.display = 'none';
                        if (otherTrigger) otherTrigger.setAttribute('aria-expanded', 'false');
                    }
                });

                isOpen = !isOpen; // Toggle current

                if (isOpen) {
                    content.style.display = 'block';
                    trigger.setAttribute('aria-expanded', 'true');
                } else {
                    content.style.display = 'none';
                    trigger.setAttribute('aria-expanded', 'false');
                }
            });

            // Hover support (Desktop)
            let hoverTimeout;
            dropdown.addEventListener('mouseenter', () => {
                // Close others first? Maybe not needed for hover, CSS handles it mostly.
                // But for consistency with JS state:
                clearTimeout(hoverTimeout);
                content.style.display = 'block';
            });
            dropdown.addEventListener('mouseleave', () => {
                hoverTimeout = setTimeout(() => {
                    content.style.display = 'none';
                    isOpen = false; // Sync state
                    trigger.setAttribute('aria-expanded', 'false');
                }, 200);
            });
        }
    });

    // Global Close on outside click
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

    // Close mobile menu + dropdowns on Escape key (single handler)
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            if (mobileNav && mobileNav.classList.contains('active')) {
                closeMenu();
            }
            dropdowns.forEach(dropdown => {
                const content = dropdown.querySelector('.nav-dropdown-content');
                const trigger = dropdown.querySelector('.nav-dropdown-trigger');
                if (content) content.style.display = 'none';
                if (trigger) trigger.setAttribute('aria-expanded', 'false');
            });
            // Close search suggestions on Escape
            const sugBox = document.getElementById('search-suggestions');
            if (sugBox) sugBox.style.display = 'none';
        }
    });

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

        // Close suggestions on outside click
        document.addEventListener('click', (e) => {
            if (!searchInput.contains(e.target) && !suggestionsBox.contains(e.target)) {
                suggestionsBox.style.display = 'none';
            }
        });

        // Allow keyboard navigation in suggestions
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
