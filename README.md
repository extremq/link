# link
**link** is a tool I use for connecting devices on my LAN network to my primary unit.

# Usage
## Starting the server
You can start the server up using `python server.py PORT`. If the port is not specified, `1337` will be chosen.
A random password will be generated for the client to connect with.

## Connecting as a client
Using `python client.py IP PORT`, you can connect to your server. Default port is `1337`. Then, just type the password and you're done.

BEWARE: you should assign a static IP address for your server from your router/OS settings. This way, you won't have to change the IP countlessly.

# Commands
- prs - shows running processes on server with their respective PID. Limited to 4KB of data.
- kill <PID> - kills a process with PID = <PID>
- url <URL> - opens a browser tab (can omit https://)
- quit - quits the server
- dis - disconnects from the server