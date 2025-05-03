const pageText = document.body.innerText.toLowerCase();
const url = window.location.href;

fetch("https://dropshipping-backend.onrender.com", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ text: pageText, url })
})
.then(res => res.json())
.then(data => {
  if (data.result === "dropshipping") {
    chrome.runtime.sendMessage({ alert: true, result: data });
  }
});