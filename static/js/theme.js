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
        return 'dark';
    }

    function applyTheme(theme) {
        var isLight = theme === 'light';
        root.setAttribute('data-theme', theme);
        root.classList.toggle('theme-light', isLight);
        root.classList.toggle('theme-dark', !isLight);

        var meta = document.querySelector('meta[name="theme-color"]');
        if (meta) {
            meta.setAttribute('content', isLight ? '#fafafa' : '#06060b');
        }

        document.querySelectorAll('[data-theme-toggle]').forEach(function (btn) {
            var label = isLight ? 'Switch to dark mode' : 'Switch to light mode';
            btn.setAttribute('aria-label', label);
            btn.setAttribute('title', label);
            btn.setAttribute('aria-pressed', isLight ? 'true' : 'false');
        });

        document.querySelectorAll('.mobile-theme-label').forEach(function (el) {
            el.textContent = isLight ? 'Dark mode' : 'Light mode';
        });
    }

    function setTheme(theme) {
        if (theme !== 'light' && theme !== 'dark') {
            theme = 'dark';
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
