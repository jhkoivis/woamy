#!/usr/bin/python3.8


defaults = {
    "memcache.address"                  : "127.0.0.1:11211",
    "heatingUnit.0.port_name"           : "/dev/tty.usbserial-ANZ20BUO",
    "heatingUnit.0.enabled"             : 1,
    "heatingUnit.0.simulate"            : 1,
    "heatingUnit.0.target_temp_degc"    : 0,
    "heatingUnit.0.current_temp_degc"   : 0,
    "heatingUnit.0.switch_ro"           : 0,
    "heatingUnit.0.pythonImportName"    : "heating_unit_mc",

    "heatingUnit.1.port_name"           : "/dev/tty.usbserial-ANZ20BUO",
    "heatingUnit.1.enabled"             : 1,
    "heatingUnit.1.simulate"            : 1,
    "heatingUnit.1.target_temp_degc"    : 0,
    "heatingUnit.1.current_temp_degc"   : 0,
    "heatingUnit.1.switch_ro"           : 0,
    "heatingUnit.1.pythonImportName"    : "heating_unit_mc",

    "listOfDevices"                     : ["heatingUnit.0", "heatingUnit.1"]
    }



d = defaults

import pymemcache
import time
import importlib

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

list_of_units = []

# heating unit 0 
import heating_unit_mc
hu_mc_0 = heating_unit_mc.heating_unit_mc(  unit_name           = "heatingUnit.0", 
                                            memcached_address   = defaults["memcache.address"])
list_of_units.append(hu_mc_0)

# heating unit 1
import heating_unit_mc
hu_mc_1 = heating_unit_mc.heating_unit_mc(  unit_name           = "heatingUnit.1",
                                            memcached_address   = defaults["memcache.address"])
list_of_units.append(hu_mc_1)

# 2023_5m_conveyer
import conveyer_2023_5m
co_0 = conveyer_2023_5m.conveyer_2023_5m(   unit_name           = "conveyer_2023_5m.0",
                                            memcached_address   = defaults["memcache.address"])
list_of_units.append(co_0)

###########################################
# run loop
###########################################

while True:

    for unit in list_of_units:
        unit.update()
        unit.print()
    
    time.sleep(5)
    #print(list_of_units[0].get_temperature())

    










