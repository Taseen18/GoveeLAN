

import socket
import json
import threading
import time

# Define the multicast address and port for listening
multicast_ip = "239.255.255.250"
multicast_port = 4002

# Create a UDP socket for listening to multicast messages
listen_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_socket.bind(('', multicast_port))
listen_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, socket.inet_aton(multicast_ip) + socket.inet_aton("0.0.0.0"))
listening = True

listen_socket.settimeout(5)

# Create a list to store responses from different devices
responses = []
lock = threading.Lock()

def process_response(data, addr):
    received_message = data.decode('utf-8')
    try:
        received_json = json.loads(received_message)
        device_info = {
            'ip': addr[0],  # Extract the IP address from the source address tuple
            'device': received_json.get("msg", {}).get("data", {}).get("device")
        }
        if device_info['device']:
            with lock:
                responses.append(device_info)
                print(f"Received response from {addr[0]}: {device_info}")
    except json.JSONDecodeError:
        print("Received non-JSON message:", received_message)

# Start listening for responses
try:
    while True:
        data, addr = listen_socket.recvfrom(10240)
        threading.Thread(target=process_response, args=(data, addr)).start()
except socket.timeout:
    pass

# Process the responses from different devices
with lock:
    for device_info in responses:
        print(f"Device at {device_info['ip']} with device ID {device_info['device']} responded.")

print(responses)



# Close the listening socket when done
listen_socket.close()
