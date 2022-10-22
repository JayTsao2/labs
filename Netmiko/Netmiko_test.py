from netmiko import ConnectHandler

net_connect = ConnectHandler(
    device_type="cisco_xe",
    host="192.168.56.103",
    username="cisco",
    password="cisco123!",
)

output = net_connect.send_command(
    "show ip arp"
)
print(output) 