chrome.runtime.onMessage.addListener(async (message, sender, sendResponse) => {
  if (message.action === "aiResult") {
    const { url, status, text } = message;

    if (status === "dropshipping") {
      // Voeg hier Supabase-logica toe
      fetch("https://klselxdmqxmwqiqjesry.supabase.co", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "apikey": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imtsc2VseGRtcXhtd3FpcWplc3J5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDYyMjEzNzIsImV4cCI6MjA2MTc5NzM3Mn0.2pvkzKNAeL3Kjti6Tx8BXO9OxA-1HCqL2o8yEVAbX_0",
          "Authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imtsc2VseGRtcXhtd3FpcWplc3J5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDYyMjEzNzIsImV4cCI6MjA2MTc5NzM3Mn0.2pvkzKNAeL3Kjti6Tx8BXO9OxA-1HCqL2o8yEVAbX_0",
          "Prefer": "return=minimal"
        },
        body: JSON.stringify({
          url: url,
          text: text || "AI-detectie",
          status: "ai_detected",
          manually_added: false,
          ai_trained: false,
          source: "extension"
        })
      }).then(res => {
        if (!res.ok) console.error("Supabase logging mislukt (AI):", res.status);
      });
    }
  }
});
