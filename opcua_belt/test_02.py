



from opcua import Client
from opcua import ua


client = Client("opc.tcp://10.0.0.53:4840")


try:
    client.connect()
    var = client.get_node("ns=4;s=Belt_on_1_off_5")
    
    dv = ua.DataValue(ua.Variant(1.0, ua.VariantType.Float))
    #dv = ua.DataValue(ua.Variant(5.0, ua.VariantType.Float))
    
    var.set_value(dv)

finally:

    client.disconnect()


