import socket
import threading

# Connection Data
host = '127.0.0.1'
port = 8000

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
usernames = []

# Broadcast Messages To All Connected Clients
def broadcast(message):
    for client in clients:
        client.send(message)

# Handling Messages From Clients
def handle(client):
    while True:
        try:
            # Broadcasting Messages
            message = client.recv(1024)
            broadcast(message)
        except:
            # Removing And Closing Clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            username = usernames[index]
            broadcast(f"{username} left!".encode('ascii'))
            usernames.remove(username)
            break

# Receiving / Listening Function 
def receive():
    while True:
        # Accept Connection
        client, address = server.accept()
        print(f"Connected with {str(address)}")
        
        # Request And Store Username
        client.send('USER'.encode('ascii'))
        username = client.recv(1024).decode('ascii')
        usernames.append(username)
        clients.append(client)

        # Print And Broadcast Username
        print(f"Username is {username}")
        broadcast(f"{username} joined".encode('ascii'))
        client.send("Connected to server!".encode('ascii'))
                    
        # Start Handling Thread For Client)
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

receive()
