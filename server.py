from arguments import *
from socket_helpers import *

import random, string, os

def generate_password():
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(10))

def main():
    os.system("git pull")
    print("Welcome.\nSyntax: python server.py PORT")
    PORT = get_port()
    main_socket = setup_server(PORT)
    password = generate_password()
    process_requests(main_socket, password)

if __name__=="__main__":
    main()
