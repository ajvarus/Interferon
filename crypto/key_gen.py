from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA256
import os
import base64

def generate_master_key(password:str) -> bytes:
    master_password = password.encode()
    salt = os.urandom(16)  # Generate a random salt
    master_key = PBKDF2(master_password, 
                        salt, 
                        dkLen=32, 
                        count=100000, 
                        hmac_hash_module=SHA256)
    
    return master_key

def generate_derived_key(master_key:str) -> bytes:
    master_password = master_key.encode()
    salt = os.urandom(16)  # Generate a random salt
    derived_key = PBKDF2(master_password, 
                        salt, 
                        dkLen=32, 
                        count=100000, 
                        hmac_hash_module=SHA256)
    
    return derived_key

def bytes_to_string(key: bytes) -> str: 
    b64_encoded_key = base64.b64encode(key)
    key_string = b64_encoded_key.decode()
    
    return key_string

def string_to_bytes(key_string: str) -> bytes: 
    b64_decoded_key = base64.b64decode(key_string)
    
    return b64_decoded_key

