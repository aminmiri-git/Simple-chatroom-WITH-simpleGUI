import socket
import threading
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from datetime import datetime


class ServerGUI:

    def __init__(self, master):
        self.master = master
        self.master.title("Chatroom Server")
        self.text_area = ScrolledText(self.master, state="disabled", wrap="word")
        self.text_area.pack(expand=True, fill="both")
        self.start_server()

    def log_message(self, message):
        self.text_area.config(state="normal")
        self.text_area.insert("end", message + "\n")
        self.text_area.config(state="disabled")
        self.text_area.yview("end")

    def start_server(self):
        self.server = Server(self)
        threading.Thread(target=self.server.run).start()


class Server:

    def __init__(self, gui):
        self.gui = gui
        self.users_table = {}
        self.server_address = ('localhost', 8080)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(self.server_address)
        self.socket.listen(10)
        self.gui.log_message(f"Server started on {self.server_address}")

    def run(self):
        while True:
            connection, _ = self.socket.accept()
            threading.Thread(target=self.handle_client, args=(connection,)).start()

    def handle_client(self, connection):
        try:
            client_name = connection.recv(64).decode('utf-8')
            self.users_table[connection] = client_name
            self.gui.log_message(f"{self.get_time()} {client_name} joined the room!")
            while True:
                data = connection.recv(1024).decode('utf-8')
                if data.startswith("FILE:"):
                    file_name = data[5:]
                    file_size = int(connection.recv(1024).decode('utf-8'))
                    file_data = connection.recv(file_size)
                    self.broadcast_file(file_name, file_data, connection)
                else:
                    self.broadcast_message(data, connection)
        except:
            self.gui.log_message(f"{self.get_time()} {self.users_table[connection]} left the room!")
            self.users_table.pop(connection)
            connection.close()

    def get_time(self):
        return datetime.now().strftime("%H:%M:%S")

    def broadcast_message(self, message, owner):
        for conn in self.users_table:
            if conn != owner:
                conn.sendall(bytes(f"{self.get_time()} {self.users_table[owner]}: {message}", 'utf-8'))

    def broadcast_file(self, file_name, file_data, owner):
        for conn in self.users_table:
            if conn != owner:
                conn.sendall(bytes(f"FILE:{file_name}", 'utf-8'))
                conn.sendall(bytes(str(len(file_data)), 'utf-8'))
                conn.sendall(file_data)


if __name__ == "__main__":
    root = tk.Tk()
    app = ServerGUI(root)
    root.mainloop()
