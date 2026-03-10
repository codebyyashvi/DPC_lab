import socket

import os

HOST = "127.0.0.1"

PORT = 5001

def main():
    pid = os.getpid()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print(f"Client PID={pid} connected. Type messages:")
        while True:
            msg = input("> ")
            s.sendall((msg + "\n").encode("utf-8"))
            print(s.recv(4096).decode("utf-8", errors="ignore"),
            end="")

if __name__ == "__main__":
    main()