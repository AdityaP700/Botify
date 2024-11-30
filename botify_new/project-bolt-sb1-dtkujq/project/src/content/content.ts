interface ProductData {
  name: string;
  price: string;
  description: string;
}

interface PageData {
  title: string;
  url: string;
  product: ProductData;
}

interface MessageResponse {
  success: boolean;
  data: PageData;
}

// Listen for messages from the background script
chrome.runtime.onMessage.addListener((
  _message: { type: string },
  _sender: chrome.runtime.MessageSender,
  sendResponse: (response: MessageResponse) => void
) => {
  if (_message.type === 'GET_PAGE_DATA') {
    const pageData: PageData = {
      title: document.title,
      url: window.location.href,
      product: {
        name: getProductName(),
        price: getProductPrice(),
        description: getProductDescription(),
      },
    };
    sendResponse({ success: true, data: pageData });
  }
  return true; // Required to use sendResponse asynchronously
});

// Helper functions to extract product information
function getProductName(): string {
  const selectors = [
    '[data-testid="product-title"]',
    '.product-title',
    'h1',
    '[class*="product"][class*="title"]',
    '[class*="product"][class*="name"]'
  ];

  for (const selector of selectors) {
    const element = document.querySelector<HTMLElement>(selector);
    if (element?.textContent) {
      return element.textContent.trim();
    }
  }
  return '';
}

function getProductPrice(): string {
  const selectors = [
    '[data-testid="product-price"]',
    '.product-price',
    '.price',
    '[class*="product"][class*="price"]',
    '[class*="price"]'
  ];

  for (const selector of selectors) {
    const element = document.querySelector<HTMLElement>(selector);
    if (element?.textContent) {
      return element.textContent.trim();
    }
  }
  return '';
}

function getProductDescription(): string {
  const selectors = [
    '[data-testid="product-description"]',
    '.product-description',
    '[class*="product"][class*="description"]',
    '[class*="description"]'
  ];

  for (const selector of selectors) {
    const element = document.querySelector<HTMLElement>(selector);
    if (element?.textContent) {
      return element.textContent.trim();
    }
  }
  return '';
}

// Create and configure MutationObserver
const observerConfig: MutationObserverInit = {
  childList: true,
  subtree: true,
  attributes: true,
  characterData: true
};

// Debounce function to limit update frequency
function debounce<T extends (...args: any[]) => void>(
  func: T,
  wait: number
): (...args: Parameters<T>) => void {
  let timeout: NodeJS.Timeout | null = null;
  
  return (...args: Parameters<T>) => {
    if (timeout) {
      clearTimeout(timeout);
    }
    
    timeout = setTimeout(() => {
      func.apply(null, args);
      timeout = null;
    }, wait);
  };
}

// Debounced function to notify background script
const notifyBackgroundScript = debounce(() => {
  chrome.runtime.sendMessage({ type: 'PAGE_DATA_UPDATED' });
}, 1000);

// Create and start the observer
const observer = new MutationObserver(() => {
  notifyBackgroundScript();
});

observer.observe(document.body, observerConfig);
