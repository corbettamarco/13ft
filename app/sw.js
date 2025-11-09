// Simple service worker for PWA installation
self.addEventListener('install', (event) => {
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(clients.claim());
});

// Basic fetch handler - just pass through to network
self.addEventListener('fetch', (event) => {
  event.respondWith(fetch(event.request));
});
