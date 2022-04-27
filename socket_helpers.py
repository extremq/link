import socket
import webbrowser
import os

DISCONNECT = "3"
MESSAGE_INCOMING = "2"
HEALTH = "1"

def setup_client(IP, PORT):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client_socket.connect((IP, PORT))
    print(f"You connected succesfully to {IP}:{PORT}.")

    return client_socket

def process_client(client_socket):
    message = client_socket.recv(256).decode()
    if message == MESSAGE_INCOMING:
        message = client_socket.recv(4096).decode()
        print(message)
    
    while True:
        command = input(">>> ").strip()
        client_socket.send(command.encode())

        if command == "quit" or command == "disconnect":
            break
        
        message = client_socket.recv(256)
        if not message:
            print("Server shut down.")
            exit()
        else:
            if message.decode() == MESSAGE_INCOMING:
                message = client_socket.recv(4096).decode()
                print(message)
            elif message.decode() == HEALTH:
                pass 
            elif message.decode() == DISCONNECT:
                print("Wrong password.")
                exit()

def setup_server(PORT):
    # Init a socket
    main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Succesfully created socket.")

    # Bind the port
    main_socket.bind(('', PORT))
    print(f"Bound socket to port {PORT}")

    # Start listening
    main_socket.listen()
    print("Socket is listening.")

    return main_socket

def disconnect_client(client_socket, addr):
    print(f"Client disconnected ({addr[0]}:{addr[1]}).")
    print("-----END CONNECTION-----")
    client_socket.close()


def process_requests(main_socket, password):
    print(f"The password is '{password}'")

    running = True

    while running:
        client, addr = main_socket.accept()

        password_accepted = False

        print("-----BEGIN CONNECTION-----")
        print(f"Connected with {addr[0]}:{addr[1]}!")

        client.send(MESSAGE_INCOMING.encode())
        client.send("Type the server password.".encode())
        while True:
            try:
                data = client.recv(4096)
            except:
                print("Connection error.")
                disconnect_client(client, addr)

            # data not present means client disconnected
            if not data:
                disconnect_client(client, addr)
                break

            message = data.decode().strip()
            
            if password_accepted == False:
                if message == password:
                    password_accepted = True
                    client.send(MESSAGE_INCOMING.encode())
                    client.send("Correct password! You can send commands.".encode())
                else:
                    client.send(DISCONNECT.encode())
                    disconnect_client(client, addr)
                    break
            
            # Split the message into arguments
            args = message.split()
            args[0] = args[0].lower()
            print(f"Got: {args}")

            # Function returns 0 when client disconnects
            if process_command(args, client, addr) == 0:
                break
            else:
                client.send(HEALTH.encode())

def process_command(args, client, addr):
    if args[0] == "disconnect":
        disconnect_client(client, addr)
        return 0
    elif args[0] == "quit":
        disconnect_client(client, addr)
        exit()
    # URL <URL> - opens a web browser tab 
    elif args[0] == "url" and len(args) > 1:
        if not args[1].startswith("https://"):
            args[1] = "https://" + args[1]

        webbrowser.open(args[1], new=2)
    # CMD <CMD> - send a command
    elif args[0] == "cmd" and len(args) > 1:
        os.system(args[1])
