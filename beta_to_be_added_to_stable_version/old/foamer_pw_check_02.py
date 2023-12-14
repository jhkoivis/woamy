import asyncio

from opcua import Client as OpcUaClient
from opcua import ua

from pymemcache.client.base import Client as McClient

import time
import csv

class Foamer:

    # init ---------------------------------------------------------------------#
    def __init__(   self, 
                    unit_name       = None,
                    memcached_host  = None, 
                    memcached_port  = None):

        self.unit_name      = unit_name
        self.memcached_host = memcached_host
        self.memcached_port = memcached_port

        if self.unit_name        == None: self.unit_name        = "opc.tcp://10.0.0.63:4840"
        if self.memcached_host   == None: self.memcached_host   = 'localhost'
        if self.memcached_port   == None: self.memcached_port   = 11211

        self.opcua_client               = None
        self.mc_client                  = None 

        self.MES_TO_PLC_air_flow        = 49
        self.MES_TO_PLC_head_speed      = None
        self.MES_TO_PLC_pressure_head   = None
        self.MES_TO_PLC_product_flow    = None
        self.MES_TO_PLC_pump_speed      = None

        self.debug      = 1
        self.dry_run    = 1

    # _init for asyncio -----------------------------------------------------------------------#
    async def _init(self):
        try:
            if not self.dry_run:
                self.opcua_client   = OpcUaClient(self.unit_name)
                self.opcua_client.connect()
            self.mc_client      = McClient("%s:%d" % (self.memcached_host, self.memcached_port))
        except Exception as e:
            print("Error while connecting:", e)
            raise


    # disconnect for asyncio -----------------------------------------------------------#
    async def disconnect(self): 
        if self.opcua_client: 
            if not self.dry_run:
                self.opcua_client.disconnect()
        if self.mc_client:
            self.mc_client.close()


    # update function -------------------------------------------------------------------#
    async def update(self):
        try:
            await self._init()

            mc_var = int(self.mc_client.get("foamer.0.MES_TO_PLC_air_flow"))
            if not mc_var == int(self.MES_TO_PLC_air_flow):
                if self.debug: 
                    print("change detected")
                self.MES_TO_PLC_air_flow = mc_var
                if not self.dry_run:
                    opc_value   = ua.DataValue(ua.Variant(mc_var), ua.VariantType.Int32)
                    opc_node    = self.opcua_client.get_node("ns=4;s=MES_TO_PLC_air_flow")
                    opc_node.set_value(opc_value)
            
            if self.debug:
                print("MES_TO_PLC_air_flow: %d" % (self.MES_TO_PLC_air_flow))

            await asyncio.sleep(0.5)

        except Exception as e:
            raise
        finally:
            await self.disconnect()
    #------------------------------------------------------------------------------------#

# block to running foamer
#async def main():
#    foamer = Foamer()
#    await foamer.update()
#
#if __name__ == "__main__":
#    asyncio.run(main())

if __name__ == "__main__":

    foamer = Foamer()
    while True:
        asyncio.run(foamer.update())
    
#client = Client("opc.tcp://10.0.0.63:4840")

#"""
#MES_TO_PLC_air_flow(one)
#MES_TO_PLC_head_speed(two)
#MES_TO_PLC_pressure_head(three)
#MES_TO_PLC_product_flow(four)
#MES_TO_PLC_pump_speed(fife)
#
#PLC_TO_MES_flow_air(one)
#PLC_TO_MES_head_speed(two)
#PLC_To_MES_backpressure_head(three)
#PLC_TO_MES_flow_product(four)
#PLC_TO_MES_pressure_head(six)
#PLC_TO_MES_temperature_head
#"""
#
#try:
#    client.connect()
#    
#    for i in range(10):
#    
#    	head_rpm_value = int(input("Give head head pressure: "))
#
#    	head_rpm_node = client.get_node("ns=4;s=MES_TO_PLC_pressure_head")
#    	speed = ua.DataValue(ua.Variant(head_rpm_value, ua.VariantType.Int32))
#    	head_rpm_node.set_value(speed) 	
#    
#    	#block for reading head rpm value
#    	var_speed_head = client.get_node("ns=4;s=PLC_TO_MES_head_speed")
#    	pressure_head_result = var_speed_head.get_value()
#    	print("Speed Head Rpm is:",pressure_head_result)
#    	time.sleep(0.5)
#            
#finally:
#    
#    client.disconnect()
#    print("Finished")

