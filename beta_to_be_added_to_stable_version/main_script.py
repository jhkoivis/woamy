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




async def conveyorBelt():

    device          = ConveyorBelt(unit_name="conveyorBelt.0")

    coros           = [device._init(), asyncio.sleep(0.5)]
    await asyncio.gather(*coros)
    while true:
        coros       = [device.update(), asyncio.sleep(0.5)]
        await asyncio.gather(*coros)

async def foamer():

    device          = FoamerUnit(unit_name="foamer_0")
    
    coros           = [device._init(), asyncio.sleep(0.5)]
    await asyncio.gather(*coros)
    while true:
        coros       = [device.update(), asyncio.sleep(0.5)]
        await asyncio.gather(*coros)

async def flowSensor(device, mc):

    async for event in device.async_read_loop():
        # put here what to do to the data
        #print(device.path, evdev.categorize(event), sep=': ')
        rel_x = 0
        rel_y = 0
        if event.type == 2:
            #print(device.path)
            #print(  time.time(),
            #        mouse_locations[0][0],
            #        mouse_locations[1][0],
            #        mouse_locations[2][0])
            #mouse_no = device.path.split("event")[1]
            if event.code == 0: rel_x = event.value
            if event.code == 1: 
                rel_y = event.value
                print(event.value)
                mc.set("flowSensor.0.rawFlow", event.value)

        #mouse_locations[mouse_name_list.index(device.path)][0] += rel_x
        #mouse_locations[mouse_name_list.index(device.path)][1] += rel_y

        #mouse_colors = [[255,0,0], [0,255,0], [0,0,255]]

        #window.set_at( mouse_locations[mouse_name_list.index(device.path)],
        #                mouse_colors  [mouse_name_list.index(device.path)])

        #for event in pygame.event.get():
        #    if event.type == pygame.QUIT:
        #        run = False    


    #device          = FlowSensor(unit_name="flowSensor.0")
    #
    #coros           = [device._init(), asyncio.sleep(0.5)]
    #await asyncio.gather(*coros)
    #while true:
    #    coros       = [device.update(), asyncio.sleep(0.5)]
    #    await asyncio.gather(*coros)
    





#def init_all():
#
#    mc_address = defaults["memcache.address"]
#    mc = Client(mc_address)
#
#   ## Initialize memcached
#    for key, val in defaults.items():
#        mc.set(key, val)
#
#    conveyorBelt_0  = ConveyorBelt(unit_name="conveyorBelt.0")
#    foamer_0        = FoamerUnit(unit_name="foamer_0")
#    flowSensor_0    = FlowSensor(unit_name="flowSensor.0")
#    
#    
#async def run_machine():
#
#    ## Create objects for each "module"
#    conveyorBelt_0 = ConveyorBelt(unit_name="conveyorBelt.0")
#    foamer_0 = FoamerUnit(unit_name="foamer_0")
#    ## Initialize objects using concurrency
#    oliot = []
#    for device in eval(mc.get("listOfDevices").decode("ascii")):
#        oliot.append(eval(device))
#
#
#    coros = [getattr(olio, "_init")() for olio in oliot]
#    await asyncio.gather(*coros)
#
#    ## Start the main loop 
#    ## On each step run the "update" mehtod of the object
#    for ind in range(200000):
#
#        oliot = []
#        for device in eval(mc.get("listOfDevices").decode("ascii")):
#            oliot.append(eval(device))
#
#        coros = [getattr(olio, "update")() for olio in oliot]
#        coros.append(asyncio.sleep(0.5))
#        results = await asyncio.gather(*coros)
#        ##await asyncio.sleep(1)
#
#
#    oliot = []
#    for device in eval(mc.get("listOfDevices").decode("ascii")):
#        oliot.append(eval(device))
#    coros = [getattr(olio, "close_connection")() for olio in oliot]
#    results = await asyncio.gather(*coros)

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
    loop.create_task(conveyorBelt())
    loop.create_task(foamer())


    loop.run_forver()





    #print("start execution")
    #asyncio.run(run_machine())


