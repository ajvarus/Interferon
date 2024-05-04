from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA256
import os

def generate_master_key(password:str):
    master_password = password.encode()
    salt = os.urandom(16)  # Generate a random salt
    master_key = PBKDF2(master_password, 
                        salt, 
                        dkLen=32, 
                        count=100000, 
                        hmac_hash_module=SHA256)
    
    return master_key
