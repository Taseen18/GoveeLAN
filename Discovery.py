import socket
import json

# Define the multicast address and port used by the Govee lights
multicast_ip = "239.255.255.250"
multicast_port = 4001  # Modify this port according to your Govee lights setup

# Create a UDP socket for sending the "cmd: scan" message
send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Define the "cmd: scan" command for discovery
cmd_scan = {
    "msg": {
        "cmd": "scan",
        "data": {
            "account_topic": "reserve"
        }
    }
}

# Convert the command to a JSON string
cmd_scan_json = json.dumps(cmd_scan)

# Send the "cmd: scan" message to the multicast address and port
send_socket.sendto(cmd_scan_json.encode('utf-8'), (multicast_ip, multicast_port))

# Close the sending socket when done
send_socket.close()
