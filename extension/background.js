// background.js
chrome.runtime.onMessage.addListener((message, sender) => {
  if (message.alert) {
    chrome.action.setBadgeText({ text: "⚠️", tabId: sender.tab.id });
    chrome.action.setPopup({ tabId: sender.tab.id, popup: "popup.html" });
  }
});
