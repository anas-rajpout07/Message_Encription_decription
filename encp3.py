import time

def get_time_key():
    return int(time.time()) % 256

def encrypt_message(message, time_key):
    encrypted = ""
    for char in message:
        encrypted += chr((ord(char) + time_key) % 256)
    return encrypted

def decrypt_message(encrypted_message, time_key):
    decrypted = ""
    for char in encrypted_message:
        decrypted += chr((ord(char) - time_key) % 256)
    return decrypted
