import random
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os
import base64

# Utility: Generate a strong key from a password using PBKDF2
def derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100_000,
    )
    return kdf.derive(password.encode())

# Utility: Generate a decoy message that matches the length of the original message
def generate_decoy(original_message: str) -> str:
    """
    Generates a decoy message that matches the length of the original message.
    Creates realistic sentences combined into a paragraph.
    """
    # Length of the original message
    target_length = len(original_message)

    # Predefined sentences for decoy generation
    sentence_pool = [
        "This document contains sensitive information.",
        "Access is restricted to authorized personnel only.",
        "Please ensure the confidentiality of this data.",
        "Unauthorized access is strictly prohibited.",
        "Encryption is used to secure all sensitive information.",
        "This message is protected by advanced security protocols.",
        "Secure communication is critical to maintaining privacy.",
        "All data must be handled with the utmost care."
    ]

    # Combine sentences into a paragraph
    decoy_message = " ".join(random.choices(sentence_pool, k=10))  # Combine 10 random sentences

    # Adjust the length of the decoy message
    if len(decoy_message) > target_length:
        decoy_message = decoy_message[:target_length]  # Trim if too long
    else:
        decoy_message += ' ' * (target_length - len(decoy_message))  # Pad with spaces if too short

    return decoy_message

# Core Honey Encryption Functions
class HoneyEncryption:
    def __init__(self, password: str):      #constructor (__init__ method) of the HoneyEncryption class
        self.password = password
        self.salt = os.urandom(16)  # #randomly generated 16-byte salt for key generation  #✅ensuring that even if the same password is used multiple times, the derived keys will differ
        self.key = derive_key(password, self.salt)  # Derived key

    def encrypt(self, plaintext: str, decoys: list[str]) -> dict:
        """
        Encrypt plaintext and associate with decoys.
        Returns a dictionary containing ciphertext and associated decoys.
        """
        # Generate a random Initialization Vector (IV)
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(self.key), modes.CFB(iv))
        encryptor = cipher.encryptor()

        # Encrypt the plaintext
        ciphertext = encryptor.update(plaintext.encode()) + encryptor.finalize()

        # Add decoys
        all_messages = [plaintext] + decoys
        decoy_ciphertexts = []
        for message in all_messages:
            cipher = Cipher(algorithms.AES(self.key), modes.CFB(iv))
            encryptor = cipher.encryptor()
            decoy_ciphertext = encryptor.update(message.encode()) + encryptor.finalize()
            decoy_ciphertexts.append(base64.b64encode(decoy_ciphertext).decode())

        return {
            "salt": base64.b64encode(self.salt).decode(),
            "iv": base64.b64encode(iv).decode(),
            "ciphertexts": decoy_ciphertexts,  # Includes real ciphertext and decoys
        }

    def decrypt(self, input_data: dict, attempt_key: str) -> list:
        """
        Attempt decryption with a given key and identify the correct message.
        If decryption fails, return random decoys that match the length and type of the original message.
        """
        # Re-derive the key using the attempted password
        try:
            derived_key = derive_key(attempt_key, base64.b64decode(input_data["salt"]))
        except Exception as e:
            return ["Invalid Key"]

        plausible_messages = []
        for encoded_ciphertext in input_data["ciphertexts"]:
            iv = base64.b64decode(input_data["iv"])
            cipher = Cipher(algorithms.AES(derived_key), modes.CFB(iv))
            decryptor = cipher.decryptor()

            # Attempt to decrypt
            try:
                decrypted = decryptor.update(base64.b64decode(encoded_ciphertext)) + decryptor.finalize()
                plausible_messages.append(decrypted.decode('utf-8'))
            except Exception as e:
                # Generate a valid decoy message when decryption fails
                plausible_messages.append(generate_decoy(input_data["ciphertexts"][0]))

        return plausible_messages


# Test: Encrypt and Decrypt with Enhanced Decoys
password = "strongpassword123"
plaintext = "This is a confidential paragraph. It contains sensitive data that needs protection."
decoys = [
    "This is a random decoy message.",
    "This is another decoy to confuse attackers.",
    "Unrelated message that looks like the real one."
]

# Initialize Honey Encryption System
honey_encryption = HoneyEncryption(password)

# Encrypt the data
encrypted_data = honey_encryption.encrypt(plaintext, decoys)

# Attempt decryption with correct and incorrect keys
correct_attempt = honey_encryption.decrypt(encrypted_data, "strongpassword123")
incorrect_attempt = honey_encryption.decrypt(encrypted_data, "wrongpassword456")

print("Encrypted Data:", encrypted_data)
print("\nDecryption with Correct Key:", correct_attempt)
print("\nDecryption with Incorrect Key:", incorrect_attempt)