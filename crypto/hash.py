import hashlib

def sha_2(text):
    # Convert text to bytes
    text_bytes = bytes(text, 'utf-8')
    
    # Create SHA-256 hash object
    sha256_hash = hashlib.sha256()
    
    # Update hash object with the text bytes
    sha256_hash.update(text_bytes)
    
    # Get the hexadecimal digest of the hash
    hex_digest = sha256_hash.hexdigest()
    
    return hex_digest

import hashlib

def sha_3(text):
    # Convert text to bytes
    text_bytes = bytes(text, 'utf-8')
    
    # Create SHA-3-256 hash object
    sha3_256_hash = hashlib.sha3_256()
    
    # Update the hash object with the text bytes
    sha3_256_hash.update(text_bytes)
    
    # Get the hexadecimal digest of the hash
    hex_digest = sha3_256_hash.hexdigest()
    
    return hex_digest

def blake_2(text):
    # Convert the text to bytes
    text_bytes = bytes(text, 'utf-8')
    
    # Compute the BLAKE2b hash
    blake2b_hash = hashlib.blake2b(text_bytes)
    
    # Get the hexadecimal digest of the hash
    hex_digest = blake2b_hash.hexdigest()
    
    return hex_digest

