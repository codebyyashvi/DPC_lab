import socket
import threading

SERVER_IP = '127.0.0.1'
SERVER_PORT = int(input("Enter YOUR server port: "))


def receive(sock):
    while True:
        try:
            msg = sock.recv(1024).decode()
            if msg.startswith("DISPLAY:"):
                print(f"\n[CLIENT] Received: {msg.replace('DISPLAY:', '')}\n>> ", end="")
        except:
            break


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((SERVER_IP, SERVER_PORT))

threading.Thread(target=receive, args=(sock,), daemon=True).start()

while True:
    msg = input(">> ")
    print(f"[CLIENT] Sending: {msg}")
    sock.send(f"CLIENT:{msg}".encode())
