#!/usr/bin/env python

import ipaddress
from config import config
from modules.utils import domain_sanitizer, dns_resolver

# check for DNS blocklist
def dsn_blocklist(bacons, type):
    # a variable to store results
    results = list()
    # set the print arguments for the function "run_requests"
    print_args = [False, '       │      ■ ', '       │      ■■ ']

    # form bacons
    if not isinstance(bacons, list):
        bacons = [bacons]
    
    # iterate over bacons
    for bacon in bacons:
        if type in ['ipv4', 'ipv6']:
            bacon = ipaddress.ip_address(bacon).reverse_pointer
            # strip the additional texts
            bacon = bacon.replace('in-addr.arpa', '').replace('ip6.arpa', '')
        elif type in ['domain']:
            # sanitize the domain name
            bacon = domain_sanitizer(bacon)
            bacon = bacon + '.'

        for bl, content in config['dnsbl'].items():
            if type in content['type']:
                # get the result of the DNS query
                try:
                    # get the result of A record without printing anything
                    answer = dns_resolver(bacon + bl, 'A', print_args)
                    if answer and type == 'domain':
                        results.append('by "' + bl + '" as ' + content[answer[0]][1].split(':')[0])
                    elif answer:
                        results.append(bl + ': ' + content[answer[0]][1].split(':')[0])
                except:
                    continue

    # return results
    return results
    