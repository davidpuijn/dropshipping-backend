document.getElementById("reportButton").addEventListener("click", () => {
  chrome.tabs.query({ active: true, currentWindow: true }, tabs => {
    chrome.scripting.executeScript({
      target: { tabId: tabs[0].id },
      function: () => {
        const url = window.location.href;
        const text = document.body.innerText.slice(0, 1000); // Beperk text
        fetch("https://klselxdmqxmwqiqjesry.supabase.co", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "apikey": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imtsc2VseGRtcXhtd3FpcWplc3J5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDYyMjEzNzIsImV4cCI6MjA2MTc5NzM3Mn0.2pvkzKNAeL3Kjti6Tx8BXO9OxA-1HCqL2o8yEVAbX_0",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imtsc2VseGRtcXhtd3FpcWplc3J5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDYyMjEzNzIsImV4cCI6MjA2MTc5NzM3Mn0.2pvkzKNAeL3Kjti6Tx8BXO9OxA-1HCqL2o8yEVAbX_0",
            "Prefer": "return=minimal"
          },
          body: JSON.stringify({
            url: url,
            text: text,
            status: "manual",
            manually_added: true,
            ai_trained: false,
            source: "manual_button"
          })
        }).then(res => {
          if (res.ok) alert("✅ Succesvol gemeld!");
         else alert("⚠️ Melding mislukt.");

        });
      }
    });
  });
});
