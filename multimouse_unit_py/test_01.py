
import asyncio, evdev

# modify this list to include all mouses
mouse_name_list = ["/dev/input/event15", "/dev/input/event16"]
device_list = [evdev.InputDevice(name) for name in mouse_name_list]

# uncomment to grab all data (cursor does not move if you grab all mouses)
# [dev.grab() for dev in device_list]

async def print_events(device):
    async for event in device.async_read_loop():
        # put here what to do to the data
        print(device.path, evdev.categorize(event), sep=': ')

for device in device_list:
    asyncio.ensure_future(print_events(device))

loop = asyncio.get_event_loop()
loop.run_forever()



