import socket
import threading
from queue import Queue

HOST = '0.0.0.0'
PORT = 6000
queue = Queue ()

def handle_client ( sock ) :
    while True :
        try :
            data = sock . recv (1024) . decode ()
            if not data :
                break

            if data.startswith("SEND:") :
                queue.put(data [5:])
                sock.send(" Message stored in queue \ n ".encode())
            elif data == " RECEIVE ":
                if not queue.empty():
                    msg = queue.get()
                    sock.send(f" Message : { msg }\ n ".encode())
            else:
                sock.send(" Queue is empty \ n ".encode())
        except:
            break

    sock.close()

server = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
server.bind((HOST , PORT ))
server.listen()

while True:
    client , addr = server.accept()
    threading.Thread (
        target = handle_client ,
        args =( client ,)
    ).start ()