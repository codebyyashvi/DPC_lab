import socket
import threading

HOST = '0.0.0.0'
PORT = 5000
clients = []

def handle_client ( client ) :
    while True :
        try :
            msg = client . recv (1024) . decode ()
            if not msg :
                break
            for c in clients :
                if c != client :
                    c.send ( msg . encode () )
        except :
            break

    clients . remove ( client )
    client . close ()

server = socket . socket ( socket . AF_INET , socket . SOCK_STREAM )
server . bind (( HOST , PORT ) )
server . listen ()

while True :
    client , addr = server . accept ()
    clients . append ( client )
    threading . Thread (
        target = handle_client ,
        args =( client ,)
    ) . start ()