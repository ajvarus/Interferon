import dotenv
import os

dotenv.load_dotenv()

def get_base_url():
    return os.getenv("HOST_BASE_URL")

def get_firebase_key_path():
    return os.getenv("FIREBASE_KEY_PATH")