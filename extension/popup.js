// popup.js
document.getElementById("reportBtn").addEventListener("click", async () => {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  chrome.scripting.executeScript({
    target: { tabId: tab.id },
    func: () => ({
      text: document.body.innerText,
      url: window.location.href
    }),
  }, async (results) => {
    const { text, url } = results[0].result;
    await fetch("https://dropshipping-backend.onrender.com/report", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text, url })
    });
    document.getElementById("status").innerText = "✅ Rapport verzonden!";
  });
});
