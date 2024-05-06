import database as db
import crypto.encryption as enc


def handler(enum_id:int, text:str, key=None, encrypt=True):
    # Fetching enum row from database
    enum_type = db.load_selected_enum_type(enum_id)

    # For AES 128 Encryption 
    if enum_id == 1 or enum_id == 2:
        result = enc.encrypt_aes(enum_id, text)

    return result