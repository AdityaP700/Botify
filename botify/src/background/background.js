// Handle API calls in extension mode
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.type === 'API_REQUEST') {
    fetch('http://localhost:8000/groq', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Origin': chrome.runtime.getURL(''),
      },
      body: JSON.stringify(request.data)
    })
    .then(response => response.text())
    .then(data => {
      sendResponse({ success: true, data });
    })
    .catch(error => {
      console.error('Error:', error);
      sendResponse({ success: false, error: error.message });
    });

    return true; // Required to use sendResponse asynchronously
  }
});