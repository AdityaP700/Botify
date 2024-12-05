import logging
import os

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if os.getenv("ENVIRONMENT") == "development" else logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)
