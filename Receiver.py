# This discovery tool runs for 5 seconds.

import socket
import json
import threading
import time


multicast_ip = "239.255.255.250"
multicast_port = 4002

# Create a UDP socket for listening to multicast messages
listen_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_socket.bind(('', multicast_port))
listen_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, socket.inet_aton(multicast_ip) + socket.inet_aton("0.0.0.0"))
listen_socket.settimeout(5) # Sets the discovery time

responses = [] # Holds dictionaries containing all details of each response
lock = threading.Lock()

#Processes each response and adds it to the list
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
        threading.Thread(target=process_response, args=(data, addr)).start() # Starts a thread once a response is received to process it concurrently
except socket.timeout:
    pass

# Prints all the stored devices from the list
with lock:
    for device_info in responses:
        print(f"Device at {device_info['ip']} with device ID {device_info['device']} responded.")

print(responses) # Prints the list



# Ensures proper closure of the socket
listen_socket.close()
