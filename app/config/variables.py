from dotenv import load_dotenv
import os

load_dotenv()

MONGO_CONFIG = {
    "HOST": os.getenv("MONGODB_URL"),
    "DBNAME": os.getenv("MONGODB_NAME")
}

API_KEYS = os.getenv("API_KEYS").split()

SEARCH_QUERY = os.getenv("SEARCH_QUERY")

REFRESH_INTERVAL = int(os.getenv("REFRESH_INTERVAL"))
