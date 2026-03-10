import socket
import threading

MY_IP = '127.0.0.1'
MY_PORT = int(input("Enter YOUR server port: "))

PEER_IP = input("Enter PEER server IP: ")
PEER_PORT = int(input("Enter PEER server port: "))

def server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((MY_IP, MY_PORT))
    s.listen()
    print(f"[SERVER {MY_PORT}] Running...")

    while True:
        conn, addr = s.accept()
        threading.Thread(target=handle_connection, args=(conn,)).start()

def handle_connection(conn):
    try:
        msg = conn.recv(1024).decode()

        if msg.startswith("CLIENT:"):
            content = msg.replace("CLIENT:", "")
            print(f"[NODE SERVER] Received from client: {content}")
            forward_to_peer(content)

        elif msg.startswith("SERVER:"):
            content = msg.replace("SERVER:", "")
            print(f"[NODE SERVER] Received from peer server: {content}")

    except:
        pass
    conn.close()

# ----------- SERVER → SERVER -------------
def forward_to_peer(message):
    try:
        print("[NODE SERVER] Forwarding to peer server...")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((PEER_IP, PEER_PORT))
        s.send(f"SERVER:{message}".encode())
        s.close()
    except:
        print("[NODE SERVER] Peer server unreachable")

# ---------------- CLIENT ----------------
def client():
    while True:
        msg = input(">> ")
        print(f"[NODE CLIENT] Sending: {msg}")

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((MY_IP, MY_PORT))
        s.send(f"CLIENT:{msg}".encode())
        s.close()

# ---------------- MAIN ------------------
threading.Thread(target=server, daemon=True).start()
client()
