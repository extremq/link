from arguments import *
from socket_helpers import *

def main():
    print("Welcome.\nSyntax: python server.py PORT")
    PORT = get_port()
    main_socket = setup_server(PORT)
    process_requests(main_socket)

if __name__=="__main__":
    main()