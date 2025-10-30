#!/usr/bin/env python


"""
    ### DNS Records: DNS Blocklist Checker

    This function checks the domain name, IPv4, or IPv6 against different
    different sources (defined in the config.py file) to find if it is blocked
    by any blocklist maintainer or not.

    # Input:  - a list of inputs: domain names, IPs (version 4 or 6)
              - the type of the input
    # Output: - a set of values related to the given DNS record
"""


import ipaddress

from config import config
from modules.dns.dns_resolver import dns_resolver
from modules.utilities.url_sanitizer import url_sanitizer


def dnsbl(bacons, type):
    # a variable to store results
    blocked_list = set()
    # assure that bacons is the list
    bacons = list(bacons)

    # form bacons
    if not isinstance(bacons, list):
        bacons = [bacons]

    # iterate over bacons
    for bacon in bacons:
        if type.lower() in ['ipv4', 'ipv6']:
            bacon = ipaddress.ip_address(bacon).reverse_pointer
            # strip the additional texts
            bacon = bacon.replace('in-addr.arpa', '').replace('ip6.arpa', '')
        elif type in ['domain']:
            # sanitize the domain name
            bacon = url_sanitizer(bacon)[1]
            bacon = bacon + '.'

        for bl, content in config['dnsbl'].items():
            if type in content['type']:
                # get the result of the DNS query "A" without printing it
                answer = dns_resolver(bacon + bl, 'A')
                if answer:
                    blocked_list.add({
                        'by': bl,
                        'reason': content[answer[0]][1].split(':')[0],
                        'type': type,
                        'name': bacon
                    })

    # return results
    return blocked_list
