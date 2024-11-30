interface TabContext {
  url: string;
  cookies: chrome.cookies.Cookie[];
  pageData: any;
  timestamp: string;
}

interface MessageRequest {
  type: string;
  endpoint?: string;
  data?: any;
  message?: string;
}

interface ApiResponse {
  success: boolean;
  data?: any;
  error?: string;
}

const API_URL = 'http://localhost:8000/api/v1';

// Store for current tab's context
let currentTabContext: TabContext | null = null;

// Get cookies and page data for a tab
async function getTabContext(tab: chrome.tabs.Tab): Promise<TabContext | null> {
  try {
    if (!tab.id || !tab.url) return null;

    const cookies = await chrome.cookies.getAll({ url: tab.url });
    
    try {
      const response = await chrome.tabs.sendMessage(tab.id, { type: 'GET_PAGE_DATA' });
      return {
        url: tab.url,
        cookies,
        pageData: response?.data || null,
        timestamp: new Date().toISOString(),
      };
    } catch (error) {
      console.error('Error getting page data:', error);
      return {
        url: tab.url,
        cookies,
        pageData: null,
        timestamp: new Date().toISOString(),
      };
    }
  } catch (error) {
    console.error('Error getting tab context:', error);
    return null;
  }
}

// Update context when tab changes
chrome.tabs.onActivated.addListener(async (activeInfo) => {
  try {
    const tab = await chrome.tabs.get(activeInfo.tabId);
    currentTabContext = await getTabContext(tab);
  } catch (error) {
    console.error('Error handling tab activation:', error);
    currentTabContext = null;
  }
});

// Handle messages from content script and popup
chrome.runtime.onMessage.addListener((message, _sender, sendResponse) => {
  if (message.type === 'PAGE_DATA_UPDATED' && _sender.tab?.id) {
    handlePageUpdate(_sender.tab.id).catch(console.error);
    return false;
  }

  if (message.type === 'API_REQUEST') {
    handleApiRequest(message)
      .then(response => sendResponse({ success: true, data: response }))
      .catch(error => sendResponse({ 
        success: false, 
        error: error instanceof Error ? error.message : 'Unknown error'
      }));
    return true;
  }

  if (message.type === 'CHAT_MESSAGE') {
    handleChatMessage(message.message || '')
      .then(response => sendResponse({ success: true, data: response }))
      .catch(error => sendResponse({ 
        success: false, 
        error: error instanceof Error ? error.message : 'Unknown error'
      }));
    return true;
  }

  return false;
});

async function handlePageUpdate(tabId: number): Promise<void> {
  try {
    const tab = await chrome.tabs.get(tabId);
    currentTabContext = await getTabContext(tab);
  } catch (error) {
    console.error('Error updating page data:', error);
    currentTabContext = null;
  }
}

async function handleChatMessage(message: string): Promise<any> {
  const response = await fetch(`${API_URL}/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      message,
      context: currentTabContext,
    }),
  });

  if (!response.ok) {
    throw new Error(`Chat request failed: ${response.statusText}`);
  }

  return response.json();
}

async function handleApiRequest(request: MessageRequest): Promise<any> {
  if (!request.endpoint) {
    throw new Error('No endpoint specified');
  }

  const response = await fetch(`${API_URL}${request.endpoint}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      ...request.data,
      context: currentTabContext,
    }),
  });

  if (!response.ok) {
    throw new Error(`API request failed: ${response.statusText}`);
  }

  return response.json();
}

// Handle extension icon click
chrome.action.onClicked.addListener((tab) => {
  chrome.tabs.create({
    url: chrome.runtime.getURL('index.html')
  });
});
