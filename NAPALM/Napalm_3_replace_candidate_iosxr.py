from napalm import get_network_driver


if __name__ == '__main__':

    driver = get_network_driver('iosxr')
    device = driver('10.188.1.94', 'admin', '1234QWer')
    
    print("Opening ...")
    device.open()

    print("Loading replacement candidate ...")
    device.load_replace_candidate(filename='./config-iosxr/iosxr_221021.conf')

    # Note that the changes have not been applied yet. Before applying
    # the configuration you can check the changes:
    print("\nDiff:")
    print(device.compare_config())