// Minimal service worker for WebAPK installation
// This enables the PWA to be installed as a full app on Android

self.addEventListener('install', (event) => {
  console.log('Service Worker installing.');
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  console.log('Service Worker activating.');
  return self.clients.claim();
});

self.addEventListener('fetch', (event) => {
  // Required fetch handler for WebAPK
  // Simply pass through all requests to the network
  event.respondWith(fetch(event.request));
});
