


import array
import sys
import usb.core
import usb.util

class FlowSensor:

    def __init__(unit_name="flowSensor.1"):
        pass

    def _init():
        self.VID = 0x03f0 #0x046d
        self.PID = 0x094a #0xc05a
        self.DATA_SIZE = 4

        # printina modulio vidurius :for i in dir(usb.util): print i

        # try to find Logiceh USB mouse
        self.device = usb.core.find(idVendor = VID, idProduct = PID)
        if self.device is None:
            sys.exit("Could not find Logitech USB mouse.")

        # make sure the hiddev kernel driver is not active
        if self.device.is_kernel_driver_active(0):
        try:
            self.device.detach_kernel_driver(0)
        except usb.core.USBError as e:
            sys.exit("Could not detatch kernel driver: %s" % str(e))

        # set configuration
        try:
            self.device.reset()
            self.device.set_configuration()
        except usb.core.USBError as e:
            sys.exit("Could not set configuration: %s" % str(e))

        self.endpoint = device[0][(0,0)][0]
        print(self.endpoint.wMaxPacketSize)


    def update():

        startTime = time.time()
        distance_travelled = 0

        data = array.array('B',(0,)*4)
        while data[0] != 3:
            try:
                data = device.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize)
                distance_travelled += data[2]
    
            except usb.core.USBError as e:
                if e.args == ('Operation timed out',):
                    print("timeoutas")
                    continue
            if time.time() - startTime >= 2.0:
                print(distance_travelled)
                break




