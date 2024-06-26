import dotenv
import os

dotenv.load_dotenv()

def get_base_url(host_address:str):
    host_address = host_address.split(":")
    host = host_address[0]

    try:
        port = host_address[1]
    except IndexError:
        port = ""
        
    host_base_url = f"http://{host}:{port}"
    return host_base_url


def get_firebase_key_path():
    return os.getenv("FIREBASE_KEY_PATH")

def get_firebase_web_api_key():
    return os.getenv("FIREBASE_WEB_API_KEY")

def get_app_secret_key():
    return os.getenv("APP_SECRET_KEY")

def get_celery_broker_url():
    return os.getenv("CELERY_BROKER_URL")

def get_celery_result_backend():
    return os.getenv("CELERY_RESULT_BACKEND")
