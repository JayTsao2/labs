from napalm import get_network_driver


if __name__ == '__main__':

    driver = get_network_driver('ios')
    device = driver('192.168.56.103', 'cisco', 'cisco123!')
    
    print("Opening ...")
    device.open()

    print("Loading replacement candidate ...")
    device.load_replace_candidate(filename='./config-ios/221020.conf')

    # Note that the changes have not been applied yet. Before applying
    # the configuration you can check the changes:
    print("\nDiff:")
    print(device.compare_config())