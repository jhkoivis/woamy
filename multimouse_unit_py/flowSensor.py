


import array
import sys
import usb.core
import usb.util

VID = 0x03f0 #0x046d
PID = 0x094a #0xc05a
DATA_SIZE = 4

# printina modulio vidurius :for i in dir(usb.util): print i

# try to find Logiceh USB mouse
device = usb.core.find(idVendor = VID, idProduct = PID)
if device is None:
    sys.exit("Could not find Logitech USB mouse.")

# make sure the hiddev kernel driver is not active
if device.is_kernel_driver_active(0):
    try:
        device.detach_kernel_driver(0)
    except usb.core.USBError as e:
        sys.exit("Could not detatch kernel driver: %s" % str(e))

# set configuration
try:
    device.reset()
    device.set_configuration()
except usb.core.USBError as e:
    sys.exit("Could not set configuration: %s" % str(e))

endpoint = device[0][(0,0)][0]
print(endpoint.wMaxPacketSize)


data = array.array('B',(0,)*4)
while data[0] != 3:
    try:
        data = device.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize)
        print(data)
    
    except usb.core.USBError as e:
        if e.args == ('Operation timed out',):
            print("timeoutas")
            continue
print("baigiau! :)")




