import socket
import threading
import ssl

# Choosing Username
username = input("Choose your username: ")

# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Creating Socket and Wrapping in SSL
client = ssl.wrap_socket(client, ssl_version=ssl.PROTOCOL_TLS_CLIENT, cert_reqs=ssl.CERT_NONE)

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

