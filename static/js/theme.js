(function () {
    var APPEARANCE_KEY = 'cr-appearance';
    var PALETTE_KEY = 'cr-palette';
    var LEGACY_THEME_KEY = 'cr-theme';
    var PALETTES = ['editorial-ink', 'warm-copper', 'midnight-navy', 'olive-graphite'];
    var THEME_COLORS = {
        'editorial-ink': { light: '#F7F5F0', dark: '#121212' },
        'warm-copper': { light: '#F6F1E9', dark: '#151311' },
        'midnight-navy': { light: '#F5F7F8', dark: '#0E151A' },
        'olive-graphite': { light: '#F5F4EE', dark: '#11130F' }
    };
    var root = document.documentElement;
    var mediaQuery = window.matchMedia ? window.matchMedia('(prefers-color-scheme: dark)') : null;

    function getStoredAppearance() {
        try {
            var stored = localStorage.getItem(APPEARANCE_KEY);
            if (stored === 'light' || stored === 'dark' || stored === 'system') {
                return stored;
            }
            var legacy = localStorage.getItem(LEGACY_THEME_KEY);
            if (legacy === 'light' || legacy === 'dark') {
                return legacy;
            }
        } catch (e) {
            // localStorage unavailable
        }
        return 'system';
    }

    function getStoredPalette() {
        try {
            var stored = localStorage.getItem(PALETTE_KEY);
            if (PALETTES.indexOf(stored) !== -1) {
                return stored;
            }
        } catch (e) {
            // ignore
        }
        return 'editorial-ink';
    }

    function resolveTheme(appearance) {
        if (appearance === 'light' || appearance === 'dark') {
            return appearance;
        }
        if (mediaQuery && mediaQuery.matches) {
            return 'dark';
        }
        return 'light';
    }

    function updateMetaThemeColor(palette, theme) {
        var meta = document.querySelector('meta[name="theme-color"]');
        if (!meta) return;
        var colors = THEME_COLORS[palette] || THEME_COLORS['editorial-ink'];
        meta.setAttribute('content', theme === 'dark' ? colors.dark : colors.light);
    }

    function syncControls(appearance, palette) {
        document.querySelectorAll('[data-appearance-option]').forEach(function (el) {
            var value = el.getAttribute('data-appearance-option');
            if (el.type === 'radio') {
                el.checked = value === appearance;
            }
            el.setAttribute('aria-checked', value === appearance ? 'true' : 'false');
        });
        document.querySelectorAll('[data-palette-option]').forEach(function (el) {
            var value = el.getAttribute('data-palette-option');
            if (el.type === 'radio') {
                el.checked = value === palette;
            }
            el.setAttribute('aria-checked', value === palette ? 'true' : 'false');
        });
        document.querySelectorAll('[data-theme-toggle]').forEach(function (btn) {
            var resolved = resolveTheme(appearance);
            var label = resolved === 'light' ? 'Appearance settings' : 'Appearance settings';
            btn.setAttribute('aria-label', label);
            btn.setAttribute('title', 'Appearance & theme');
        });
    }

    function applyState(appearance, palette) {
        var resolved = resolveTheme(appearance);
        root.setAttribute('data-appearance', appearance);
        root.setAttribute('data-palette', palette);
        root.setAttribute('data-theme', resolved);
        root.classList.toggle('theme-light', resolved === 'light');
        root.classList.toggle('theme-dark', resolved === 'dark');
        updateMetaThemeColor(palette, resolved);
        syncControls(appearance, palette);
    }

    function setAppearance(appearance) {
        if (appearance !== 'light' && appearance !== 'dark' && appearance !== 'system') {
            appearance = 'system';
        }
        try {
            localStorage.setItem(APPEARANCE_KEY, appearance);
            localStorage.setItem(LEGACY_THEME_KEY, resolveTheme(appearance));
        } catch (e) {
            // ignore
        }
        applyState(appearance, getStoredPalette());
        if (typeof window.crTrack === 'function') {
            window.crTrack('appearance_change', { appearance: appearance });
        }
    }

    function setPalette(palette) {
        if (PALETTES.indexOf(palette) === -1) {
            palette = 'editorial-ink';
        }
        try {
            localStorage.setItem(PALETTE_KEY, palette);
        } catch (e) {
            // ignore
        }
        applyState(getStoredAppearance(), palette);
        if (typeof window.crTrack === 'function') {
            window.crTrack('palette_change', { palette: palette });
        }
    }

    function setTheme(theme) {
        // Legacy API: maps to explicit light/dark appearance
        setAppearance(theme === 'dark' ? 'dark' : 'light');
    }

    function toggleTheme() {
        var resolved = resolveTheme(getStoredAppearance());
        setAppearance(resolved === 'dark' ? 'light' : 'dark');
    }

    function closePanels() {
        document.querySelectorAll('.cr-appearance-panel.is-open').forEach(function (panel) {
            panel.classList.remove('is-open');
        });
        document.querySelectorAll('[data-appearance-trigger]').forEach(function (btn) {
            btn.setAttribute('aria-expanded', 'false');
        });
    }

    window.crSetAppearance = setAppearance;
    window.crSetPalette = setPalette;
    window.crSetTheme = setTheme;
    window.crToggleTheme = toggleTheme;

    if (mediaQuery) {
        var onSchemeChange = function () {
            if (getStoredAppearance() === 'system') {
                applyState('system', getStoredPalette());
            }
        };
        if (typeof mediaQuery.addEventListener === 'function') {
            mediaQuery.addEventListener('change', onSchemeChange);
        } else if (typeof mediaQuery.addListener === 'function') {
            mediaQuery.addListener(onSchemeChange);
        }
    }

    document.addEventListener('DOMContentLoaded', function () {
        applyState(getStoredAppearance(), getStoredPalette());

        document.querySelectorAll('[data-appearance-trigger]').forEach(function (btn) {
            btn.addEventListener('click', function (e) {
                e.preventDefault();
                e.stopPropagation();
                var wrap = btn.closest('.cr-theme-toggle-wrap');
                var panel = wrap ? wrap.querySelector('.cr-appearance-panel') : null;
                var willOpen = panel && !panel.classList.contains('is-open');
                closePanels();
                if (panel && willOpen) {
                    panel.classList.add('is-open');
                    btn.setAttribute('aria-expanded', 'true');
                }
            });
        });

        // Keep legacy sun/moon toggle working as panel open OR theme flip if no panel
        document.querySelectorAll('[data-theme-toggle]').forEach(function (btn) {
            if (btn.hasAttribute('data-appearance-trigger')) return;
            btn.addEventListener('click', function (e) {
                e.preventDefault();
                toggleTheme();
            });
        });

        document.querySelectorAll('[data-appearance-option]').forEach(function (el) {
            el.addEventListener('change', function () {
                setAppearance(el.getAttribute('data-appearance-option'));
            });
            el.addEventListener('click', function () {
                if (el.type !== 'radio') {
                    setAppearance(el.getAttribute('data-appearance-option'));
                }
            });
        });

        document.querySelectorAll('[data-palette-option]').forEach(function (el) {
            el.addEventListener('change', function () {
                setPalette(el.getAttribute('data-palette-option'));
            });
            el.addEventListener('click', function () {
                if (el.type !== 'radio') {
                    setPalette(el.getAttribute('data-palette-option'));
                }
            });
        });

        document.addEventListener('click', function (e) {
            if (!e.target.closest('.cr-theme-toggle-wrap')) {
                closePanels();
            }
        });

        document.addEventListener('keydown', function (e) {
            if (e.key === 'Escape') closePanels();
        });
    });
})();
