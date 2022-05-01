import socket
import webbrowser
import subprocess
import psutil

DISCONNECT = "3"
MESSAGE_INCOMING = "2"
HEALTH = "1"

def setup_client(IP, PORT):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client_socket.connect((IP, PORT))
    print(f"You connected succesfully to {IP}:{PORT}.")

    return client_socket

def process_client(client_socket):
    message = client_socket.recv(1).decode()
    if message == MESSAGE_INCOMING:
        message = client_socket.recv(65536).decode()
        print(message)
   
    while True:
        command = input(">>> ").strip()
        client_socket.send(command.encode())

        if command == "quit" or command == "dc":
            break
        
        message = client_socket.recv(1)
        if not message:
            print("Server shut down.")
            exit()
        else:
            if message.decode() == MESSAGE_INCOMING:
                message = client_socket.recv(65536).decode()
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

        send_string(client, "Type the server password.")
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
                    send_string(client, "Correct password! You can send commands.")
                else:
                    client.send(DISCONNECT.encode())
                    disconnect_client(client, addr)
                    break
            else: 
                # Split the message into arguments
                args = message.split()
                args[0] = args[0].lower()
                print(f"Got: {args}")

                # Function returns 0 when client disconnects
                if process_command(args, client, addr) == 0:
                    break

def send_string(client, msg):
    client.send(MESSAGE_INCOMING.encode())
    client.send(msg.encode())
    

def process_command(args, client, addr):
    send_health = True

    if args[0] == "dc":
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
        subprocess.Popen(args[1:])
    elif args[0] == "prs":
        process_list = list()
        for p in psutil.process_iter():
            process_list.append("%s -> %d\n" % (p.name(), p.pid))

        process_list = 'Name -> PID'.join(sorted(process_list))
    
        send_health = False
        send_string(client, process_list)
    elif args[0] == "kill" and len(args) > 1:
        send_health = False
        try:
            psutil.Process(int(args[1])).kill()
        except:
            send_string(client, "No such process found.")
        else:
            send_string(client, "Process killed.")

    if send_health:
        client.send(HEALTH.encode())
