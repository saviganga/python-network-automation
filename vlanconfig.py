''' Write a script that connects to a device(s) (cisco switch), logs in and sets up vlan configurations '''

import time
import yaml
from create_vlans import create_vlan
from jinja2 import Environment, FileSystemLoader
    
def send_save_config(devicee):

    '''sends configuration commands to save running configuration to startup configuration'''
        
    template_env = Environment(loader=FileSystemLoader('./templates/'))
    template_obj = template_env.get_template('send_save_config.j2')

    with open('yaml-configs/save_config.yaml') as save_file:
        save_commands = yaml.full_load(save_file)

    save_config = template_obj.render(device=devicee, save_commands=save_commands)
    print(save_config)

def send_vlan_config(devicee):

    '''sends configuration commands to set up valns'''

    template_env = Environment(loader=FileSystemLoader('./templates/'))
    template_obj = template_env.get_template('send_vlan_config.j2')

    with open('yaml-configs/vlan_commands.yaml') as vlan_config_file:
        vlan_commands = yaml.full_load(vlan_config_file)

    vlan_config = template_obj.render(device=devicee, vlan_commands=vlan_commands)
    print(vlan_config)

def send_login_config(devicee):

    '''sends configuration commands to log into a device'''

    template_env = Environment(loader=FileSystemLoader('./templates/'))
    template_obj = template_env.get_template('send_login_config.j2')

    with open('yaml-configs/login_config.yaml') as login_file:
        login_commands = yaml.full_load(login_file)

    login_config = template_obj.render(device=devicee, login_commands=login_commands)
    print(login_config)

def get_vlan_command():

    '''gets vlan configuration commands from user and returns a list of the commands'''

    with open('yaml-configs/vlan_commands.yaml') as vlan_config_file:
        vlan_commands = yaml.full_load(vlan_config_file)
    return vlan_commands

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
    print(f'id |'.ljust(5, ' ') + 'Switch'.ljust(5, ' ') + '\n')
    for idd, switch in enumerate(switches,start=1):
        print( (str(idd) + ' |').ljust(5, ' ') + switch.ljust(5, ' ') + '\n' )
        accepted_input.append(idd)
        
    #connect to the device(s)
    connected_devices = connect()    
    #get the vlan commands
    get_vlan_command()
    start_time = time.time()
    
    #configure the device
    for device in connected_devices:
        print('-'*50)
        print(f'Connected: {device}\n')
        time.sleep(1)
        send_login_config(device)
        send_vlan_config(device)
        send_save_config(device)
        print('-'*50)
    
    stop_time = time.time()
    prog_time = round(stop_time - start_time, 2)
    program_time = f'{prog_time}'
    print(f'\nconfiguration time: {program_time} secs\n')