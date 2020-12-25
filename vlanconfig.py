''' Write a script that connects to a device(s) (cisco switch), logs in and sets up vlan configurations '''




import time




def save_config(devicee):

    '''sends configuration commands to save running configuration to startup configuration'''

    save_commands = ['exit', 'save run start', 'y']
    print('-'*50)
    print(f'\nSaving configurations for {devicee}...')
    time.sleep(1)

    for command in save_commands:

        print(f'\ncommand sent...{command}')
        time.sleep(1)
    print('-'*50)




def vlan_config(devicee):

    '''sends configuration commands to set up valns'''

    print('-'*50)
    print(f'\nsending vlan configurations for {devicee}...\n')
    time.sleep(1)

    for command in vlan_commands:
        v_id = command.get('id')
        v_name = command.get('name')
        print(f'command sent...vlan {v_id}')
        time.sleep(1)
        print(f'command sent...{v_name}')
        time.sleep(1)
        print(f'command sent...exit\n')
        time.sleep(1)
    print('-'*50)




def login_config(devicee):

    '''sends configuration commands to log into a device'''

    login_commands = ['enable', 'conf t',]
    print('-'*50)
    print(f'\nsending login configurations for {devicee}...')
    time.sleep(1)

    for command in login_commands:
        print(f'\ncommand sent...{command}')
        time.sleep(1)
    print('-'*50)
        



def get_vlan_command():

    '''gets vlan configuration commands from user and returns a list of the commands'''

    vlans_list = []

    #get the number of vlans from the user
    num_vlans = int(input('Enter the number of vlans to create: '))

    for c in range(1, num_vlans+1):
        vlans = {}
        print(f'\nVLAN setup {c}\n')
        vlan_id = input('vlan id: ')
        vlan_name = input('vlan name: ')
        vlans['id'] = vlan_id
        vlans['name'] = vlan_name
        vlans_list.append(vlans)
    return vlans_list




def select_switches(number):

    '''takes a number, accepts inputs for that range and returns a list of the input'''

    #select the switches
    selected_switches = []
    for a in range(1, number+1):
        selected_switch = int(input(f'Enter selected switch {a} id: '))
        print('\n')
        selected_switches.append(selected_switch)
    
    return selected_switches




def user_num():

    '''returns number of switches to connect to as declared by user'''

    #ask the user for the number of devices to connect to (error avoidance: show max number)
    num_switches = int(input(f'Enter the number of switches to connect to (max={max_num}): '))
    print('\n')
    return num_switches




def connect():

    '''connects to the devices (switches) selected by the user'''

    numb_switches = user_num()

    while numb_switches > max_num or numb_switches < 1:

        #humans right (sigh)... still capture errors
        if numb_switches > max_num:
            print(f'ERROR: Number of available switches less than {numb_switches}')
            numb_switches = user_num()
        elif numb_switches < 1:
            print(f'ERROR: {numb_switches} is an invalid choice')
            numb_switches = user_num()

    #select the switches
    select_switch = select_switches(numb_switches)

    #confirm user choice and connect
    try:

        connected_switches = []
        for select in select_switch:
            connected_switch = switches[select-1]
            connected_switches.append(connected_switch)

    except Exception:

        print(f'\nInvalid Input\n')
        connect()
        
    return connected_switches




if __name__ == "__main__":

    #get a list of switches
    switches = ['ground_floor', 'floor1', 'floor2', 'floor3', 'floor4', 'floor5', 'floor6']
    max_num = len(switches)

    #display available switches to user
    print('\nSELECT AN ID TO CONNECT TO A SWITCH\n'.center(15, ' '))
    print(f'SWITCHES\n'.center(15, ' '))
    accepted_input = []
    print(f'id.'.ljust(5, ' ') + 'Switch'.ljust(5, ' ') + '\n')
    for idd, switch in enumerate(switches,start=1):
        print( (str(idd) + '.').ljust(5, ' ') + switch.ljust(5, ' ') + '\n' )
        accepted_input.append(idd)

    #connect to the device(s)
    connected_devices = connect()    

    #get the vlan commands
    vlan_commands = get_vlan_command()

    start_time = time.time()

    #configure the device
    for device in connected_devices:
        print(f'\nConnecting to switch {device}...\n')
        time.sleep(1)
        
        print('#'*50)
        print(f'Connected: {device}\n')
        time.sleep(1)
        login_config(device)
        vlan_config(device)
        save_config(device)
        print('#'*50)
    
    stop_time = time.time()

    program_time = round(stop_time - start_time, 2)

    print(f'\nconfiguration time: {program_time}\n')