import socket
import threading

# Shared state
balance = 1000.0
# Lock for synchronization to prevent race conditions
lock = threading.Lock()

def handle_client(client_socket, address):
    global balance  
    print(f"[NEW CONNECTION] Client { address } connected.")

    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message :
                break
            command = message.split()
            action = command[0].upper()

            # Critical Section starts here
            with lock:
                if action == "BALANCE":
                    response = f"Current Balance : ${ balance :.2f}"
                elif action == "DEPOSIT":
                    amount = float(command[1])
                    balance += amount
                    response = f"Deposited ${amount:.2f}.New Balance:${balance:.2f}"
                elif action == "WITHDRAW":
                    amount = float(command[1])
                    if balance >= amount:
                        balance -= amount
                        response = f"Withdrew ${amount:.2f}.New Balance : ${balance:.2f}"
                    else:
                        response = "Insufficient funds!"
                else :
                        response = " Invalid command."
            # Critical Section ends here
            client_socket.send(response.encode('utf-8'))
        except Exception as e:
            print(f"[ERROR]{e}")
            break

    print(f"[DISCONNECT] Client { address } disconnected.")
    client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 5555))
    server.listen(5)
    print("[STARTED] Bank Server is listening on port 5555...")

    while True:
        client_socket, address = server.accept()
        thread = threading.Thread(target = handle_client, args=(client_socket, address))
        thread.start()
        print(f"[ ACTIVE CONNECTIONS ] {threading.active_count() - 1}")

if __name__ == "__main__":
    start_server()