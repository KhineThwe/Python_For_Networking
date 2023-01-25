import socket

# host = socket.gethostbyname(socket.gethostname())#can get ip address automatically
import threading

HOST = '192.168.100.63'
PORT = 9090

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)  # how many unacceptable connection do we allow before we reject new ones

clients = []
nicknames = []


def broadcast(message):
    for client in clients:
        client.send(message)


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)  # broadcast messages to all the other clients
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} left the chat !'.encode("ascii"))
            nicknames.remove(nickname)
            break

def receive():
    while True:
        client, address = server.accept()
        #accept client all the time
        print(f"Connected with {str(address)}")
        #when client actually connects

        client.send('NICK'.encode("ascii"))
        nickname = client.recv(1024).decode("ascii")
        nicknames.append(nickname)
        clients.append(client)
        print(f"Nickname of the client is {nickname}")
        broadcast(f"{nickname} joined the chat!".encode("ascii"))
        #broadcast all the clients connected to the server
        client.send("Connected to the server!".encode("ascii"))

        thread = threading.Thread(target=handle,args=(client,))
        thread.start()
print("Server is listening ........")
receive()
