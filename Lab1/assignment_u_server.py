import socket
import threading
import json

def multiply_matrices(A, B):
    rowsA = len(A)
    colsA = len(A[0])
    colsB = len(B[0])

    result = [[0 for _ in range(colsB)] for _ in range(rowsA)]

    for i in range(rowsA):
        for j in range(colsB):
            for k in range(colsA):
                result[i][j] += A[i][k] * B[k][j]

    return result


def handle_client(client_socket, client_address):
    print(f"[NEW CONNECTION] {client_address} connected.")

    client_socket.send("Send matrices in JSON format".encode())

    try:
        data = client_socket.recv(4096).decode()
        matrices = json.loads(data)

        A = matrices["A"]
        B = matrices["B"]

        print(f"Received matrices from {client_address}")

        result = multiply_matrices(A, B)

        client_socket.send(json.dumps(result).encode())

    except Exception as e:
        client_socket.send("Error processing matrices".encode())
        print("Error:", e)

    client_socket.close()
    print(f"[DISCONNECTED] {client_address} disconnected.")


# ---------------- MAIN SERVER ----------------

server_socket = socket.socket()
server_socket.bind(("localhost", 12345))
server_socket.listen(5)

print("Matrix Multiplication Socket Server running...")

while True:
    client_socket, client_address = server_socket.accept()

    thread = threading.Thread(
        target=handle_client,
        args=(client_socket, client_address)
    )
    thread.start()
