# GoveeLAN
This program uses Govee's new LAN API to control supported devices using python.

Usage:
- controller.py is the main program and should be used by itself. It contains a discovery tool.
- Receiver.py & Discovery.py are to be used together only if you wish to discover devices.
    1. run Receiver.py
    2. run Discovery.py
    3. If any responses detected Receiver.py should print the details.