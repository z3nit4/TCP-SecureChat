import socket
import threading
import ssl

# Connection Data
host = '0.0.0.0'
port = 8000

# TLS Context
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile="certs/cert.pem", keyfile="certs/key.pem")

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
print(f"Server listening on {host}:{port} with TLS")

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
            if clients in clients:
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
        
        # Wrap client socket with TLS
        client = context.wrap_socket(client, server_side=True)

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
