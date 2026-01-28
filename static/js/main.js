document.addEventListener('DOMContentLoaded', () => {
    const mobileToggle = document.querySelector('.mobile-menu-toggle');
    const mobileNav = document.querySelector('.mobile-nav');
    const overlay = document.querySelector('.mobile-menu-overlay');
    const body = document.body;

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

    // Close on escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && mobileNav.classList.contains('active')) {
            closeMenu();
        }
    });

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

    // Close on escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            dropdowns.forEach(dropdown => {
                const content = dropdown.querySelector('.nav-dropdown-content');
                const trigger = dropdown.querySelector('.nav-dropdown-trigger');
                if (content) content.style.display = 'none';
                if (trigger) {
                    trigger.setAttribute('aria-expanded', 'false');
                    // Optionally focus back? trigger.focus();
                }
            });
        }
    });
});
