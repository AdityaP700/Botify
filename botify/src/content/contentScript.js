/* global chrome */

// E-commerce site parsers
const siteParsers = {
  amazon: {
    productTitle: () => document.getElementById('productTitle')?.textContent.trim(),
    price: () => document.querySelector('.a-price-whole')?.textContent,
    description: () => document.getElementById('productDescription')?.textContent.trim(),
    rating: () => document.querySelector('.a-icon-star')?.textContent,
  },
  ebay: {
    productTitle: () => document.querySelector('h1.x-item-title__mainTitle')?.textContent.trim(),
    price: () => document.querySelector('div.x-price-primary')?.textContent,
    description: () => document.querySelector('.x-item-description')?.textContent.trim(),
    rating: () => document.querySelector('.x-star-rating')?.textContent,
  },
  // Add more e-commerce sites as needed
};

// Extract page data based on URL
function extractPageData() {
  const url = window.location.href;
  let siteType = null;
  
  // Determine site type
  if (url.includes('amazon')) siteType = 'amazon';
  else if (url.includes('ebay')) siteType = 'ebay';
  // Add more site detection logic
  
  if (!siteType || !siteParsers[siteType]) return null;
  
  const parser = siteParsers[siteType];
  return {
    url,
    siteType,
    productInfo: {
      title: parser.productTitle(),
      price: parser.price(),
      description: parser.description(),
      rating: parser.rating(),
    },
    timestamp: new Date().toISOString(),
  };
}

// Listen for messages from background script
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.type === 'GET_PAGE_DATA') {
    const pageData = extractPageData();
    sendResponse({ success: true, data: pageData });
  }
  return true;
});

// Observe page changes
const observer = new MutationObserver(() => {
  const pageData = extractPageData();
  if (pageData) {
    chrome.runtime.sendMessage({
      type: 'PAGE_DATA_UPDATED',
      data: pageData,
    });
  }
});

observer.observe(document.body, {
  childList: true,
  subtree: true,
});
