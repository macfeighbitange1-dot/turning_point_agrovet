const CACHE_NAME = 'turning-point-v1';
const ASSETS_TO_CACHE = [
    '/',
    '/static/css/style.css',
    '/static/img/logo.png', // Ensure you have a logo here
    'https://fonts.googleapis.com/css2?family=Inter:wght@300;500;700&display=swap'
];

// Install Event: Caching the Shell
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            return cache.addAll(ASSETS_TO_CACHE);
        })
    );
});

// Activate Event: Cleaning old caches
self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((keys) => {
            return Promise.all(
                keys.filter(key => key !== CACHE_NAME).map(key => caches.delete(key))
            );
        })
    );
});

// Fetch Event: Serving from Cache when Offline
self.addEventListener('fetch', (event) => {
    event.respondWith(
        caches.match(event.request).then((response) => {
            // Return cached asset, or fetch from network
            return response || fetch(event.request).catch(() => {
                // If both fail (like a page not in cache), return nothing or a custom offline page
                if (event.request.mode === 'navigate') {
                    return caches.match('/');
                }
            });
        })
    );
});