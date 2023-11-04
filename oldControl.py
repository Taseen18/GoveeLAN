import socket
import json

# Define the device's IP address and port (adjust with the actual values)
device_ip = "192.168.0.40"
device_port = 4003  # Replace with the appropriate port for control

# Construct the control command
control_command = {
    "msg": {
        "cmd": "turn",
        "data": {
            "value": 1  # 0 means "off," 1 means "on"
        }
    }
}

# Convert the command to a JSON string
control_command_json = json.dumps(control_command)

# Create a socket to send the control command
control_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Send the control command to the device's IP address and port
control_socket.sendto(control_command_json.encode('utf-8'), (device_ip, device_port))

# Close the control socket when done
control_socket.close()
