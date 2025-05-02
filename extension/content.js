// content.js - detectie op webpagina's

const apiUrl = "https://dropshipping-backend.onrender.com";

// Haal tekstinhoud van de pagina op
const pageText = document.body.innerText || "";

// Verstuur naar backend voor analyse
fetch(`${apiUrl}/analyze`, {
  method: "POST",
  headers: {
    "Content-Type": "application/json"
  },
  body: JSON.stringify({ text: pageText, url: window.location.href })
})
.then(res => res.json())
.then(data => {
  if (data.is_dropshipping) {
    chrome.runtime.sendMessage({ alert: true, result: data });
  }
})
.catch(err => {
  console.warn("❌ Fout bij backend-analyse:", err);
});
