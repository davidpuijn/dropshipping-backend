document.addEventListener("DOMContentLoaded", () => {
  const button = document.getElementById("reportButton");

  if (button) {
    button.addEventListener("click", () => {
      chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        chrome.scripting.executeScript(
          {
            target: { tabId: tabs[0].id },
            func: () => {
              const url = window.location.href;
              const text = document.body.innerText.slice(0, 1000);

              fetch("https://dropshipping-backend.onrender.com/report", {
                method: "POST",
                headers: {
                  "Content-Type": "application/json"
                },
                body: JSON.stringify({
                  url,
                  text,
                  reason: "Handmatige extensie-melding"
                })
              })
              .then(res => {
                if (res.ok) {
                  alert("✅ Succesvol gemeld!");
                } else {
                  alert("⚠️ Melding mislukt.");
                }
              });
            }
          }
        );
      });
    });
  }
});
