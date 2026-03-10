import socket
import threading

MY_IP = '127.0.0.1'
MY_PORT = int(input("Enter THIS server port: "))

PEER_IP = input("Enter PEER server IP: ")
PEER_PORT = int(input("Enter PEER server port: "))

clients = []   # local clients connected to this server


def handle_connection(conn):
    clients.append(conn)

    while True:
        try:
            msg = conn.recv(1024).decode()
            if not msg:
                break

            # From local client
            if msg.startswith("CLIENT:"):
                data = msg.replace("CLIENT:", "")
                print(f"[SERVER {MY_PORT}] From local client: {data}")
                forward_to_peer(data)

            # From peer server
            elif msg.startswith("SERVER:"):
                data = msg.replace("SERVER:", "")
                print(f"[SERVER {MY_PORT}] From peer server: {data}")
                send_to_local_clients(data)

        except:
            break

    clients.remove(conn)
    conn.close()


def forward_to_peer(message):
    try:
        print(f"[SERVER {MY_PORT}] Forwarding to peer server...")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((PEER_IP, PEER_PORT))
        s.send(f"SERVER:{message}".encode())
        s.close()
    except:
        print(f"[SERVER {MY_PORT}] Peer server not reachable")


def send_to_local_clients(message):
    for c in clients:
        try:
            c.send(f"DISPLAY:{message}".encode())
        except:
            pass


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((MY_IP, MY_PORT))
    server.listen()
    print(f"[SERVER {MY_PORT}] Running...")

    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_connection, args=(conn,)).start()


start_server()
