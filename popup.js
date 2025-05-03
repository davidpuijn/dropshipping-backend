fetch("https://dropshipping-backend.onrender.com", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    url,
    text,
    status: "manual",
    manually_added: true,
    ai_trained: false,
    source: "manual_button"
  })
})
.then(res => {
  if (res.ok) alert("✅ Succesvol gemeld!");
  else alert("⚠️ Melding mislukt.");
});
