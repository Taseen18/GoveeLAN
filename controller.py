import socket
import json
import time

# Define the device's IP address and port
device_ip = "192.168.0.40"
device_port = 4003  # Replace with the appropriate port for control
running = True

def powerOn():
    command = {
        "msg": {
            "cmd": "turn",
            "data": {
                "value": 1  # 0 means "off," 1 means "on"
            }
        }
    }
    sendCommand(command)
    time.sleep(1)
    sync()

def powerOff():
    command = {
        "msg": {
            "cmd": "turn",
            "data": {
                "value": 0  # 0 means "off," 1 means "on"
            }
        }
    }
    sendCommand(command)
    time.sleep(1)
    sync()

def adjustBrightness():
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
    sendCommand(command)
    time.sleep(1)
    sync()

def changeColour():
    pass

def sync():
    command = {
        "msg": {
            "cmd": "devStatus",
            "data": {}
        }
    }
    sendCommand(command)

def sendCommand(command):
    # Convert the command to a JSON string
    command_json = json.dumps(command)

    # Create a socket to send the control command
    controller_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Send the control command to the device's IP address and port
    controller_socket.sendto(command_json.encode('utf-8'), (device_ip, device_port))
 

    # Close the control socket when done
    controller_socket.close()




while running:
    print("\n~~CONTROLS~~\n1. Power On\n2. Power Off\n3. Adjust Brightness\n4. Sync\n5. (quit)")
    selection = str(input("--> "))
    if selection == '1':
        powerOn()
    elif selection == '2':
        powerOff()
    elif selection == '3':
        adjustBrightness()
    elif selection == '4':
        sync()
    elif selection == '5' or selection.lower() == 'quit':
        running = False
    else:
        pass


