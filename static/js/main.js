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

    // Topics Dropdown Handler (Desktop)
    const topicsDropdown = document.querySelector('.nav-dropdown');
    const topicsButton = document.querySelector('.nav-dropdown-trigger');
    const topicsContent = document.querySelector('.nav-dropdown-content');

    if (topicsButton && topicsContent) {
        let isOpen = false;

        topicsButton.addEventListener('click', (e) => {
            e.stopPropagation();
            e.preventDefault();
            isOpen = !isOpen;

            if (isOpen) {
                topicsContent.style.display = 'block';
                topicsButton.setAttribute('aria-expanded', 'true');
            } else {
                topicsContent.style.display = 'none';
                topicsButton.setAttribute('aria-expanded', 'false');
            }
        });

        // Close on outside click
        document.addEventListener('click', (e) => {
            if (topicsDropdown && !topicsDropdown.contains(e.target) && isOpen) {
                topicsContent.style.display = 'none';
                topicsButton.setAttribute('aria-expanded', 'false');
                isOpen = false;
            }
        });

        // Close on escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && isOpen) {
                topicsContent.style.display = 'none';
                topicsButton.setAttribute('aria-expanded', 'false');
                isOpen = false;
                topicsButton.focus(); // Return focus to button
            }
        });

        // Optional: Keep hover behavior for desktop as enhancement
        if (topicsDropdown) {
            let hoverTimeout;

            topicsDropdown.addEventListener('mouseenter', () => {
                clearTimeout(hoverTimeout);
                if (!isOpen) {
                    topicsContent.style.display = 'block';
                }
            });

            topicsDropdown.addEventListener('mouseleave', () => {
                hoverTimeout = setTimeout(() => {
                    if (!isOpen) {
                        topicsContent.style.display = 'none';
                    }
                }, 200);
            });
        }
    }
});
