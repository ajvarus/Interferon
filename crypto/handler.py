import database as db
import crypto.encryption as enc
import crypto.hash as hash


def crypto_handler(enum_id:int, text:str, key=None, encrypt=True):
    # Fetching enum row from database
    enum_type = db.load_selected_enum_type(enum_id)

    # For AES 128 Encryption 
    if enum_id == 1 or enum_id == 2:
        result = enc.encrypt_aes(enum_id, text)
    elif enum_id == 3:
        result = hash.sha_2(text)
    elif enum_id == 4:
        result = hash.sha_3(text)
    elif enum_id == 5:
        result = hash.blake_2(text)

    return result