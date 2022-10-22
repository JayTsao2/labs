from ncclient import manager
import xml.dom.minidom

m = manager.connect( 
    host="192.168.56.103",
    port=830,
    username="cisco",
    password="cisco123!",
    hostkey_verify=False 
    )

hostname = "Jay_Hostname_1022_1"

netconf_filter = """
                <filter>
                    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
                        <hostname></hostname>
                    </native>
                </filter>
                """

netconf_config_template = """ 
        <config>
            <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
                <hostname>{HOSTNAME}</hostname>
            </native>
        </config>
        """

netconf_reply = m.edit_config(target = "running", config = netconf_config_template.format(HOSTNAME=hostname))

result = m.get_config(source = "running", filter = netconf_filter)

print(xml.dom.minidom.parseString(result.xml).toprettyxml())