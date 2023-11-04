import socket
import json

# Define the multicast address and port used by the Govee lights
multicast_ip = "239.255.255.250"
multicast_port = 4001  # Modify this port according to your Govee lights setup

# Create a UDP socket for sending the "cmd: scan" message
send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Define the "cmd: scan" command for discovery
command = {
    "msg": {
        "cmd": "scan",
        "data": {
            "account_topic": "reserve"
        }
    }
}

# Convert the command to a JSON string
command_json = json.dumps(command)

# Send the "cmd: scan" message to the multicast address and port
send_socket.sendto(command_json.encode('utf-8'), (multicast_ip, multicast_port))

# Close the sending socket when done
send_socket.close()
