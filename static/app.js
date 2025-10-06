document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("form").forEach(form => {
    form.addEventListener("submit", function (e) {
      e.preventDefault();

      const url = form.action; // e.g. /form/agronomic
      const data = Object.fromEntries(new FormData(form).entries());

      if (navigator.onLine) {
        fetch(url, { method: "POST", body: new FormData(form) })
          .then(r => console.log("Synced online:", r))
          .catch(err => console.error("Online save failed:", err));
      } else {
        saveToIndexedDB({ url, data });
        alert("Saved offline — will sync later");
      }
    });
  });
});

function saveToIndexedDB(record) {
  let request = indexedDB.open("FieldApp", 1);
  request.onupgradeneeded = e => {
    let db = e.target.result;
    if (!db.objectStoreNames.contains("pending")) {
      db.createObjectStore("pending", { autoIncrement: true });
    }
  };
  request.onsuccess = e => {
    let db = e.target.result;
    let tx = db.transaction("pending", "readwrite");
    tx.objectStore("pending").add(record);
    console.log("Saved to IndexedDB:", record);
  };
}
