from sys import argv

def get_port(PORT=1337):
    # The first argument is the port
    if len(argv) > 1:
        PORT = int(argv[1]) 

    return PORT

def get_ip_port(IP="192.168.100.100", PORT=1337):
    if len(argv) > 2:
        IP = argv[1]
        PORT = int(argv[2])

    return (IP, PORT)
