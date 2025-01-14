from HE_algo import HoneyEncryption

# Parameters for testing
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

# Display encrypted data
print("Encrypted Data:", encrypted_data)

# Attempt decryption with the correct key
correct_attempt = honey_encryption.decrypt(encrypted_data, "strongpassword123")
print("\nDecryption with Correct Key:", correct_attempt)

# Attempt decryption with an incorrect key
incorrect_attempt = honey_encryption.decrypt(encrypted_data, "wrongpassword456")
print("\nDecryption with Incorrect Key:", incorrect_attempt)
