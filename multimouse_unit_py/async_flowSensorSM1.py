import pygame
import subprocess
import time

pygame.init()
window = pygame.display.set_mode((1000, 1000))

import asyncio, evdev

# how to know which is which /dev/input/event
# ls -lha /dev/input/by-path/

out = subprocess.run(["ls", "-lha", "/dev/input/by-path/"], capture_output=True)

print(out.stdout)

mouse_name_list = []
for line  in out.stdout.decode("utf-8").split('\n'):
    if "../event" in line and "mouse" in line:
        mouse_name = "/dev/input/event" + line.split("../event")[1].strip()
        mouse_name_list.append(mouse_name)

print(mouse_name_list)

# modify this list to include all mouses
#mouse_name_list = ["/dev/input/event3", "/dev/input/by-path/pci-0000:00:14.0-usb-0:6.3:1.0-event-mouse", "/dev/input/mouse2"]
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
            #print(device.path)
            print(  time.time(),
                    mouse_locations[0][0],
                    mouse_locations[1][0],
                    mouse_locations[2][0])
            mouse_no = device.path.split("event")[1]
            if event.code == 0: rel_x = event.value
            if event.code == 1: rel_y = event.value
            #print(device.path.split("event")[1], " ", event.value)

        mouse_locations[mouse_name_list.index(device.path)][0] += rel_x
        mouse_locations[mouse_name_list.index(device.path)][1] += rel_y

        mouse_colors = [[255,0,0], [0,255,0], [0,0,255]]

        window.set_at( mouse_locations[mouse_name_list.index(device.path)],
                        mouse_colors  [mouse_name_list.index(device.path)])

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
