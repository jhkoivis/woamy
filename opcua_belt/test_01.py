


import sys

from opcua import Client



client = Client("opc.tcp://10.0.0.53:4840")

#client.set_security_string("Basic256")

#client.set_password("test")
#client.activate_session(username="test", password = "test")

try:
    client.connect()

    root = client.get_root_node()

    print("Objects node is: ", root)

    print("Children: ", root.get_children())

    obj = root.get_child(["0:Objects", "4:EwonTags", "4:ewon_sys_up"])
    print("MyObject is: ", obj)


    print("value: ", obj.get_value())

finally:

    client.disconnect()



