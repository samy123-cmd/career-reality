// Career Reality Service Worker — Offline support + caching
const CACHE_NAME = 'cr-v2';
const OFFLINE_URL = '/offline/';

const PRECACHE_URLS = [
    '/',
    '/offline/',
    '/static/css/style-core.css',
    '/static/css/theme-premium-dark.css',
    '/static/css/theme-dark-contrast.css',
    '/static/js/main.js',
];

self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            return cache.addAll(PRECACHE_URLS).catch(() => {
                // Non-fatal: some URLs may 404 during first install
            });
        })
    );
    self.skipWaiting();
});

self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((names) => {
            return Promise.all(
                names.filter((name) => name !== CACHE_NAME).map((name) => caches.delete(name))
            );
        })
    );
    self.clients.claim();
});

self.addEventListener('fetch', (event) => {
    if (event.request.method !== 'GET') return;

    const url = new URL(event.request.url);

    // Skip admin, API, and payment endpoints
    if (url.pathname.startsWith('/admin/') ||
        url.pathname.startsWith('/api/') ||
        url.pathname.startsWith('/payments/') ||
        url.pathname.startsWith('/internal/')) {
        return;
    }

    // Network-first for HTML pages
    if (event.request.headers.get('Accept')?.includes('text/html')) {
        event.respondWith(
            fetch(event.request)
                .then((response) => {
                    const clone = response.clone();
                    caches.open(CACHE_NAME).then((cache) => cache.put(event.request, clone));
                    return response;
                })
                .catch(() => {
                    return caches.match(event.request).then((cached) => {
                        return cached || caches.match(OFFLINE_URL);
                    });
                })
        );
        return;
    }

    // Cache-first for static assets
    if (url.pathname.startsWith('/static/')) {
        event.respondWith(
            caches.match(event.request).then((cached) => {
                return cached || fetch(event.request).then((response) => {
                    const clone = response.clone();
                    caches.open(CACHE_NAME).then((cache) => cache.put(event.request, clone));
                    return response;
                });
            })
        );
        return;
    }

    // Stale-while-revalidate for everything else
    event.respondWith(
        caches.match(event.request).then((cached) => {
            const fetchPromise = fetch(event.request).then((response) => {
                const clone = response.clone();
                caches.open(CACHE_NAME).then((cache) => cache.put(event.request, clone));
                return response;
            }).catch(() => cached);
            return cached || fetchPromise;
        })
    );
});
