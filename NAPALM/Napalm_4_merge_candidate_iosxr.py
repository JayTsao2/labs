from napalm import get_network_driver

if __name__ == '__main__':

    driver = get_network_driver('iosxr')
    device = driver('10.188.1.94', 'admin', '1234QWer')
    
    print("Opening ...")
    device.open()

    print("Loading replacement candidate ...")
    device.load_merge_candidate(filename='./config-iosxr/router_static.conf')

    # Note that the changes have not been applied yet. Before applying
    # the configuration you can check the changes:
    print("\nDiff:")
    print(device.compare_config())

    try:
        choice = input("\nWould you like to commit these changes? [yN]: ")
    except NameError:
        choice = input("\nWould you like to commit these changes? [yN]: ")
    if choice == "y":
        print("Committing ...")
        device.commit_config()
    else:
        print("Discarding ...")
        device.discard_config()

    # close the session with the device.
    device.close()
    print("Done.")