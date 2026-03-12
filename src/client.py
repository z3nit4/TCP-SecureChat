import socket
import threading
import ssl

# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Create SSL context for client
context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

# Wrap the socket in SSL
client = context.wrap_socket(client, server_hostname='209.38.232.217')
client.connect(('209.38.232.217', 8000))

while True:
    print("\n--- Secure Chat ---")
    print("Welcome. Select 1 to login if you're a returning user. Otherwise, select 2 to register.")
    print("1. Login")
    print("2. Register")
    choice = input("Choose an option: ")

    # ---------------- LOGIN USER ----------------
    if choice == "1":
        
         # Reset attempts each time login is selected
        attempts = 3
        
         # Login loop (limited attempts)
        while attempts > 0:
            try:
                print("\n--- Secure Login ---")
                
                username = input("Enter username: ").strip()
                password = input("Enter password: ").strip()

                # Prevent empty username or password
                if not username or not password:
                    print("Username and password cannot be empty.")
                    continue

                auth_message = f"LOGIN|{username}|{password}"
                client.send(auth_message.encode("ascii"))

                response = client.recv(1024).decode("ascii")
                print(response)

                if response == "AUTH_SUCCESS":
                    print("Login successful!")
                    break
                else: 
                    attempts -= 1
                    print(f"{response} Attempts left: {attempts}")

            except ValueError as e:
                print("Error:", e)

            except KeyboardInterrupt:
                print("\nLogin cancelled by user.")
                break

            except Exception as e:
                print("Unexpected error occurred:", e)

        
        if attempts == 0:
            print("Account locked. Too many failed attempts.")
            client.close()
            exit()

        if response == "AUTH_SUCCESS":
            break


    # ---------------- REGISTER USER ----------------
    elif choice == "2":
        try:
            username = input("Enter username: ").strip()
            password = input("Enter password: ").strip()

            if not username or not password:
                print("Username and password cannot be empty.")
                continue

            auth_message = f"REGISTER|{username}|{password}"
            client.send(auth_message.encode("ascii"))

            response = client.recv(1024).decode("ascii")
            print(response)

            if response == "AUTH_SUCCESS":
                print("Registration successful! You may now login.")
                continue
            else:
                print(response)

        except ValueError as e:
            print("Error:", e)

        except KeyboardInterrupt:
            print("\nRegistration cancelled by user.")
            client.close()
            exit()
        
        except Exception as e:
            print("Unexpected error occurred:", e)

    else:
        print("Invalid option.")
        client.close()
        exit()



# Listening To Server and Sending Username
def receive():
    while True:
        try:
            # Receive Message From Server
            # If 'USER' Send Username
            message = client.recv(1024).decode('ascii')
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
        client.send(message.encode("ascii"))

# Starting Threads For Listening And Writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()

