#!/usr/bin/env python


"""
    ### Whois: Utilities

    Here is the list of general functions used for whois queries
    for IP addresses and domains
"""

import ipaddress


# validate the Ipv4 or IPv6
# if the IP address is valid, returns IP version (4 or 6), otherwise False
def validate_ip(ip):
    try:
        ip = ipaddress.ip_address(ip)
        return str(ip.version)
    except ValueError:
        return False
