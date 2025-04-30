(async () => {
  const text = document.body.innerText.toLowerCase();
  const url = window.location.hostname;

  const response = await fetch("https://dropshipping-backend.onrender.com/analyze", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "x-api-key": "MY_SECRET_API_KEY"
    },
    body: JSON.stringify({ url, text })
  });

  const result = await response.json();

  if (result.status === "dropshipping") {
    const banner = document.createElement("div");
    banner.innerText = "⚠️ Waarschuwing: Mogelijke dropshipping-website";
    banner.style.backgroundColor = "red";
    banner.style.color = "white";
    banner.style.padding = "12px";
    banner.style.fontSize = "16px";
    banner.style.fontWeight = "bold";
    banner.style.position = "fixed";
    banner.style.top = "0";
    banner.style.left = "0";
    banner.style.width = "100%";
    banner.style.zIndex = "9999";
    document.body.prepend(banner);
    document.body.style.marginTop = "48px";
  }

  chrome.runtime.sendMessage({
    action: 'aiResult',
    url,
    status: result.status
  });
})();