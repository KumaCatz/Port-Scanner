import socket
import re
from common_ports import ports_and_services

def get_open_ports(target, port_range, verbose = False):
    open_ports = []

    try:
        pattern = r'^\d{1,3}(\.\d{1,3}){3}$'
        if re.match(pattern, target):
            host_data = socket.gethostbyaddr(target)
        else:
            host_data = socket.gethostbyname_ex(target)
    except socket.herror:
        host_data = socket.gethostbyname_ex(target)
    except socket.gaierror:
        if re.match(pattern, target):
            return 'Error: Invalid IP address'
        else:
            return 'Error: Invalid hostname'

    for port in range(port_range[0], port_range[1] + 1):
        try:
            with socket.create_connection((target, port), timeout=0.2):
                open_ports.append(port)
        except (socket.timeout, ConnectionRefusedError, OSError) as e:
            pass
    
    if verbose:
        descriptive_string = []

        if host_data[0] == host_data[2][0]:
            descriptive_string.append(f'Open ports for {host_data[0]}')
        else:
            descriptive_string.append(f'Open ports for {host_data[0]} ({host_data[2][0]})')

        descriptive_string.append('\nPORT     SERVICE')

        for port in open_ports:
            service = ports_and_services.get(port)
            descriptive_string.append(f'\n{port:<9}{service}')

        return ''.join(descriptive_string)

    return(open_ports)
