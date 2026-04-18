const CACHE_NAME = 'vitd-v1';
const SHELL_URLS = [
  '/vitd/',
  '/vitd/index.html',
  '/vitd/manifest.json',
  '/vitd/icons/icon-192.png',
  '/vitd/icons/icon-512.png'
];

// Install - cache shell
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(SHELL_URLS))
      .then(() => self.skipWaiting())
  );
});

// Activate - clean old caches
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames
          .filter(name => name !== CACHE_NAME)
          .map(name => caches.delete(name))
      );
    }).then(() => self.clients.claim())
  );
});

// Fetch - cache-first for shell, network-first for API
self.addEventListener('fetch', (event) => {
  const url = new URL(event.request.url);
  
  // GitHub API - network only, don't cache
  if (url.hostname === 'api.github.com') {
    event.respondWith(fetch(event.request));
    return;
  }
  
  // Shell files - cache first, network fallback
  event.respondWith(
    caches.match(event.request).then(cached => {
      if (cached) {
        // Return cached but also fetch update in background
        fetch(event.request).then(response => {
          caches.open(CACHE_NAME).then(cache => {
            cache.put(event.request, response.clone());
          });
        }).catch(() => {});
        return cached;
      }
      
      // Not in cache - fetch and cache
      return fetch(event.request).then(response => {
        if (response.ok) {
          const clone = response.clone();
          caches.open(CACHE_NAME).then(cache => {
            cache.put(event.request, clone);
          });
        }
        return response;
      });
    }).catch(() => {
      // Offline fallback - could return a custom offline page
      return new Response('Offline', { status: 503 });
    })
  );
});

// Background sync - retry failed Gist syncs
self.addEventListener('sync', (event) => {
  if (event.tag === 'vitd-sync') {
    event.waitUntil(syncToGist());
  }
});

// Message handler from main thread
self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});

// Helper to sync to Gist (called by background sync)
async function syncToGist() {
  // Get sync data from IndexedDB or return
  // This would need access to the stored sync credentials
  // For now, notify clients that sync is needed
  const clients = await self.clients.matchAll();
  clients.forEach(client => {
    client.postMessage({ type: 'SYNC_REQUIRED' });
  });
}

// Push notification handler (for future server push support)
self.addEventListener('push', (event) => {
  if (!event.data) return;
  
  const data = event.data.json();
  event.waitUntil(
    self.registration.showNotification(data.title, {
      body: data.body,
      icon: '/vitd/icons/icon-192.png',
      badge: '/vitd/icons/icon-192.png',
      tag: data.tag || 'vitd-reminder',
      requireInteraction: data.requireInteraction || false,
      actions: data.actions || []
    })
  );
});

// Notification click handler
self.addEventListener('notificationclick', (event) => {
  event.notification.close();
  
  event.waitUntil(
    clients.matchAll({ type: 'window' }).then(clientList => {
      if (clientList.length > 0) {
        clientList[0].focus();
      } else {
        clients.openWindow('/vitd/');
      }
    })
  );
});
