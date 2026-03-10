import socket
import threading

SERVER_IP = '127.0.0.1'
PORT = 5000

def receive ( sock ) :
    while True :
        try :
            print ( sock . recv (1024) . decode () )
        except :
            break

client = socket.socket ( socket.AF_INET , socket.SOCK_STREAM )
client.connect (( SERVER_IP , PORT ) )

name = input ("Enter name : ")

threading.Thread (
    target = receive ,
    args =( client ,)
).start ()

while True :
    msg = input ()
    client.send(f" { name }: { msg } ".encode())