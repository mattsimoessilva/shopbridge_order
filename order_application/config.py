import os

# Database configuration
DATABASE_NAME = os.getenv("DATABASE_NAME", "database.db")
DATABASE_PATH = os.path.join(os.path.dirname(__file__), "storage", DATABASE_NAME)
DATABASE_URL = f"sqlite+aiosqlite:///{DATABASE_PATH}"

# App configuration
HOST = os.getenv("ORDER_SERVICE_HOST", "0.0.0.0")
PORT = int(os.getenv("ORDER_SERVICE_PORT", 3000))
DEBUG = os.getenv("ORDER_SERVICE_DEBUG", "true").lower() == "true"

# Service URLs
PRODUCT_SERVICE_URL = os.getenv("PRODUCT_SERVICE_URL", "http://localhost:5000/api/")
LOGISTICS_SERVICE_URL = os.getenv("LOGISTICS_SERVICE_URL", "http://localhost:8000/api/")
