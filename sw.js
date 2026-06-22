/* Service Worker — École Facile
   Stratégie : cache-first pour les assets statiques,
   network-first pour les pages HTML */

var CACHE = 'ef-v2';

var PRECACHE = [
  '/',
  '/index.html',
  '/favicon.svg',
  '/manifest.json',
  'https://fonts.googleapis.com/css2?family=Nunito:wght@700;800;900&display=swap'
];

// ── Installation : précache des assets essentiels ─────────────
self.addEventListener('install', function (e) {
  e.waitUntil(
    caches.open(CACHE).then(function (cache) {
      return cache.addAll(PRECACHE);
    }).then(function () {
      return self.skipWaiting();
    })
  );
});

// ── Activation : supprime les anciens caches ──────────────────
self.addEventListener('activate', function (e) {
  e.waitUntil(
    caches.keys().then(function (keys) {
      return Promise.all(
        keys.filter(function (k) { return k !== CACHE; })
            .map(function (k) { return caches.delete(k); })
      );
    }).then(function () {
      return self.clients.claim();
    })
  );
});

// ── Fetch : cache-first pour CSS/JS/images, network-first HTML ─
self.addEventListener('fetch', function (e) {
  var url = new URL(e.request.url);

  // Ne pas intercepter les requêtes Firebase / CDN externes hors fonts
  if (url.origin !== location.origin &&
      !url.href.includes('fonts.googleapis.com') &&
      !url.href.includes('fonts.gstatic.com')) {
    return;
  }

  var isHTML = e.request.headers.get('accept') &&
               e.request.headers.get('accept').includes('text/html');

  if (isHTML) {
    // Network-first pour les pages : contenu toujours à jour
    e.respondWith(
      fetch(e.request).then(function (res) {
        var clone = res.clone();
        caches.open(CACHE).then(function (c) { c.put(e.request, clone); });
        return res;
      }).catch(function () {
        return caches.match(e.request).then(function (cached) {
          return cached || caches.match('/index.html');
        });
      })
    );
  } else {
    // Cache-first pour CSS, JS, fonts, images
    e.respondWith(
      caches.match(e.request).then(function (cached) {
        if (cached) return cached;
        return fetch(e.request).then(function (res) {
          var clone = res.clone();
          caches.open(CACHE).then(function (c) { c.put(e.request, clone); });
          return res;
        });
      })
    );
  }
});
