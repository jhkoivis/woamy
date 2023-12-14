import asyncio
import evdev

from async_conveyor_belt import ConveyorBelt
from async_foamer import FoamerUnit
from pymemcache.client.base import Client




defaults = {
    "memcache.address"                   : "127.0.0.1:11211",
    "conveyorBelt.0.address"             : "opc.tcp://10.0.0.53:4840",
    "conveyorBelt.0.enable"              : 0,
    "conveyorBelt.0.target"              : 0,
    "conveyorBelt.0.pythonImportName"    : "async_conveyor_belt",
    "conveyorBelt.0.status"              : 5,
   
    #defaults for async_foamer
    
    "foamer.0.address"             : "opc.tcp://10.0.0.63:4840",
    "foamer.0.enable"              : 0,
    "foamer.0.pythonImportName"    : "async_foamer",
    "foamer.0.target"              :0,
    "foamer.0.status"              : 5,
    "foamer.0.Airtarget"           :10,
    "foamer.0.HeadRPMtarget"       :200,
    "foamer.0.PressureHeadtarget"  :0,
    "foamer.0.ProductFlowtarget"   :20,
    "foamer.0.PumpSpeedtarget"     :5,
    "listOfDevices": ["conveyorBelt_0", "foamer_0"], 
   
    "flowSensor.0.address"          : "/dev/input/event3",
    "flowSensor.0.rawFlow"          : 0,
 
    }



async def module(device):
    coros           = [device._init(), asyncio.sleep(0.5)]
    await asyncio.gather(*coros)
    while true:
        coros       = [device.update(), asyncio.sleep(0.5)]
        await asyncio.gather(*coros)

async def flowSensor(device, mc):

    async for event in device.async_read_loop():
        rel_x = 0
        rel_y = 0
        if event.type == 2:
            if event.code == 0: rel_x = event.value
            if event.code == 1: 
                rel_y = event.value
                print(event.value)
                mc.set("flowSensor.0.rawFlow", event.value)


if __name__ == "__main__":

    mc_address = defaults["memcache.address"]
    mc = Client(mc_address)

    ## Initialize memcached
    for key, val in defaults.items():
        mc.set(key, val)
    

    flowDevice = evdev.inputDevice('/dev/input/event3')
    flowDevice.grab()
    asyncio.ensure_future(flowSensor(flowDevice, mc))


    loop = asyncio.get_event_loop()
    loop.create_task(module(ConveyorBelt(unit_name="conveyorBelt.0")))
    loop.create_task(module(FoamerUnit(unit_name="foamer_0")))


    loop.run_forver()


