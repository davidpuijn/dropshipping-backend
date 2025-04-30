chrome.tabs.query({ active: true, currentWindow: true }, tabs => {
  const url = new URL(tabs[0].url).hostname;

  chrome.storage.local.get(['siteDB'], res => {
    const siteDB = res.siteDB || {};
    const status = siteDB[url];
    const result = document.getElementById('result');

    if (status === 'dropshipping') {
      result.innerHTML = '<div class="alert">Waarschuwing: Mogelijke Dropshipping-site</div>';
    } else if (status === 'safe') {
      result.innerHTML = '<div class="safe">Deze site is als veilig gemarkeerd</div>';
    } else {
      result.innerHTML = 'Geen data voor deze site.';
    }
  });

  document.getElementById('feedback-dropshipping').onclick = () => {
    chrome.runtime.sendMessage({ action: 'markSite', status: 'dropshipping', url });
    fetch('https://dropshipping-backend.onrender.com/report', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': "{DEDC9729/12BZPM@}"
      },
      body: JSON.stringify({ url, status: 'dropshipping' })
    });
  };

  document.getElementById('feedback-safe').onclick = () => {
    chrome.runtime.sendMessage({ action: 'markSite', status: 'safe', url });
    fetch('https://dropshipping-backend.onrender.com/report', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': "{DEDC9729/12BZPM@}"
      },
      body: JSON.stringify({ url, status: 'safe' })
    });
  };
});
