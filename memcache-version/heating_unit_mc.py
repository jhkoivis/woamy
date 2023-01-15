import serial
import time
import random
import pymemcache


class heating_unit_mc:
    """
    A class for Woamy machine heating unit control to be used with memcached and node-red

    ...

    Attributes
    ----------
    temperature: float
        Temperature measured inside the heater unit
    target_temperature: float
        Desired temperature set by user (default 0.0)
    ser: Serial() object
        Serial object for the usb serial port cotrol
    switch: Boolean
        

    Methods
    -------
    get_temperature()
        Measures the temperature inside unit. Returns and updates the value
    heater_switch(value)
        Switches the heating lamp on or off
    """

    def __init__(self, unit_name=None, memcached_address=None):

        self.unit_name  = unit_name
        self.mc         = pymemcache.Client(memcached_address)         
        self.update_local()

        if not self.simulate: self.ser = serial.Serial(self.port_name, 250000)
        time.sleep(5)
        self.temperature = 0.0
        self.switch = False
        self.errorCount = 0

    def update_local(self):
        """
            Reads essential inputs from memcached to local variables.
        """
        try:
            self.simulate           = int  (self.mc.get(self.unit_name + ".simulate").decode('ascii'))
            self.port_name          =       self.mc.get(self.unit_name + ".port_name")
            self.enabled            = int  (self.mc.get(self.unit_name + ".enabled"))
            self.target_temp_degc   = float(self.mc.get(self.unit_name + ".target_temp_degc").decode('ascii')) 
            self.errorCount = 0
        except Exception as e:
            print(str(e))
            print(self.unit_name)
            print(self.unit_name + ".target_temp_degc")
            print(self.mc.get(self.unit_name + ".target_temp_degc"))
            self.errorCount = self.errorCount + 1


    def update_mc(self):
        """
            Writes essential outputs to memcached from local variables.
        """
        self.mc.set(self.unit_name + ".current_temp_degc",  self.get_temperature())
        self.mc.set(self.unit_name + ".switch_ro",          self.switch)
        self.mc.set(self.unit_name + ".errorCount",         self.errorCount)


    def update(self):
        """
            This function is the outline for main functionality

            TODO: consider creating update_mc function instead of writing stuff here
        """
        self.update_local()
        
        if self.enabled:
            current_temp = self.get_temperature()
            if current_temp < self.target_temp_degc: self.heater_switch(True)
            else: self.heater_switch(False)

        self.update_mc()


    def print(self):
        print()
        print("Unit name:                   ", self.unit_name)
        print("Current temperature (local): ", self.get_temperature())
        print("Current temperature (mc):    ", float(self.mc.get(self.unit_name + ".current_temp_degc").decode('ascii')))
        print("Target temperature (local):  ", self.target_temp_degc)
        print("Target temperature (mc):     ", self.mc.get(self.unit_name + ".target_temp_degc"))
        print("Switch on/off: (local):      ", self.switch)
        print("Errorcount (local):          ", self.errorCount)
        print()

    ###########################################
    # internal functions
    ###########################################

    def get_temperature(self):

        if self.simulate: 
            self.temperature = self.temperature + random.random() - 0.5 + 0.1*(self.target_temp_degc - self.temperature)
            return self.temperature

        ## Read message to empty the buffer
        self.read_message()
        time.sleep(0.1)

        ## Ask for the temperature
        self.ser.write(b'M105\r\n')
        time.sleep(0.1)

        ## Read messsage containing temperature from buffer
        message = self.read_message()
        message_list = message.split(' ')
        for element in message_list:
            if len(element) < 2:
                continue
            elif element[:2] == 'T:':
                self.temperature = float(element[2:])
                break

        return self.temperature


    def heater_switch(self, switch_value):
        """Switch the heater on/off

        Parameters
        ----------
        switch_value: Boolean
            Turn heater on (True) or off (False)
        """

        if switch_value == self.switch:
            return

        if switch_value:
            if not self.simulate:
                self.ser.write(b'M104 S200\r\n')
            self.switch = True
        else:
            if not self.simulate:
                self.ser.write(b'M104 S0\r\n')
            self.switch = False

        self.read_message()


    def read_message(self):
        """Print message from self.ser - usb device

        Returns
        -------
        message: str
            Message read from the buffer of the device
        """

        if self.simulate:
            return "simulation"

        message_bits = self.ser.inWaiting()
        if message_bits:
            message = self.ser.read(message_bits)
            return message.decode('utf-8')


    def close_connection(self):

        ## Before closeing the connection switch heater off for safety
        self.heater_switch(False)
        if not self.simulate: self.ser.close()






