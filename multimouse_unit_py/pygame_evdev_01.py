import pygame

pygame.init()
window = pygame.display.set_mode((1000, 1000))

import asyncio, evdev

# how to know which is which /dev/input/event
# ls -lha /dev/input/by-path/

# modify this list to include all mouses
mouse_name_list = ["/dev/input/event3", "/dev/input/event17", "/dev/input/event18"]
device_list = [evdev.InputDevice(name) for name in mouse_name_list]

# uncomment to grab all data (cursor does not move if you grab all mouses)
# [dev.grab() for dev in device_list]

mouse_locations = [[150,150], [150,150], [150,150]]


async def print_events(device):
    async for event in device.async_read_loop():
        # put here what to do to the data
        #print(device.path, evdev.categorize(event), sep=': ')
        rel_x = 0
        rel_y = 0
        if event.type == 2:
            mouse_no = device.path.split("event")[1]
            if event.code == 0: rel_x = event.value
            if event.code == 1: rel_y = event.value
            #print(device.path.split("event")[1], " ", event.value)
        
        map_mouse = {'3'  : 0,
                     '17' : 1,
                     '18' : 2}

        mouse_locations[map_mouse[mouse_no]][0] += rel_x 
        mouse_locations[map_mouse[mouse_no]][1] += rel_y 
        
        mouse_colors = [[255,0,0], [0,255,0], [0,0,255]]

        

        window.set_at( mouse_locations[map_mouse[mouse_no]],
                        mouse_colors   [map_mouse[mouse_no]])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        #window.fill(0)

        #rect = pygame.Rect(window.get_rect().center, (0, 0)).inflate(*([min(window.get_size())//2]*2))
    
        #for x in range(rect.width):
        #    u = x / (rect.width - 1)
        #    color = (round(u*255), 0, round((1-u)*255))
        #    for y in range(rect.height):
        #        window.set_at((rect.left + x, rect.top + y), color) 
    
        pygame.display.flip()

for device in device_list:
    asyncio.ensure_future(print_events(device))

loop = asyncio.get_event_loop()
loop.run_forever()

