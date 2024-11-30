# Botify

A smart e-commerce assistant that helps users make informed shopping decisions through AI-powered product recommendations and comparisons.

## Features

- **Smart Product Recommendations**: Helps users find the best products based on their specific needs and use cases
- **Product Comparisons**: Provides detailed comparisons between similar products
- **Multi-Platform Support**: Works seamlessly on major e-commerce platforms:
  - Amazon
  - eBay
  - Flipkart

## Architecture

### Backend (Python)
- Built with FastAPI framework
- RESTful API architecture
- CORS enabled for secure cross-origin requests
- Health check endpoint for monitoring

### Frontend (Chrome Extension)
- Built using React
- Manifest V3 compliant
- Content scripts for e-commerce site integration
- Background service worker for persistent functionality

## Technical Stack

### Backend
- Python
- FastAPI
- Uvicorn (ASGI server)

### Frontend
- React.js
- Tailwind CSS
- Chrome Extension APIs

## Installation

1. **Backend Setup**
```bash
cd python-backend
# Install dependencies (requirements.txt should be present)
python -m pip install -r requirements.txt
# Run the server
python -m uvicorn app.main:app --reload
```

2. **Extension Setup**
```bash
cd botify
# Install dependencies
npm install
# Build the extension
npm run build
```

3. **Load the Extension**
- Open Chrome/Edge
- Go to Extensions (chrome://extensions/)
- Enable Developer Mode
- Click "Load unpacked"
- Select the `botify/build` directory

## Permissions

The extension requires the following permissions:
- cookies: For session management
- activeTab: For current tab interaction
- storage: For saving user preferences
- scripting: For dynamic content injection
- tabs: For tab management
- webNavigation: For navigation events

## API Endpoints

- Base URL: `/api/v1`
- Health Check: `/health`
- OpenAPI Documentation: `/api/v1/openapi.json`

## Development

The project follows a modular architecture:
- `/python-backend`: Contains the FastAPI backend service
- `/botify`: Contains the Chrome extension frontend
- Configuration files in root directory for Tailwind CSS and PostCSS

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## License

This project is licensed under the terms found in the LICENSE file.

## Host Permissions

The extension can interact with:
- amazon.com
- ebay.com
- flipkart.com
- localhost:8000 (development backend)
- localhost:3000 (development frontend)
