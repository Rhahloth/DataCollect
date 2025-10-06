document.addEventListener("DOMContentLoaded", () => {
  const syncBtn = document.getElementById("syncBtn");
  const syncWrapper = syncBtn ? syncBtn.closest("div") : null; 
  const statusBox = document.getElementById("syncStatus");

  if (syncBtn && syncWrapper) {
    if (navigator.onLine) {
      // Hide sync area completely if user is online
      syncWrapper.style.display = "none";
      return;
    }

    // If offline keep visible and enable sync
    syncBtn.addEventListener("click", async () => {
      syncBtn.disabled = true;
      syncBtn.innerText = "Syncing...";
      if (statusBox) statusBox.innerText = "Sync in progress...";

      try {
        const response = await fetch("/form/sync_all", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-Requested-With": "XMLHttpRequest"
          },
          body: JSON.stringify({})
        });

        const result = await response.json();

        if (response.ok) {
          if (statusBox) statusBox.innerText = result.message;
          syncBtn.innerText = "Synced";
        } else {
          if (statusBox) statusBox.innerText = `Error: ${result.error}`;
          syncBtn.innerText = "Retry Sync";
        }
      } catch (err) {
        if (statusBox) statusBox.innerText = `Request failed: ${err}`;
        syncBtn.innerText = "Retry Sync";
      }

      syncBtn.disabled = false;
    });
  }
});
