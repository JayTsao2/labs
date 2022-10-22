import requests                                                        # API requests
import json                                                            # JSON formatting
import time                                                            # Time module
from ncclient import manager                                           # Manager class from ncclient module
import xml.dom.minidom                                                 # xml.dom.minidom module to prettify XML output
import re                           # Regular expressions module
import sys                          # System specific functions: sys.exit() to exit the program

###########################################################################################
# User hardcodes their own WebEx Teams token after "Bearer " (keep the code then secret!)
###########################################################################################

accessToken = "YmIxMDRkMDUtZDZjYi00OTliLWEwNDMtMDVjMzE4MTA2ZDljYzA3OWNkOGUtZWEy_P0A1_4fbc8836-28d2-47cd-9b80-e05ba83c5673"


#######################################################################################
#     Using the requests library, create a new HTTP GET Request against the Cisco API Endpoint 
#     for WebEx Teams Rooms.
#######################################################################################


def get_webexteams_room(access_token):

    #  Student Step #3
    #     Modify the code below to use the Cisco WebEx Teams Rooms API endpoint (URL)
    #     r = requests.get(   
    #                        "<!!!REPLACEME with URL for Cisco WebEx Teams Rooms API!!!>", 
 
    r = requests.get(
        "https://api.ciscospark.com/v1/rooms",
        headers={'Authorization': f'Bearer {access_token}'}
        )

    if not r.status_code == 200:
        raise Exception("Incorrect reply from Cisco WebEx Teams API. Status code: {}. Text: {}".format(r.status_code, r.text))   
    else:
        print("Status code 200 (Ok)")
    
    #################################################################### 
    # Prints list of WebEx Teams rooms 
    ####################################################################

    # The list of rooms stored in the r variable is converted to JSON and stored in the rooms variable. 
    # "items" is a list of dictionaries with ['title'] one of the key data elements in each dictionary. 
    # The WebEx Teams API documentation for listing rooms to examine the other response properties for the array "items". 

    print("\nList of rooms:")
    rooms = r.json()['items']

    #  Student Step #4
    #     Modify the code below to print the user-friendly name of each room.
    #     print (room['<!!! REPLACEME to display the room name !!!>'])

    for room in rooms:
        print (room['title'])

    # Defines a variable that will hold the roomId
    while True:
        # Input value into roomNameToSearch to select the room to be used
        room_name_to_search = input("\nWhich room do you check for 'configure hostname <hostname>' message? (Can use partial name of the room.) ")
        rooms = r.json()['items']
        for room in rooms:
            # Searches for the room name using the variable roomNameToSearch
            if not room['title'].find(room_name_to_search) == -1:
                # Displays the rooms found using the variable roomNameToSearch (additional options incuded)
                print ("\nFound rooms with the word " + room_name_to_search)
                print(room['title'])
                return room
        print("\nSorry, I didn't find any room with " + room_name_to_search + " in it.")
        print("\nPlease try again...")

###############################################################
# Get the WebEx Teams message from the room previously selected
# Uses variables: roomID and roomIdToMessage
# Returns message (text of message)
############################################################### 

def get_webexteams_messages(access_token, room_id):

    # run this until a message is retrieved
    while True:
        print(".")

        # add a short delay to not reach API rate-limits
        time.sleep(3)

        #  Student Step #5
        #     Modify the code below to use the Cisco WebEx Teams Messages API endpoint (URL)
        #     r = requests.get(   
        #                        "<!!!REPLACEME with URL for Cisco WebEx Teams Messages API!!!>",

        r = requests.get(
            "https://api.ciscospark.com/v1/messages",
            params = { "roomId": room_id, "max": 1 }, # retrieve only the last 1 message in the space
            headers = {"Authorization": f'Bearer {access_token}'} 
            )
        
        # check if we reached the API rate-limits
        if r.status_code == 429:
            # if so, let's delay the execution of the code
            retry_after = int(r.headers["Retry-After"])
            print ("Regetting in {} seconds ...".format(retry_after))
            time.sleep(retry_after)
            continue
        
        # should the reply's HTTP error code be anything else than 200, it's probably an error
        if not r.status_code == 200:
            raise Exception("Incorrect reply from Cisco WebEx Teams API. Status code: {}. Text: {}".format(r.status_code, r.text))

        # In order to retrieve the data from the response object, 
        # we need to convert the raw response content into a JSON type data structure
        # r.json()' creates a Python dictionary from the JSON response given by the API website.
        # The response data is a list ("items") of dictionaries

        # all seems to be fine, let's get the json formatted data
        json_data = r.json()
        
        # check if any messages have been retrieved
        if len(json_data["items"]) == 0:
            continue
        
        #  Only one dictionary (last message) was received in the get request (max = 1)
        #  return back only the text of the retrieved single (last) message

        #  Assign key/value data elements for this dictionary data element (last message) to "messages"
        messages = json_data["items"]

        #  Using key "text" assign the value to the variable message 
        #  [0] refers to the first and only dictionary item in the list)
        message = messages[0]["text"]
        
        # Returns text of the last message in this room
        return message      


