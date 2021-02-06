#!/usr/bin/env python3

'''subnetting a class C IP Address'''

def subnet_ip(addr_list):

    '''
    takes an ip address and subnet mask, calculates subnet info from subnet mask
    returns network address and broadcast address of ip address
    '''
    
    #get the ip address and subnet mask from the list
    ip_addr = addr_list[0]
    s_mask = addr_list[1]

    #save the valid block sizes for a class C ip address
    valid_block_sizes = ['128', '192', '224', '240', '248', '252']

    #get the ip address information
    network_bits = ip_addr.rindex('.')
    network_addr = ip_addr[ :network_bits].split('.')
    ip_address = ip_addr.split('.')

    #select subnet mask and convert all octets to binary
    subnet_mask = s_mask.split('.')
    subnet_mask_bin = [str(bin(int(octet))).replace('0b', '') for octet in subnet_mask]

    #calculate the number of subnets
    '''
    no of subnets = 2^x
    where x = number of 1's in subnet mask binary
    '''
    on_bits = subnet_mask_bin[-1].count('1')
    no_of_subnets = 2 ** on_bits
    print('\n' + '-'*50)
    print(f'Number of Subnets: {no_of_subnets}')


    #calculate the number of valid hosts
    '''
    valid_hosts = (2^y) - 2
    where y = number of unmasked bits (zeros)
    '''
    off_bits = subnet_mask_bin[-1].count('0')
    valid_hosts = (2 ** off_bits) - 2
    print(f'\nNumber of valid hosts: {valid_hosts}')


    #calculate the valid subnets (block size)
    '''
    block_size = 256 - subnet mask (last octet in decimal subnet mask)
    '''
    block_size = 256 - int(subnet_mask[-1])
    print(f'\nBlock size: {block_size}')
    subnet = 0
    network_addresses = [0, ]
    while subnet < 256:
        subnet += block_size
        network_addresses.append(subnet)
    twofivesix = network_addresses.pop()
    print('-'*50 + '\n')

    #calculate the broadcast address
    '''
    broadcast address = network address - 1
    '''
    broadcast_address = 0
    broadcast_addresses = []
    for network_address in network_addresses:
        if network_address == 0:
            broadcast_address = 255
            broadcast_addresses.append(broadcast_address)
        elif network_address != 0:
            broadcast_address = network_address - 1
            broadcast_addresses.append(broadcast_address)
    last_broadcast = broadcast_addresses.pop(0)
    broadcast_addresses.append(last_broadcast)


    #save the valid subnets
    valid_subnets = []
    print('-'*50)
    for i in range(len(network_addresses)):
        subnets = {}
        subnets['network_address'] = network_addresses[i]
        subnets['broadcast_address'] = broadcast_addresses[i]
        valid_subnets.append(subnets)
    for net in  range(1, len(valid_subnets)+1):
        print(f'\nSubnet {net}: {valid_subnets[net-1]}')
    print('-'*50 + '\n')

    #get network address of ip address
    network_info = {}
    for network in valid_subnets:
        if int(ip_address[-1]) > network['network_address'] and int(ip_address[-1]) < network['broadcast_address']:
            net_addr = '.'.join(network_addr) + '.' + str(network['network_address'])
            bcast_addr = '.'.join(network_addr) + '.' + str(network['broadcast_address'])
            network_info['network_address'] = net_addr
            network_info['broadcast_address'] = bcast_addr
            print('\n' + '-'*50)
            print(f"Network info for ip address: {'.'.join(ip_address)} {'.'.join(subnet_mask)}\nNetwork Address: {net_addr}\nBroadcast Address: {bcast_addr}")
            print('-'*50 + '\n')
    return network_info
        


def enter_ip():

    address = input('\nEnter ip address and subnet mask seperated by a space: ')
    addr = address.split(' ')
    return addr

if __name__ == "__main__":

    ip_address = enter_ip()    
    s = subnet_ip(ip_address)
    print(f'\nNetwork Info:\n{s}\n')
#   print(f'\n{s}\n')
