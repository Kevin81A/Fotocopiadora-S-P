const CACHE_NAME = 'syp-cache-v1';
const ASSETS = [
  '/',
  '/index.html',
  '/nosotros.html',
  '/contacto.html',
  '/productos.html',
  '/servicio-tecnico.html',
  '/login.html',
  '/admin.html',
  '/css/style.css',
  '/js/products.js',
  '/js/auth.js',
  '/js/main.js',
  '/manifest.json'
];

self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS)).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.map((k) => (k !== CACHE_NAME ? caches.delete(k) : null)))
    ).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (e) => {
  e.respondWith(
    caches.match(e.request).then((res) => res || fetch(e.request)).catch(() => caches.match('/index.html'))
  );
});
