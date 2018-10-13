const serverAddress = "http://127.0.0.1:5000";
chrome.tabs.onUpdated.addListener(function(id, info, tab) {
  if (tab.url.toLowerCase().indexOf("youtube.com") > -1) {
    chrome.pageAction.show(tab.id);
  }
});