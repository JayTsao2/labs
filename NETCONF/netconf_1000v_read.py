from ncclient import manager
import xml.dom.minidom

m = manager.connect( 
    host="192.168.56.103",
    port=830,
    username="cisco",
    password="cisco123!",
    hostkey_verify=False 
    )

netconf_filter = """
                <filter>
                    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
                        
                    </native>
                </filter>
                """
#<hostname></hostname>
#<interface></interface>

result = m.get_config(source = "running", filter = netconf_filter)

print(xml.dom.minidom.parseString(result.xml).toprettyxml())