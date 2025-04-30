chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg.action === 'aiResult') {
    chrome.storage.local.get(['siteDB'], res => {
      const siteDB = res.siteDB || {};
      siteDB[msg.url] = msg.status;
      chrome.storage.local.set({ siteDB }, () => {
        console.log("AI result opgeslagen:", msg.url, msg.status);
      });
    });
  }

  if (msg.action === 'markSite') {
    chrome.storage.local.get(['siteDB'], res => {
      const siteDB = res.siteDB || {};
      siteDB[msg.url] = msg.status;
      chrome.storage.local.set({ siteDB }, () => {
        console.log("Handmatig gemarkeerd:", msg.url, msg.status);
      });
    });

    // Extra: stuur markering ook naar backend (eventueel met leerdata)
    fetch("https://dropshipping-backend.onrender.com/report", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "x-api-key": "{DEDC9729/12BZPM@}"
      },
      body: JSON.stringify({ url: msg.url, status: msg.status })
    });
  }
});
