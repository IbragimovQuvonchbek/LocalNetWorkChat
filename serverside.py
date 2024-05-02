import socket
import threading

SERVER_HOST = '0.0.0.0'
SERVER_PORT = 12345

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen()

clients = []


def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
        except ConnectionResetError:
            clients.remove(client_socket)
            break
        if not message:
            break
        for client in clients:
            if client != client_socket:
                client.send(message.encode())


def accept_clients():
    print("Server started.")
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"[*] Accepted connection from {client_address}")
        clients.append(client_socket)
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()


print("Do you want to start the server?[y/n]")
choice = input("> ")
if choice == "y":
    accept_clients()
