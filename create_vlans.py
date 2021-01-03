import yaml

def create_vlan():

    '''creates vlans from user input and saves in a config file'''

    vlans_list = []
    #get the number of vlans from the user
    num_vlans = int(input('\nEnter the number of vlans to create: '))
    for c in range(1, num_vlans+1):
        vlans = {}
        print(f'\nVLAN setup {c}\n')
        vlan_id = input('vlan id: ')
        vlan_name = input('vlan name: ')
        vlans['id'] = vlan_id
        vlans['name'] = vlan_name
        vlans_list.append(vlans)
    with open('yaml-configs/vlan_commands.yaml', 'a') as vlan_commands_file:
        vlans_list = yaml.dump(vlans_list, vlan_commands_file)


if __name__ == "__main__":
    create_vlan()