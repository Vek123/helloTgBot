import os

from dotenv import load_dotenv
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent

# Load environment variables
dotenv_path = BASE_DIR / ".env"

if dotenv_path.exists():
    load_dotenv(dotenv_path)

# Creating constants
BOT_TOKEN = os.environ.get("BOT_TOKEN")
MONGODB_CLUSTER_URL = os.environ.get("TG_DB_URL", "No URL!")
CURRENCY_API_TOKEN = os.environ.get("CURRENCY_API_TOKEN")
CURRENCY_API_URL = (
    "https://api.currencyapi.com/v3/latest?apikey=%s&currencies=RUB"
    % CURRENCY_API_TOKEN
)
