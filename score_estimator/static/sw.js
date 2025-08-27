self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open("score-estimator-cache").then((cache) => {
      return cache.addAll(["/", "/static/css/styles.css", "/static/js/app.js"]);
    })
  );
});

self.addEventListener("fetch", (event) => {
  event.respondWith(
    caches.match(event.request).then((response) => {
      return response || fetch(event.request);
    })
  );
});