##############################################################
#   Sends message to room selected previously
##############################################################

def send_webexteams_message(access_token, room_id, confirmation):
    # run this until a message is sent
    while True:

        #  Student Step #5
        #     Modify the code below to use the Cisco WebEx Teams Messages API endpoint (URL)
        #     r = requests.get(   
        #                        "<!!!REPLACEME with URL for Cisco WebEx Teams Messages API!!!>",

        r = requests.post(
            "https://api.ciscospark.com/v1/messages", 
            data = json.dumps( { "roomId": room_id, "text": confirmation } ), 
            headers = { "Authorization": f'Bearer {access_token}', "Content-Type": "application/json" } 
            )

        # check if we reached the API rate-limits
        if r.status_code == 429:
            # if so, let's delay the execution of the code
            retry_after = int(r.headers["Retry-After"])
            print ("Resending in {} seconds ...".format(retry_after))
            time.sleep(retry_after)
            continue

        # should the reply's HTTP error code be anything else than 200, it's probably an error
        if not r.status_code == 200:
            raise Exception("Incorrect reply from Cisco WebEx Teams API. Status code: {}. Text: {}".format(r.status_code, r.text))

        # all seems to be fine, time to return back
        return




# ************************************************************************
#
#   Main Program starts here
#
# ************************************************************************

##########################################################################
#   from ncclient import manager
#   Creates a variable m to represent the connection() method. 
#   The connection() method includes all the information that is required to 
#   connect to the NETCONF service running on the CSR1kv 
#   For host: IPv4 address may differ 192.168.56.x (ping CSR1kv to verify)
##########################################################################

m = manager.connect( 
    host="192.168.56.103",
    port=830,
    username="cisco",
    password="cisco123!",
    hostkey_verify=False 
    )

#########################################################################
#    Following this comment and using the accessToken variable below, modify the code to
#    ask user to use either the hardcoded or user entered access token.
#    The access token hardcoded above.
###########################################################################

choice = input("Do you wish to use the hard-coded token? (y/n)")
 
if choice == "N" or choice == "n":
    accessToken = input("user-entered access token : ")
    # No else - accessToken has a previously assigned value

# identifies which webex teams room (space) to look for new messages
room = get_webexteams_room(accessToken)

# Stores room id and room title into variables
room_id = room['id']
room_title = room['title']

# checking for messages and applying intended config changes
while True:
    message = get_webexteams_messages(accessToken, room_id)
    print("Received message: {}".format(message))
    
    # Uses the regular expressions function to look for the words "configure hostname" in message and assign it to match
    match = re.match(".*configure hostname (.*)", message)
    if match:
        # After the message string "configure hostname" the next characters in the match group will be the value for the variable hostname
        hostname = match.groups()[0]

        # Student Step #9
        # Complete the NETCONF configuration template below to include the ending XML tags
        # "<!!! ADD ENDING XML TAGS !!!>"

        # This is the NETCONF configuration template used to by the m.edit_config containing the value for HOSTNAME 
        netconf_config_template = """ 
        <config>
            <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
                <hostname>{HOSTNAME}</hostname>
            </native>
        </config>
        """
        # This is the edit_config() function of the m NETCONF session object to send the configuration 
        # and store the results in the netconf_reply variable so that they can be printed. 
        nenetconf_reply = m.edit_config(target = "running", config = netconf_config_template.format(HOSTNAME=hostname))
 
        # This calls a function with a message that will be sent to the WebEx Teams room  
        send_webexteams_message(
            accessToken, 
            room_id, 
            "Hostname has been updated to {HOSTNAME}.".format(HOSTNAME=hostname) 
            )
 
        # This confirms in the terminal screen that the event was successful including NETCONF
        # validation using get_config()
        print('\nFrom the WebEx Teams Room "{ROOMTITLE}", NETCONF has automatically updated the CSR1kv router with the hostname "{HOSTNAME}"'.format(ROOMTITLE=room_title, HOSTNAME=hostname))
        print("\nHere is your NETCONF m.get_config() validation: ")

        # This is the NETCONF filter used by the m.get_config to filter everything out but the hostname
        netconf_filter = """
                <filter>
                    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
                        <hostname></hostname>
                    </native>
                </filter>
                """
        result = m.get_config(source = "running", filter = netconf_filter)
        print(xml.dom.minidom.parseString(result.xml).toprettyxml())
        print("\nThank you! Your automatic update using NETCONF is now complete.")

        sys.exit()

    else:
        # Displays a message to remind the user to enter the proper information into the correct room
        print('Waiting for user to enter "configure hostname <hostname>" in WebEx Teams room {ROOMTITLE}'.format(ROOMTITLE=room_title))



