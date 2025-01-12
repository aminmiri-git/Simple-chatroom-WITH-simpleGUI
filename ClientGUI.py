import socket
import threading
import tkinter as tk
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText
import os


class ClientGUI:

    def __init__(self, master, client_name):
        self.master = master
        self.master.title(f"Chatroom - {client_name}")
        self.client_name = client_name

        self.text_area = ScrolledText(self.master, state="disabled", wrap="word")
        self.text_area.pack(expand=True, fill="both")

        self.entry_frame = tk.Frame(self.master)
        self.entry_frame.pack(fill="x")

        self.entry = tk.Entry(self.entry_frame)
        self.entry.pack(side="left", fill="x", expand=True, padx=5, pady=5)

        self.send_button = tk.Button(self.entry_frame, text="Send", command=self.send_message)
        self.send_button.pack(side="right", padx=5, pady=5)

        self.file_button = tk.Button(self.master, text="Send File", command=self.send_file)
        self.file_button.pack(fill="x", padx=5, pady=5)

        self.client = Client(self.client_name, self)
        threading.Thread(target=self.client.receive_messages).start()

    def log_message(self, message):
        self.text_area.config(state="normal")
        self.text_area.insert("end", message + "\n")
        self.text_area.config(state="disabled")
        self.text_area.yview("end")

    def send_message(self):
        message = self.entry.get()
        if message:
            self.client.send_message(message)
            self.entry.delete(0, tk.END)

    def send_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.client.send_file(file_path)


class Client:

    def __init__(self, client_name, gui):
        self.client_name = client_name
        self.gui = gui
        self.server_address = ('localhost', 8080)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(self.server_address)
        self.socket.sendall(bytes(self.client_name, 'utf-8'))

    def send_message(self, message):
        self.socket.sendall(bytes(message, 'utf-8'))

    def send_file(self, file_path):
        if os.path.exists(file_path):
            file_name = os.path.basename(file_path)
            file_size = os.path.getsize(file_path)
            self.socket.sendall(bytes(f"FILE:{file_name}", 'utf-8'))
            self.socket.sendall(bytes(str(file_size), 'utf-8'))
            with open(file_path, 'rb') as f:
                self.socket.sendall(f.read())
            self.gui.log_message(f"File '{file_name}' sent successfully.")

    def receive_messages(self):
        while True:
            try:
                data = self.socket.recv(1024).decode('utf-8')
                if data.startswith("FILE:"):
                    file_name = data[5:]
                    file_size = int(self.socket.recv(1024).decode('utf-8'))
                    file_data = self.socket.recv(file_size)
                    with open(f"received_{file_name}", 'wb') as f:
                        f.write(file_data)
                    self.gui.log_message(f"File '{file_name}' received and saved as 'received_{file_name}'.")
                else:
                    self.gui.log_message(data)
            except:
                break


if __name__ == "__main__":
    client_name = input("Enter your name: ")
    root = tk.Tk()
    app = ClientGUI(root, client_name)
    root.mainloop()
