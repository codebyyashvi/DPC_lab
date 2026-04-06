import socket

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 5555))
    print("Connected to Central Bank.")
    print("Commands: BALANCE | DEPOSIT <amount> | WITHDRAW <amount> | EXIT")

    while True:
        command = input("Enter command: ")
        if command.upper() == "EXIT":
            break

        client.send(command.encode('utf-8'))
        response = client.recv(1024).decode('utf-8')
        print(f"Bank : { response }\n")

        client.close()

if __name__ == "__main__":    
    start_client()