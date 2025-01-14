import tkinter as tk
from tkinter import messagebox
from HE_algo import HoneyEncryption

# Functions for encryption and decryption
def encrypt_message():
    password = key_entry.get()
    plaintext = text_entry.get("1.0", tk.END).strip()

    if not password or not plaintext:
        messagebox.showerror("Error", "Key and text are required for encryption.")
        return

    decoys = [
        "This is a random decoy message.",
        "This is another decoy to confuse attackers.",
        "Unrelated message that looks like the real one."
    ]

    honey_encryption = HoneyEncryption(password)
    encrypted_data = honey_encryption.encrypt(plaintext, decoys)

    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, encrypted_data)

def decrypt_message():
    password = key_entry.get()
    encrypted_text = text_entry.get("1.0", tk.END).strip()

    if not password or not encrypted_text:
        messagebox.showerror("Error", "Key and cipher text are required for decryption.")
        return

    try:
        encrypted_data = eval(encrypted_text)
        honey_encryption = HoneyEncryption(password)
        decrypted_messages = honey_encryption.decrypt(encrypted_data, password)

        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, "\n".join(decrypted_messages))
    except Exception as e:
        messagebox.showerror("Error", f"Decryption failed: {e}")

# UI Setup
app = tk.Tk()
app.title("Honey Encryption")

# Key Input
tk.Label(app, text="Key:").grid(row=0, column=0, sticky=tk.W)
key_entry = tk.Entry(app, show="*", width=40)
key_entry.grid(row=0, column=1, padx=10, pady=5)

# Text Input
tk.Label(app, text="Text (for encryption) or Cipher Text (for decryption):").grid(row=1, column=0, sticky=tk.W)
text_entry = tk.Text(app, height=10, width=40)
text_entry.grid(row=1, column=1, padx=10, pady=5)

# Result Display
tk.Label(app, text="Result:").grid(row=2, column=0, sticky=tk.W)
result_text = tk.Text(app, height=10, width=40, state=tk.NORMAL)
result_text.grid(row=2, column=1, padx=10, pady=5)

# Buttons
encrypt_button = tk.Button(app, text="Encrypt", command=encrypt_message)
encrypt_button.grid(row=3, column=0, pady=10)

decrypt_button = tk.Button(app, text="Decrypt", command=decrypt_message)
decrypt_button.grid(row=3, column=1, pady=10)

app.mainloop()
