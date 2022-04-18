import socket
import webbrowser

def setup_client(IP, PORT):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    client_socket.connect((IP, PORT))
    print(f"You connected succesfully to {IP}:{PORT}.")

    return client_socket

def process_client(client_socket):
    while True:
        command = input(">>> ").strip()
        client_socket.send(command.encode())

        if command == "quit" or command == "disconnect":
            break
    

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


def process_requests(main_socket):
    running = True

    while running:
        client, addr = main_socket.accept()

        print("-----BEGIN CONNECTION-----")
        print(f"Connected with {addr[0]}:{addr[1]}!")
        client.send("Connected succesfully.\n".encode())

        while True:
            data = client.recv(4096)

            if not data:
                disconnect_client(client, addr)
                break
            
            message = data.decode().strip()
            print(f"Got: {message}")

            command = message.split()
            
            if command[0] == "disconnect":
                disconnect_client(client, addr)
                break;
            elif command[0] == "quit":
                disconnect_client(client, addr)
                main_socket.close()
                exit()
            elif command[0] == "url" and len(command) > 1:
                if not command[1].startswith("https://"):
                    command[1] += "https://"
                
                webbrowser.open(command[1], new=2)


