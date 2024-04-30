import firebase_admin
from firebase_admin import credentials
import dotenv
import os

dotenv.load_dotenv()

def init_auth():
    try:
        cred = credentials.Certificate(os.getenv("FIREBASE_KEY_PATH"))
        app = firebase_admin.initialize_app(cred)
    except Exception as e:
        print(f"Error: {str(e)}")

