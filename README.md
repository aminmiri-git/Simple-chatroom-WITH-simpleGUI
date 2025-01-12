# Simple-chatroom-WITH-simpleGUI
A simple chatroom where you can send messages and files on a shared network . Two or more PCs or Phones should be connected to the same wifi , (or a shared Hotspot).   Using tkinter  ( the standard Python interface to the Tcl/Tk GUI toolkit  )


# Overview
This project is a server-client application for LAN/WiFi communication, supporting text messaging and file sharing. The server broadcasts its presence for discovery by clients. Clients can join the server to send messages or transfer files to others on the network. The system is designed to work on both Windows and Android (via SL4A library).

# Features
Message Broadcasting: Clients can send and receive messages in real-time.
File Sharing: Clients can share files with others in the network.
Server Discovery: Clients automatically locate the server within the local network.

# How to Run

***Server
Save the server.py script to a desired directory.
Run the server script:

python server.py

The server starts on the local IP and port 8080 and listens for client connections.

***Client
Save the client.py script to a desired directory.
Run the client script:

python client.py

Enter your name when prompted.
The client automatically discovers the server and connects.
Use the interface to:
Send messages.
Send files (type send file when prompted and provide the file path)
