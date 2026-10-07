/* =========================================================
   Fotocopiadora SyP — Service Worker v3 (PWA Offline & Cache)
   Estrategia: Híbrida (Stale-While-Revalidate + Network-First)
   ========================================================= */

const CACHE_NAME = 'syp-cache-v3';
const STATIC_ASSETS = [
  '/',
  '/index.html',
  '/productos.html',
  '/servicio-tecnico.html',
  '/nosotros.html',
  '/contacto.html',
  '/login.html',
  '/cotizacion.html',
  '/admin.html',
  '/offline.html',
  '/css/style.css',
  '/js/products.js',
  '/js/auth.js',
  '/js/main.js',
  '/manifest.json'
];

// Instalación: Precarga de la Shell de la Aplicación
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log('[SyP SW] Precaching application shell...');
      return cache.addAll(STATIC_ASSETS);
    }).then(() => self.skipWaiting())
  );
});

// Activación: Limpieza de cachés antiguas
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.map((key) => {
          if (key !== CACHE_NAME) {
            console.log('[SyP SW] Removing outdated cache:', key);
            return caches.delete(key);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

// Intercepción de Solicitudes (Fetch)
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);

  // 1. Ignorar llamadas API a FastAPI o solicitudes no GET
  if (request.method !== 'GET' || url.pathname.startsWith('/api/') || url.port === '8000') {
    return;
  }

  // 2. Solicitudes de Navegación HTML: Network-First con fallback a Caché y luego a offline.html
  if (request.mode === 'navigate') {
    event.respondWith(
      fetch(request)
        .then((networkResponse) => {
          if (networkResponse && networkResponse.status === 200) {
            const clone = networkResponse.clone();
            caches.open(CACHE_NAME).then((cache) => cache.put(request, clone));
          }
          return networkResponse;
        })
        .catch(async () => {
          const cachedResponse = await caches.match(request);
          if (cachedResponse) return cachedResponse;
          const offlinePage = await caches.match('/offline.html');
          return offlinePage || new Response('Modo sin conexión', { status: 503, headers: { 'Content-Type': 'text/plain' } });
        })
    );
    return;
  }

  // 3. Recursos Estáticos (CSS, JS, Fuentes, Imágenes): Stale-While-Revalidate / Cache-First
  event.respondWith(
    caches.match(request).then((cachedResponse) => {
      const fetchPromise = fetch(request)
        .then((networkResponse) => {
          if (networkResponse && networkResponse.status === 200 && networkResponse.type === 'basic') {
            const clone = networkResponse.clone();
            caches.open(CACHE_NAME).then((cache) => cache.put(request, clone));
          }
          return networkResponse;
        })
        .catch(() => null);

      return cachedResponse || fetchPromise;
    })
  );
});

// Listener para actualización inmediata de SW
self.addEventListener('message', (event) => {
  if (event.data && event.data.action === 'skipWaiting') {
    self.skipWaiting();
  }
});
