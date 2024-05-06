from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

def encrypt_aes(enum_id:int, text:str, key = None, encrypt:bool = True):
    # Key and IV setup
    if enum_id == 1:
        key = get_random_bytes(16)  # AES-128 uses a 16-byte key
    elif enum_id == 2:
        key = get_random_bytes(32)  # AES-256 uses a 32-byte key
    
    iv = get_random_bytes(16)   # Initialization vector should also be 16 bytes for AES

    if encrypt:
        # Encryptor setup
        encryptor = AES.new(key, AES.MODE_CBC, iv)

        # Data to be encrypted
        plaintext_encoded = str(text).encode()
        padded_data = pad(plaintext_encoded, AES.block_size)  # Padding data to make it compatible with block size

        # Perform encryption
        encrypted_data = encryptor.encrypt(padded_data)
        return encrypted_data.hex()
    else:
        # Decryptor setup
        decryptor = AES.new(key, AES.MODE_CBC, iv)

        # Perform decryption
        decrypted_data = decryptor.decrypt(encrypted_data)
        original_data = unpad(decrypted_data, AES.block_size)  # Remove padding after decryption
        return original_data.decode()