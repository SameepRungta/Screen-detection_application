document.getElementById('sendTab').addEventListener('click', () => {
    chrome.runtime.sendMessage({ action: 'sendTabInfo' });
  });
  