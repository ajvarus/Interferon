import firebase_admin
from firebase_admin import credentials
import dotenv
import os



def init_auth():

    dotenv.load_dotenv()


    try:
        cred = credentials.Certificate(os.getenv("FIREBASE_KEY_PATH"))
        firebase_admin.initialize_app(cred)
    except Exception as e:
        print(f"Error: {str(e)}")

