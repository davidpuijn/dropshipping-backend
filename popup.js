document.addEventListener("DOMContentLoaded", () => {
  const button = document.getElementById("reportButton");

  if (button) {
    button.addEventListener("click", () => {
      chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        chrome.tabs.sendMessage(tabs[0].id, { action: "getPageInfo" }, (response) => {
          if (chrome.runtime.lastError || !response) {
            alert("⚠️ Kon pagina-inhoud niet ophalen.");
            return;
          }

          fetch("https://dropshipping-backend.onrender.com/report", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ url: websiteUrl, text: pageText, reason: "Handmatige melding" })
})

            })
          })
          .then(res => {
            if (res.ok) {
              alert("✅ Succesvol gemeld!");
            } else {
              alert("⚠️ Melding mislukt.");
            }
          });
        });
      });
    });
  }
});
