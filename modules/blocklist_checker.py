#!/usr/bin/env python


"""
    ### Blocklist Checker

    This function 
    
    # Input:  - a single bacon
              - type of the bacon [ipv4, ipv6, domain]
    # Output: - a list of dictionary contains 
"""


from modules.whois.ip_api import ip_api
from modules.whois.utils import validate_ip
from modules.blocklist.dnsbl import dnsbl
from modules.blocklist.gray_noise import gray_noise


def blocklist_checker(bacon, type):

    type = type.lower()

    # return the results in the format of set
    return 
