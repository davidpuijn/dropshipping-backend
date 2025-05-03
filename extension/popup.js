document.getElementById("reportButton").addEventListener("click", () => {
  chrome.runtime.sendMessage({ action: "getPageInfo" }, (data) => {
    if (!data || !data.url || !data.text) {
      alert("⚠️ Kon pagina-inhoud niet ophalen.");
      return;
    }

    fetch("https://dropshipping-backend.onrender.com/report", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url: data.url, text: data.text, reason: "Handmatige melding" })
    })
    .then(res => {
      if (res.ok) alert("✅ Succesvol gemeld!");
      else alert("⚠️ Melding mislukt.");
    })
    .catch(() => {
      alert("❌ Er is een fout opgetreden tijdens het verzenden.");
    });
  });
});
