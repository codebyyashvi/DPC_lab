import socket
import threading
from datetime import datetime

HOST = "127.0.0.1"
PORTS = [3000, 3001, 3002]

def process_request(request):
    parts = request.split()

    if not parts:
        return "Empty request"

    command = parts[0].lower()

    if command in ("add", "sub", "mul", "div"):
        if len(parts) != 3:
            return "Error: Format -> add/sub/mul/div x y"
        try:
            a = float(parts[1])
            b = float(parts[2])

            if command == "add":
                result = a + b
            elif command == "sub":
                if a>b:
                    result = a - b
                else:
                    result = b - a
            elif command == "mul":
                result = a * b
            elif command == "div":
                if b == 0:
                    return "Error: Division by zero"
                result = a/b
            return f"Result: {result}"
        except ValueError:
            return "Error: Operands must be numbers"
    elif command == "analyze":
        text = " ".join(parts[1:])
        uppercase = text.upper()
        char_count = len(text)
        word_count = len(text.split())

        return (
            f"Uppercase: {uppercase}\n"
            f"Characters: {char_count}\n"
            f"Words: {word_count}"
        )
    else:
        return "Error: Unknown command"

def handle_client(conn, addr, port):
    print(f"[+] Client {addr} connected on port {port}")
    with conn:
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    break
                msg = data.decode().strip()
                print(f"[{port}] {addr} -> {msg}")
                response = process_request(msg)
                timestamp = datetime.now().strftime("%H:%M:%S")
                reply = f"[{timestamp}] {response}\n"
                conn.sendall(reply.encode())
            except ConnectionResetError:
                break

    print(f"[-] Client {addr} disconnected from port {port}")

def start_server(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, port))
    server.listen()
    print(f"Server running on {HOST}:{port}\n")
    while True:
        conn, addr = server.accept()
        threading.Thread(
            target=handle_client,
            args=(conn, addr, port),
            daemon=True
        ).start()

def main():
    for port in PORTS:
        threading.Thread(
            target=start_server,
            args=(port,),
            daemon=True
        ).start()
    while True:
        pass

if __name__ == "__main__":
    main()
