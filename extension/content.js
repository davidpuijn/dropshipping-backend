(async () => {
  const text = document.body.innerText.toLowerCase();
  const url = window.location.hostname;
  const API_KEY = CONFIG.API_KEY;

  const response = await fetch("https://dropshipping-backend.onrender.com/analyze", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "x-api-key": API_KEY
    },
    body: JSON.stringify({ url, text })
  });

  const result = await response.json();

  if (result.status === "dropshipping") {
    const banner = document.createElement("div");
    banner.innerText = "⚠️ Waarschuwing: Mogelijke dropshipping-website";
    banner.style = "background:red;color:white;padding:10px;position:fixed;top:0;width:100%;z-index:9999;";
    document.body.prepend(banner);
  }

  chrome.runtime.sendMessage({ action: 'aiResult', url, status: result.status });
})();