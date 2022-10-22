import napalm
from tabulate import tabulate
 
def main():
 
    driver_ios = napalm.get_network_driver("ios")
    driver_nxos = napalm.get_network_driver("nxos")
    driver_iosxr = napalm.get_network_driver("iosxr")
 
    device_list = [
    ["10.188.1.95","nxos", "router_2"],
    ["10.188.1.94", "iosxr", "router_1"]
    
    # Remark cause no bgp running, key value will be null
    #,
    #["192.168.56.103", "ios", "switch"]
    ]
 
    network_devices = []
    for device in device_list:
        if device[1] == "nxos":
            network_devices.append(
                            driver_nxos(
                            hostname = device[0],
                            username = "admin",
                            password = "1234QWer"
                            )
                              )
        elif device[1] == "iosxr":
            network_devices.append(
                            driver_iosxr(
                            hostname = device[0],
                            username = "admin",
                            password = "1234QWer"
                            )
                              )
        elif device[1] == "ios":
            network_devices.append(
                            driver_ios(
                            hostname = device[0],
                            username = "cisco",
                            password = "cisco123!"
                            )
                              )

    devices_table = [["hostname", "vendor", "model", "uptime", "serial_number"]]
    
    devices_table_int = [["hostname","interface","is_up", "is_enabled", "description", "speed", "mtu", "mac_address"]]
    
    #Select column from get_bgp_neighbors
    devices_table_bgp = [["hostname", "neighbor", "remote-as", "status", "sent prefixes", "received prefixes"]]
 
    for device in network_devices:
        print("Connecting to {} ...".format(device.hostname))
        device.open()
 
        print("Getting device facts")
        device_facts = device.get_facts()
 
        devices_table.append([device_facts["hostname"],
                              device_facts["vendor"],
                              device_facts["model"],
                              device_facts["uptime"],
                              device_facts["serial_number"]
                              ])

        print("Getting device interfaces")
        device_interfaces = device.get_interfaces()
        for interface in device_interfaces:
            devices_table_int.append([device_facts["hostname"],
                                  interface,
                                  device_interfaces[interface]['is_up'],
                                  device_interfaces[interface]['is_enabled'],
                                  device_interfaces[interface]['description'],
                                  device_interfaces[interface]['speed'],
                                  device_interfaces[interface]['mtu'],
                                  device_interfaces[interface]['mac_address']
        ])

        if not "SW" in device_facts["hostname"]:
            print("Getting device BGP Neighbors")
            device_bgp_peers = device.get_bgp_neighbors()
 
            address_fam = "ipv4 unicast"
            if "router" in device_facts["hostname"]:
                address_fam = "ipv4"
            
            for bgp_neighbor in device_bgp_peers['global']['peers']:
                devices_table_bgp.append([device_facts["hostname"],
                                          bgp_neighbor,
                                          device_bgp_peers['global']['peers'][bgp_neighbor]['remote_as'],
                                          device_bgp_peers['global']['peers'][bgp_neighbor]['is_up'],
                                          device_bgp_peers['global']['peers'][bgp_neighbor]['address_family'][address_fam]['sent_prefixes'],
                                          device_bgp_peers['global']['peers'][bgp_neighbor]['address_family'][address_fam]['received_prefixes']
                                     ])

        device.close()
        print("Done.")
    print(tabulate(devices_table, headers="firstrow"))
    print()
    print(tabulate(devices_table_int, headers="firstrow"))
    print()
    print(tabulate(devices_table_bgp, headers="firstrow"))
 
if __name__ == '__main__':
    main()