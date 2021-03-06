from arguments import *
from socket_helpers import *

def main():
    print("Welcome.\nSyntax: python client.py IP PORT")

    IP, PORT = get_ip_port()
    client_socket = setup_client(IP, PORT)
    process_client(client_socket)

if __name__=="__main__":
    main()