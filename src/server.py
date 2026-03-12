import socket
import threading
import ssl
import sqlite3
import hashlib

# Connection Data
host = '0.0.0.0'
port = 8000
DB_PATH = "database/chat.db"

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

def hash_password(password):
    return hashlib.sha256(password.encode('ascii')).hexdigest()

def register_user(username, password):
    password_hash = hash_password(password)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, password_hash)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def login_user(username, password):
    password_hash = hash_password(password)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username = ? AND password_hash = ?",
        (username, password_hash)
    )
    user = cursor.fetchone()
    conn.close()

    return user is not None


# Broadcast Messages To All Connected Clients
def broadcast(message):
    for client in clients:
        try:
            client.send(message)
        except:
            pass

# Handling Messages From Clients
def handle(client):
    while True:
        try:
            # Broadcasting Messages
            message = client.recv(1024)
            if not message:
                raise Exception("Client disconnected!")
            broadcast(message)
        except:
            # Removing And Closing Clients
            if client in clients:
                index = clients.index(client)
                username = usernames[index]

                clients.remove(client)
                usernames.remove(username)
                client.close()
                
                broadcast(f"{username} left!".encode('ascii'))
            break

# Receiving / Listening Function 
def receive():
    while True:
        # Accept Connection
        client, address = server.accept()
        print(f"Connected with {str(address)}")
        
        # Wrap client socket with TLS
        client = context.wrap_socket(client, server_side=True)

        try:
            # Receive auth message
            auth_data = client.recv(1024).decode('ascii')
            parts = auth_data.split("|")

            if len(parts) != 3:
                client.send("AUTH_FAILED".encode('ascii'))
                client.close()
                continue

            action, username, password = parts

            if action == "REGISTER":
                success = register_user(username, password)

                if success:
                    client.send("AUTH_SUCCESS".encode('ascii'))
                    client.close()   # send user back to login menu
                    print(f"Registered new user: {username}")
                    continue
                else:
                    client.send("USERNAME_EXISTS".encode('ascii'))
                    client.close()
                    continue

            elif action == "LOGIN":
                success = login_user(username, password)

                if success:
                    client.send("AUTH_SUCCESS".encode('ascii'))
                    usernames.append(username)
                    clients.append(client)

                    print(f"User logged in: {username}")
                    broadcast(f"{username} joined".encode('ascii'))

                    thread = threading.Thread(target=handle, args=(client,))
                    thread.start()
                else:
                    client.send("AUTH_FAILED".encode('ascii'))
                    client.close()
                    continue

            else:
                client.send("INVALID_ACTION".encode('ascii'))
                client.close()
                continue

        except Exception as e:
            print(f"Auth error: {e}")
            client.close()

receive()
