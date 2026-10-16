const CACHE_NAME = 'netsec-pro-study-v3';
const ASSETS = [
  './',
  './index.html',
  './questions.js',
  './scor-questions.js',
  './manifest.webmanifest',
  './icon-192.png',
  './icon-512.png',
  './icon-maskable-512.png'
];

self.addEventListener('install', event => {
  event.waitUntil(
    fetch('./scor-questions.js')
      .then(response => response.text())
      .then(script => [...new Set(script.match(/"\.\/scor-exhibits\/[^"]+"/g) || [])].map(path => path.slice(1, -1)))
      .then(exhibits => caches.open(CACHE_NAME).then(cache => cache.addAll([...ASSETS, ...exhibits])))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys => Promise.all(keys.filter(key => key !== CACHE_NAME).map(key => caches.delete(key)))).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', event => {
  if (event.request.method !== 'GET') return;
  event.respondWith(
    caches.match(event.request).then(cached => {
      if (cached) return cached;
      return fetch(event.request)
        .then(response => {
          const copy = response.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(event.request, copy));
          return response;
        })
        .catch(() => event.request.mode === 'navigate' ? caches.match('./index.html') : cached);
    })
  );
});
