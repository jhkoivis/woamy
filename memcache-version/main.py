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

imports = []
list_of_units = []

for unit_name in eval(mc.get('listOfDevices')):
    pass
    # do imports
    
    import_name     = mc.get(unit_name + ".pythonImportName").decode('ascii')
    imported        = importlib.import_module(import_name)
    

    mc_address = mc.get('memcache.address').decode('ascii')
    # create instaces to unit list (with simulation on/off)
    cmd = "imported." + import_name + "(unit_name='" + unit_name + "', memcached_address='" + mc_address + "')"
    print(cmd)
    #exec(import_name)
    list_of_units.append(eval(cmd))



###########################################
# run loop
###########################################

while True:

    for unit in list_of_units:
        unit.update()
        unit.print()
    
    time.sleep(5)
    #print(list_of_units[0].get_temperature())

    










