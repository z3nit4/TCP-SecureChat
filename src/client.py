import socket
import threading
import ssl

# Choosing Username
username = input("Choose your username: ")

# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Create SSL context for client
context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

# Wrap the socket in SSL
client = context.wrap_socket(client, server_hostname='209.38.232.217')

client.connect(('209.38.232.217', 8000))

# Listening To Server and Sending Username
def receive():
    while True:
        try:
            # Receive Message From Server
            # If 'USER' Send Username
            message = client.recv(1024).decode('ascii')
            if message == 'USER':
                client.send(username.encode('ascii'))
            else: 
                print(message)
        except:
            # Close Connection When Error
            print("An error occurred!")
            client.close()
            break

# Sending Messages To Server
def write():
    while True:
        message = f"{username}: {input('')}"
        client.send(message.encode('ascii'))

# Starting Threads For Listening And Writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()

