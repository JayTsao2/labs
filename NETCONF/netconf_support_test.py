from ncclient import manager

m = manager.connect( 
    host="192.168.56.103",
    port=830,
    username="cisco",
    password="cisco123!",
    hostkey_verify=False 
    )

for RTR_Capability in m.server_capabilities:
    print(RTR_Capability)

m.close_session()