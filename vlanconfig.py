''' Write a script that connects to a device(s) (cisco switch), logs in and sets up vlan configurations '''

import time
import yaml
from create_vlans import create_vlan

def send_save_config(devicee):

    '''sends configuration commands to save running configuration to startup configuration'''
        
    with open('yaml-configs/save_config.yaml') as save_file:
        save_commands = yaml.full_load(save_file)

    print('-'*50)
    print(f'\nsaving configurations for {devicee}...')
    time.sleep(1)
    for command in save_commands:
        print(f'\ncommand sent...{command}')
        time.sleep(1)
    print('-'*50)


def send_vlan_config(devicee):

    '''sends configuration commands to set up valns'''

    with open('yaml-configs/vlan_commands.yaml') as vlan_config_file:
        vlan_commands = yaml.full_load(vlan_config_file)

    print('-'*50)
    print(f'\nsending vlan configuration commands for {devicee}...\n')
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


def send_login_config(devicee):

    '''sends configuration commands to log into a device'''

    with open('yaml-configs/login_config.yaml') as login_file:
        login_commands = yaml.full_load(login_file)

    print('-'*50)
    print(f'\nsending login configuration commands for {devicee}...')
    time.sleep(1)
    for command in login_commands:
        print(f'\ncommand sent...{command}')
        time.sleep(1)
    print('-'*50)     


def get_vlan_command():

    '''gets vlan configuration commands from user and returns a list of the commands'''

    new_vlan_list = ['y', 'n']
    new_vlan = input('add new vlan?(y/n): ')
    if new_vlan.lower() not in new_vlan_list:
        get_vlan_command()
    elif new_vlan.lower() == 'n':
        pass
    elif new_vlan.lower() == 'y':
        create_vlan()



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
    with open('yaml-configs/switches.yaml') as switch_file:
        switches = yaml.full_load(switch_file)
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
    get_vlan_command()
    start_time = time.time()
    
    #configure the device
    for device in connected_devices:
        print(f'\nConnecting to switch {device}...\n')
        time.sleep(1)
        print('#'*50)
        print(f'Connected: {device}\n')
        time.sleep(1)
        send_login_config(device)
        send_vlan_config(device)
        send_save_config(device)
        print('#'*50)
    
    stop_time = time.time()
    prog_time = round(stop_time - start_time, 2)
    program_time = f'{prog_time}'
    print(f'\nconfiguration time: {program_time} secs\n')