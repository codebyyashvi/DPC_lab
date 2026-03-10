import socket
import os

HOST = "127.0.0.1"

def main():
    port = int(input("Enter server port (3000/3001/3002): "))
    pid = os.getpid()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, port))
        print(f"Client PID={pid} connected to port {port}")
        print("Commands:")
        print("  add 10 20")
        print("  sub 50 15")
        print("  mul 6 7")
        print("  div 40 5")
        print("  analyze Hello Server Programming")
        print("Type 'exit' to quit\n")

        while True:
            msg = input("> ")
            if msg.lower() == "exit":
                break

            s.sendall((msg + "\n").encode())
            reply = s.recv(4096).decode()
            print(reply)


if __name__ == "__main__":
    main()
