import socket
import threading

class Server:
    def __init__(self, host='0.0.0.0', port=5000):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen(2)
        print(f"Server listening on {host}:{port}")

        self.connections = []

    def handle_client(self, client_socket, addr):
        print(f"Connection established with {addr}")
        while True:
            try:
                header = client_socket.recv(1024).decode('utf-8')  # Receive header first
                if header.startswith("FILE"):
                    _, filename, filesize = header.split(":", 2)
                    filesize = int(filesize)
                    print(f"Receiving file {filename} of size {filesize} bytes from {addr}")

                    with open(f"received_{filename}", "wb") as f:
                        remaining = filesize
                        while remaining > 0:
                            data = client_socket.recv(min(1024, remaining))
                            f.write(data)
                            remaining -= len(data)

                    self.broadcast_file(f"received_{filename}", filename, client_socket)
                else:
                    self.broadcast(header, client_socket)  # Broadcast text messages
            except:
                print(f"Connection with {addr} lost")
                self.connections.remove(client_socket)
                client_socket.close()
                break

    def broadcast(self, message, sender):
        for conn in self.connections:
            if conn != sender:
                try:
                    conn.send(message.encode('utf-8'))
                except:
                    pass

    def broadcast_file(self, filepath, filename, sender):
        with open(filepath, "rb") as f:
            file_data = f.read()
        header = f"FILE:{filename}:{len(file_data)}".encode('utf-8')

        for conn in self.connections:
            if conn != sender:
                try:
                    conn.send(header)
                    conn.send(file_data)
                except:
                    pass

    def start(self):
        while True:
            client_socket, addr = self.server.accept()
            self.connections.append(client_socket)
            threading.Thread(target=self.handle_client, args=(client_socket, addr)).start()


if __name__ == "__main__":
    server = Server()
    server.start()
