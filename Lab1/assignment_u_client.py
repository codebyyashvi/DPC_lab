import socket
import json

A = [
    [2, 0, 1],
    [3, 4, 2],
    [1, 2, 3]
]

B = [
    [1, 2, 3],
    [0, 1, 4],
    [5, 6, 0]
]

client_socket = socket.socket()
client_socket.connect(("localhost", 12345))

msg = client_socket.recv(1024).decode()
print(msg)

payload = json.dumps({"A": A, "B": B})
client_socket.send(payload.encode())

result = json.loads(client_socket.recv(4096).decode())

print("\nResult Matrix from Server:")
for row in result:
    print(row)

client_socket.close()
