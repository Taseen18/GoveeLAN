import socket
import json

# Define the multicast address and port for listening
multicast_ip = "239.255.255.250"
multicast_port = 4002

# Create a UDP socket for listening to multicast messages
listen_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_socket.bind(('', multicast_port))
listen_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, socket.inet_aton(multicast_ip) + socket.inet_aton("0.0.0.0"))
listening = True


while listening:
    try:
        print(f"\n\nListening for JSON messages on {multicast_ip}:{multicast_port}...")
        if listen_socket.recv:
            print("Message Received: ", listen_socket.recv(10240))
    except KeyboardInterrupt:
        break



# Close the listening socket when done
listen_socket.close()
