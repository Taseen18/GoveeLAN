import socket
import json
import time
import threading
import sys


multicast_ip = "239.255.255.250"
multicast_send = 4001
multicast_receive = 4002

device_port = 4003 
running = True
responses = [] # Holds dictionaries containing all details of each response
completion_event = threading.Event() # signals the completion of the discovery function

def discoverDevices():
    threading.Thread(target=scanResponses).start()
    threading.Thread(target=sendDiscoveryPacket).start()
    message = "Discovering Devices"
    threading.Thread(target=loadingMessage, args=(message,)).start()

    time.sleep(8)
    return responses

def scanResponses():
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_socket.bind(('', multicast_receive))
    listen_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, socket.inet_aton(multicast_ip) + socket.inet_aton("0.0.0.0"))
    listen_socket.settimeout(5) # Sets the discovery time

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
                    #print(f"Received response from {addr[0]}: {device_info}")      # uncomment to print as soon as a response is received
        except json.JSONDecodeError:
            print("Received non-JSON message:", received_message)

    # Start listening for responses
    try:
        while True:
            data, addr = listen_socket.recvfrom(10240)
            threading.Thread(target=process_response, args=(data, addr)).start() # Starts a thread once a response is received to process it concurrently
    except socket.timeout:
        pass
        completion_event.set()
        return responses

    listen_socket.close()

    
def sendDiscoveryPacket():
    discovery_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    command = {
        "msg": {
            "cmd": "scan",
            "data": {
                "account_topic": "reserve"
            }
        }
    }

    command_json = json.dumps(command)
    discovery_socket.sendto(command_json.encode('utf-8'), (multicast_ip, multicast_send))
    discovery_socket.close()

def loadingMessage(message):
    while not completion_event.is_set():
        for char in "-\|/":
            print(f" {message} {char}", end="\r")
            time.sleep(0.2)
            print(" " * 25, end="\r")

    print(" Loading Complete", end="\r")
    time.sleep(2)  # Display the completion message for 2 seconds
    print(" " * 25, end="\r")  # Clear the line again
        
def powerOn(device_ip):
    command = {
        "msg": {
            "cmd": "turn",
            "data": {
                "value": 1  # 0 means "off," 1 means "on"
            }
        }
    }
    sendCommand(command, device_ip)
    time.sleep(1)
    #sync()

def powerOff(device_ip):
    command = {
        "msg": {
            "cmd": "turn",
            "data": {
                "value": 0  # 0 means "off," 1 means "on"
            }
        }
    }
    sendCommand(command, device_ip)
    time.sleep(1)
    #sync()

def adjustBrightness(device_ip):
    brightness = -1
    while brightness < 1 or brightness > 100:
        brightness = int(input("\nEnter Brightness (1-100): "))
    
    command = {
        "msg": {
            "cmd": "brightness",
            "data": {
                "value": brightness
            }
        }
    }
    sendCommand(command, device_ip)
    time.sleep(1)
    #sync()

def changeColour():
    pass

def sync(device_ip):
    command = {
        "msg": {
            "cmd": "devStatus",
            "data": {}
        }
    }
    sendCommand(command, device_ip)

def sendCommand(command, device_ip):
    # Convert the command to a JSON string
    command_json = json.dumps(command)

    # Create a socket to send the control command
    controller_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Send the control command to the device's IP address and port
    controller_socket.sendto(command_json.encode('utf-8'), (device_ip, device_port))
 

    # Close the control socket when done
    controller_socket.close()


def getDeviceIP(index):
    device = responses[index]
    if device:
        ip = device.get('ip', 'N/A')
        return ip
    return None

def getDeviceMac(index):
    device = responses[index]
    if device:
        mac = device.get('device', 'N/A')
        return mac
    return None
    

def displayDevices():
    if len(responses) <= 0:
        print("\nNo Devices Found")
    else:
        counter = 1
        for device in responses:
            print("\nDevice", counter)
            print("IP", getDeviceIP(counter-1))
            print("MAC", getDeviceMac(counter-1))
            counter += 1


def controlMenu(device_ip):
    while True:
        print("\n~~CONTROLS~~\n1. Power On\n2. Power Off\n3. Adjust Brightness\n4. Sync\n5. Change Device")
        selection = str(input("--> "))
        if selection == '1':
            powerOn(device_ip)
        elif selection == '2':
            powerOff(device_ip)
        elif selection == '3':
            adjustBrightness(device_ip)
        elif selection == '4':
            sync(device_ip)
        elif selection == '5':
            break
        else:
            pass

def deviceMenu():
    if len(responses) > 0:
        displayDevices()
        while True:
            print("\n~~SELECT DEVICE~~")
            for counter in range(len(responses)):
                print(str(counter+1) + ". Device " + str(counter+1))
            print(str(len(responses)+1) + ". Enter Custom IP")
            print(str(len(responses)+2) + ". (quit)")
            selectedDevice = input("--> ")
            try:
                selectedDevice = int(selectedDevice)
                if int(selectedDevice) > 0 and int(selectedDevice) <= len(responses):
                    device_ip = getDeviceIP(int(selectedDevice)-1)
                    controlMenu(device_ip)
                elif int(selectedDevice) == len(responses)+1:
                    device_ip = str(input("\n Enter Custom IP: "))
                    controlMenu(device_ip)
                elif selectedDevice == len(responses)+2:
                    break
            except:
                if str(selectedDevice.lower()) == 'quit':
                    break

            if int(selectedDevice) > 0 and int(selectedDevice) <= len(responses):
                device_ip = getDeviceIP(int(selectedDevice)-1)
                controlMenu(device_ip)
            elif int(selectedDevice) == len(responses)+1:
                device_ip = str(input("\n Enter Custom IP: "))
                controlMenu(device_ip)
            elif int(selectedDevice) == len(responses)+2 or str(selectedDevice.lower()) == 'quit':
                break
    

print("\nDevices: ", discoverDevices())
#print(discoverDevices())
deviceMenu()


