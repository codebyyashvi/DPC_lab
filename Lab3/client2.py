import socket

SERVER_IP = '127.0.0.1'
PORT = 6000

client = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
client.connect(( SERVER_IP , PORT ))

while True :
    cmd = input( " >> " )
    client.send( cmd . encode () )
    print( client.recv(1024).decode() )