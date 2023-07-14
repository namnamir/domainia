#!/usr/bin/env python


"""
    ### Vulnerability Scanner: Check Host

    This function gets the open ports

    Read more: - https://check-host.net/about/api

    # Input:  - a single domain name or IP address
    # Output: - a set contains open TCP/UDP ports
"""


from time import sleep

from config import config
from modules.utils import url_opener


def criminal_ip(bacon, protocol):
    # variables to store subdomains and related domains
    port_status = set()

    # the HTTP headers to send to Check Host
    headers = {'Accept': 'application/json'}

    # get the list of the ports
    if protocol == 'TCP':
        ports = config['scan_type']['tcp_ports']
    elif protocol == 'UDP':
        ports = config['scan_type']['udp_ports']
    else:
        ports = [21, 22, 25, 80, 143, 443, 587, 993, 995, 2082, 2077, 3306]

    # do scan for each port
    for port in ports:
        # add the port number to the bacon
        bacon = f'{bacon}:{str(port)}'
        # form the url to be requested
        if protocol == 'UDP':
            url = config['api']['check_host']['url_udp_port'].format(bacon)
        else:
            url = config['api']['check_host']['url_tcp_port'].format(bacon)
        # request the port scan from Check Host
        request_id = url_opener('GET', url, '', '', headers, 'json', False)
        request_id = request_id[0]['request_id']

        # sleep for a certain time to
        sleep(config['api']['check_host']['delay'])

        # get the results
        url = config['api']['check_host']['url_result'].format(request_id)
        results = url_opener(
            'GET', url, '', '', headers, 'json',
            f'Check Host API for port {port}'
        )

        # set the
        status = 'closed'

        # iterate over the result of each probe
        for result in results:
            # if any probes says that the port is open, see it as open
            if result and 'time' in result[0]:
                port_status = 'open'
                break

        # add the port to the set
        port_status.add(
            {
                'port': port,
                'status': status,
                'protocol': protocol,
                'service': '',
            }
        )

    # return gathered data
    return port_status
