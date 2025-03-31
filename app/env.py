from dotenv import load_dotenv
import os

# import the environment variables from the .env file
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
load_dotenv(dotenv_path)

# host & port (default: 0.0.0.0:8002)
HOST = os.getenv("MDB_API_HOST", "0.0.0.0")
PORT = int(os.getenv("MDB_API_PORT", 8002))

# response timeout (default: 2 seconds)
TIMEOUT = int(os.getenv("RESPONSE_TIMEOUT", 2))

# URL and token (api key) for the MdB-Data-Service
MDB_DATA_BASE_URL = os.getenv("MDB_DATA_BASE_URL", "http://127.0.0.1:8001")
MDB_DATA_READ_TOKEN = os.getenv("MDB_DATA_READ_TOKEN")