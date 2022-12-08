#!/usr/bin/python3.8


defaults = {
    "memcache.address"                  : "127.0.0.1:11211",
    "heatingUnit.0.address"             : "/dev/tty.usbserial-ANZ20BUO",
    "heatingUnit.0.enable"              : 0, 
    "heatingUnit.0.pythonImportName"    : "heating_unit_mc"
    "listOfDevices"                     : ["heatingUnit.0"]
    }



d = defaults

import pymemcache
import time


#####################################3
# set-up mc
##################################
mc = pymemcache.Client(d["memcache.address"])

for key,value in d.items(): 
    mc.set(key, value)


for key,value in d.items():
    print(key, value, mc.get(key))

############################################
# set-up units
############################################

for unit_name in mc.get(listOfDevices):

    # do imports
    if unit_name + ".pythonImportName" in mc.get
    















