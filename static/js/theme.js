(function () {
    var STORAGE_KEY = 'cr-theme';
    var root = document.documentElement;

    function getStoredTheme() {
        try {
            var stored = localStorage.getItem(STORAGE_KEY);
            if (stored === 'light' || stored === 'dark') {
                return stored;
            }
        } catch (e) {
            // localStorage unavailable
        }
        // Default matches Real Career Compass reference: light editorial + Night toggle
        return 'light';
    }

    function applyTheme(theme) {
        var isLight = theme === 'light';
        root.setAttribute('data-theme', theme);
        root.classList.toggle('theme-light', isLight);
        root.classList.toggle('theme-dark', !isLight);

        var meta = document.querySelector('meta[name="theme-color"]');
        if (meta) {
            meta.setAttribute('content', isLight ? '#f5f5f0' : '#0b0b0c');
        }

        document.querySelectorAll('[data-theme-toggle]').forEach(function (btn) {
            var label = isLight ? 'Switch to night mode' : 'Switch to light mode';
            btn.setAttribute('aria-label', label);
            btn.setAttribute('title', label);
            btn.setAttribute('aria-pressed', isLight ? 'false' : 'true');
            var text = btn.querySelector('.theme-toggle-label');
            if (text) {
                text.textContent = isLight ? 'Night' : 'Day';
            }
        });

        document.querySelectorAll('.mobile-theme-label').forEach(function (el) {
            el.textContent = isLight ? 'Night mode' : 'Light mode';
        });
    }

    function setTheme(theme) {
        if (theme !== 'light' && theme !== 'dark') {
            theme = 'light';
        }
        try {
            localStorage.setItem(STORAGE_KEY, theme);
        } catch (e) {
            // ignore
        }
        applyTheme(theme);
        if (typeof window.crTrack === 'function') {
            window.crTrack('theme_toggle', { theme: theme });
        }
    }

    function toggleTheme() {
        setTheme(getStoredTheme() === 'dark' ? 'light' : 'dark');
    }

    window.crSetTheme = setTheme;
    window.crToggleTheme = toggleTheme;

    document.addEventListener('DOMContentLoaded', function () {
        applyTheme(getStoredTheme());

        document.querySelectorAll('[data-theme-toggle]').forEach(function (btn) {
            btn.addEventListener('click', function (e) {
                e.preventDefault();
                toggleTheme();
            });
        });
    });
})();
