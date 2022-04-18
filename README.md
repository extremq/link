# link
**link** is a tool I use for connecting devices on my LAN network to my primary unit.

# Usage
## Starting the server
You can start the server up using `python server.py PORT`. If the port is not specified, `1337` will be chosen.

## Connecting as a client
Using `python client.py IP PORT`, you can connect to your server. Default port is `1337`.

BEWARE: you should assign a static IP address for your server from your router/OS settings. This way, you won't have to change the IP countlessly.

# Extending
This is a basic example, but you can improve it however you'd like by adding commands. Right now, `url link` is supported, which opens up a browser tab with the requested link.
