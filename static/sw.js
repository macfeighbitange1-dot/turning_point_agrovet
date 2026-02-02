const CACHE_NAME = 'turningpoint-agrovet-v2'; // Incremented version
const STATIC_ASSETS = [
  '/',
  '/static/css/style.css',
  '/static/img/logo.png',
  'https://fonts.googleapis.com/css2?family=Inter:wght@300;500;700&display=swap'
];

// 1. Install Service Worker - Pre-cache essential assets
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log('Caching essential assets...');
      return cache.addAll(STATIC_ASSETS);
    })
  );
  self.skipWaiting(); // Force active immediately
});

// 2. Activation - Delete old caches to free up phone storage
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.filter(key => key !== CACHE_NAME).map(key => caches.delete(key))
      );
    })
  );
  return self.clients.claim();
});

// 3. Smart Fetch Strategy
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);

  // Strategy for Images: Cache First, then Network (and update cache)
  if (request.destination === 'image' || url.hostname === 'images.unsplash.com') {
    event.respondWith(
      caches.open(CACHE_NAME).then((cache) => {
        return cache.match(request).then((cachedResponse) => {
          const fetchedResponse = fetch(request).then((networkResponse) => {
            // Save a copy of the new image to cache for next time
            cache.put(request, networkResponse.clone());
            return networkResponse;
          });

          // Return the cached version immediately if it exists, else wait for network
          return cachedResponse || fetchedResponse;
        });
      })
    );
  } else {
    // Strategy for Everything Else: Cache falling back to Network
    event.respondWith(
      caches.match(request).then((response) => {
        return response || fetch(request);
      })
    );
  }
});