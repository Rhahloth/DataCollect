self.addEventListener("install", event => {
  event.waitUntil(
    caches.open("field-app-cache").then(cache => {
      return cache.addAll([
        "/", 
        "/offline.html", 
        "/static/css/style.css",
        "/static/app.js"
      ]);
    })
  );
  console.log("Service Worker installed");
});

self.addEventListener("fetch", event => {
  event.respondWith(
    caches.match(event.request).then(response => {
      return response || fetch(event.request);
    })
  );
});

// Background sync
self.addEventListener("sync", event => {
  if (event.tag === "sync-forms") {
    event.waitUntil(syncPendingForms());
  }
});

function syncPendingForms() {
  return new Promise((resolve, reject) => {
    let request = indexedDB.open("FieldApp", 1);
    request.onsuccess = e => {
      let db = e.target.result;
      let tx = db.transaction("pending", "readwrite");
      let store = tx.objectStore("pending");
      let getAll = store.getAll();

      getAll.onsuccess = async () => {
        for (let record of getAll.result) {
          await fetch(record.url, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(record.data)
          }).catch(err => console.error("Sync failed:", err));
        }
        store.clear();
        resolve();
      };
    };
  });
}
