import socket
import threading
import tkinter as tk
import argparse
from tkinter import messagebox


def arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--server', dest='server', help='write server ip')
    parser.add_argument('-n', '--name', dest='name', help='write your name')
    return parser.parse_args()


arg = arguments()

SERVER_HOST = arg.server
SERVER_PORT = 12345
CLIENT_NAME = arg.name if arg.name else "anonymous"

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_HOST, SERVER_PORT))


def receive_messages():
    while True:
        message = client_socket.recv(1024).decode()
        insert_message(message, "left")


def insert_message(message, side):
    if side == "right":
        tag = "right"
        background = "lightblue"
    else:
        tag = "left"
        background = "lightgreen"

    chat_text.configure(state=tk.NORMAL)
    chat_text.tag_configure(tag, justify=tk.RIGHT if side == "right" else tk.LEFT, background=background)
    chat_text.insert(tk.END, message + "\n", tag)
    chat_text.configure(state=tk.DISABLED)
    chat_text.see(tk.END)


def send_message(event=None):
    message = entry_field.get()
    insert_message(f"you: {message}", "right")
    message = f"{CLIENT_NAME}: {message}"
    client_socket.send(message.encode())
    entry_field.delete(0, tk.END)


def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        client_window.destroy()
        client_socket.close()


client_window = tk.Tk()
client_window.title("Chat Client")
client_window.geometry("800x600")
client_window.resizable(False, False)
client_window.protocol("WM_DELETE_WINDOW", on_closing)

chat_text = tk.Text(client_window, wrap=tk.WORD)
chat_text.pack(expand=True, fill=tk.BOTH)

entry_field = tk.Entry(client_window)
entry_field.pack(expand=True, fill=tk.X)

send_button = tk.Button(client_window, text="Send", command=send_message)
send_button.pack()

client_window.bind("<Return>", send_message)

receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

client_window.mainloop()
