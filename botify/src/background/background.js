/* global chrome */

console.log('Background script loaded');

// Listen for extension installation or update
chrome.runtime.onInstalled.addListener((details) => {
  if (details.reason === 'install') {
    console.log('Extension installed');
    // Set default settings
    chrome.storage.sync.set({
      isEnabled: true,
      apiEndpoint: 'http://localhost:8000',
    });
  } else if (details.reason === 'update') {
    console.log('Extension updated');
  }
});

// Store for current tab's context
let currentTabContext = {};

// Get cookies and page data for a tab
async function getTabContext(tab) {
  try {
    const cookies = await chrome.cookies.getAll({ url: tab.url });
    const response = await chrome.tabs.sendMessage(tab.id, { type: 'GET_PAGE_DATA' });
    
    return {
      url: tab.url,
      cookies: cookies,
      pageData: response?.data || null,
      timestamp: new Date().toISOString(),
    };
  } catch (error) {
    console.error('Error getting tab context:', error);
    return null;
  }
}

// Update context when tab changes
chrome.tabs.onActivated.addListener(async (activeInfo) => {
  const tab = await chrome.tabs.get(activeInfo.tabId);
  currentTabContext = await getTabContext(tab);
});

// Update context when page updates
chrome.runtime.onMessage.addListener(async (request, sender, sendResponse) => {
  if (request.type === 'PAGE_DATA_UPDATED') {
    const tab = await chrome.tabs.get(sender.tab.id);
    currentTabContext = await getTabContext(tab);
  }
  
  if (request.type === 'CHAT_MESSAGE') {
    // Add context to chat messages
    const messageWithContext = {
      ...request.message,
      context: currentTabContext,
    };
    
    handleChatMessage(messageWithContext)
      .then(response => sendResponse({ success: true, data: response }))
      .catch(error => {
        console.error('Error handling chat message:', error);
        sendResponse({ success: false, error: error.message });
      });
    return true;
  }
  
  if (request.type === 'GET_SETTINGS') {
    chrome.storage.sync.get(['isEnabled', 'apiEndpoint'], (result) => {
      sendResponse({ success: true, data: result });
    });
    return true;
  }
  
  if (request.type === 'API_REQUEST') {
    handleApiRequest(request)
      .then(response => {
        console.log('API Response:', response);
        sendResponse(response);
      })
      .catch(error => {
        console.error('API Error:', error);
        sendResponse({ 
          success: false, 
          error: error.message || 'Failed to process request' 
        });
      });
    return true; // Will respond asynchronously
  }
});

const API_URL = 'http://localhost:8000/api/v1';

async function handleChatMessage(message) {
  try {
    const settings = await chrome.storage.sync.get(['apiEndpoint']);
    const response = await handleApiRequest({
      endpoint: `${settings.apiEndpoint}/chat`,
      method: 'POST',
      data: message,
    });
    return response;
  } catch (error) {
    console.error('Error in handleChatMessage:', error);
    throw error;
  }
}

async function handleApiRequest(request) {
  console.log('Making API request to:', `${API_URL}${request.endpoint}`);
  console.log('Request data:', request.data);

  try {
    const response = await fetch(`${API_URL}${request.endpoint}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request.data),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return { success: true, data };
  } catch (error) {
    console.error('API request error:', error);
    throw error;
  }
}

// Handle extension icon click
chrome.action.onClicked.addListener((tab) => {
  chrome.tabs.create({
    url: chrome.runtime.getURL('index.html')
  });
});