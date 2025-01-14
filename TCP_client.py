import socket
import threading
import tkinter as tk
from tkinter import filedialog
from HE_index import encrypt_message



class Client:
    def __init__(self, host='192.168.31.77', port=5000):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))
        print(f"Connected to server {host}:{port}")

    def send_message(self, message):
        # Ensure message is a string before encoding it
        if isinstance(message, dict):  # if the message is a dictionary, convert it to a string (e.g., using JSON)
            import json
            message = json.dumps(message)  # Convert dict to string (JSON format)
        
        self.client.send(message.encode('utf-8'))


    def send_file(self, filepath):
        filename = filepath.split("/")[-1]
        with open(filepath, "rb") as f:
            file_data = f.read()

        header = f"FILE:{filename}:{len(file_data)}".encode('utf-8')
        self.client.send(header)
        self.client.send(file_data)

    def receive_messages(self, callback):
        while True:
            try:
                header = self.client.recv(1024).decode('utf-8')
                if header.startswith("FILE"):
                    _, filename, filesize = header.split(":", 2)
                    filesize = int(filesize)

                    with open(f"downloaded_{filename}", "wb") as f:
                        remaining = filesize
                        while remaining > 0:
                            data = self.client.recv(min(1024, remaining))
                            f.write(data)
                            remaining -= len(data)
                    callback(f"Received file: downloaded_{filename}")
                else:
                    callback(header)
            except:
                print("Connection to server lost")
                break


class ChatApp:
    def __init__(self, root, client):
        self.client = client

        self.root = root
        self.root.title("Chat App")

        self.chat_area = tk.Text(root, state='disabled', wrap='word', width=50, height=20)
        self.chat_area.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.message_entry = tk.Entry(root, width=40)
        self.message_entry.grid(row=1, column=0, padx=10, pady=10)

        self.send_button = tk.Button(root, text="Send", command=self.send_message)
        self.send_button.grid(row=1, column=1, padx=10, pady=10)

        self.file_button = tk.Button(root, text="Send File", command=self.send_file)
        self.file_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        threading.Thread(target=self.receive_messages).start()

    def send_message(self):
        HE_password="pass1234"
        message = self.message_entry.get()
        # message = str(message)  # Convert message to string

        if message:
            encrypted_message=encrypt_message(HE_password,message)

            self.client.send_message(encrypted_message)
            self.display_message(f"You: {message}")
            self.message_entry.delete(0, tk.END)

    def send_file(self):
        filepath = filedialog.askopenfilename()
        if filepath:
            self.client.send_file(filepath)
            self.display_message(f"You sent a file: {filepath.split('/')[-1]}")

    def receive_messages(self):
        def callback(message):
            self.display_message(message)
        self.client.receive_messages(callback)

    def display_message(self, message):
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, message + '\n')
        self.chat_area.config(state='disabled')
        self.chat_area.see(tk.END)


if __name__ == "__main__":
    client = Client()
    root = tk.Tk()
    app = ChatApp(root, client)
    root.mainloop()
