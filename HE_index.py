from HE_algo import HoneyEncryption

# Functions for encryption and decryption
def encrypt_message(password:str,plaintext:str):

    if not password or not plaintext:
        print("Error", "Key and text are required for encryption.")
        return

    decoys = [
        "This is a random decoy message.",
        "This is another decoy to confuse attackers.",
        "Unrelated message that looks like the real one."
    ]

    honey_encryption = HoneyEncryption(password)
    encrypted_data = honey_encryption.encrypt(plaintext, decoys)

    return encrypted_data

def decrypt_message(password:str,encrypted_text):

    if not password or not encrypted_text:
        print("Error", "Key and cipher text are required for decryption.")
        return

    try:
        encrypted_data = eval(encrypted_text)
        honey_encryption = HoneyEncryption(password)
        decrypted_messages = honey_encryption.decrypt(encrypted_data, password)
        return decrypted_messages
    
    except Exception as e:
        print("Error", f"Decryption failed: {e}")
        return
