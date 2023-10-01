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
    running: int
        1 = belt moving (any int that converts to True)
        0 = belt stopped (any int (0) that converts to False)
    errorCount: int
        Number of errors detected

    Methods (public)
    -------
    update: 
        reads memcached, compares changes and sends commands only if needed 
    print:
        prints status of belt in human readable format

    Methods (private and debug)
    -------
    _start:
        Starts the belt movement
    _stop:
        Stops the belt movement
    _update_local:
        Updates local (this object from memcached)
    _update_mc:
        Updates memcached (memcached from this object)
    """

    def __init__(self, unit_name=None, memcached_address=None):

        self.unit_name  = unit_name
        self.mc         = pymemcache.Client(memcached_address)         
        self._update_local()

    def _update_local(self):
        """
            Reads essential inputs from memcached to local variables.
        """
        try:
            self.running            = int  (self.mc.get(self.unit_name + ".running").decode('ascii'))
            self.errorCount         = 0
        except Exception as e:
            print(str(e))
            print(self.unit_name)
            print(self.unit_name + ".running")
            print(self.mc.get(self.unit_name + ".running"))
            self.errorCount         = self.errorCount + 1


    def _update_mc(self):
        """
            Writes essential outputs to memcached from local variables.
        """
        self.mc.set(self.unit_name + ".running",            self.running())
        self.mc.set(self.unit_name + ".errorCount",         self.errorCount)


    def update(self):
        """
            This function is the outline for main functionality
        """
        # store current status
        prev_running = self.running

        # get new status
        self.update_local()
        
        # if change, do something
        if not prev_running == self.running:
            if self.running: self._start()
            else: self._stop()

    def print(self):
        pass

    def _start(self):
        pass

    def _stop(self):
        pass

