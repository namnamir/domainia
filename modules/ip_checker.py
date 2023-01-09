#!/usr/bin/env python


"""
    ### IP Checker

    This function gets the IP whois, the IP version, and the list of sources
    blocked the IP.
    
    # Input:  a single IP address
    # Output: a dictionary contains IP address details
"""


from modules.whois.ip_api import ip_api
from modules.whois.utils import validate_ip
from modules.vulnerability.censys import Censys
from modules.blocklist.gray_noise import gray_noise
from blocklist_checker import blocklist_checker


def ip_checker(ip):
    # a variable to store results
    ip_details = dict()

    # call different APIs
    whois, tags, reverse_dns = ip_api(ip)
    censys = Censys(ip, 'ip')

    # get the IP version
    ip_details['ip'] = ip
    ip_details['version'] = f'IPv{validate_ip(ip)}'

    # get the whois
    ip_details['whois'] = whois

    # get the list of sources mentioned the IP as an anomaly from different sources
    ip_details['listed'] = blocklist_checker(ip, "ip")
    ip_details['listed'].update(gray_noise(ip))

    # get technologies
    ip_details['technologies'] = censys['technologies']

    # get open ports
    ip_details['ports'] = censys['ports']

    # get the reverse DNS
    if reverse_dns != censys['reverse_dns']:
        reverse_dns = [reverse_dns, censys['reverse_dns']]
    ip_details['reverse_dns'] = reverse_dns

    # get the tags
    ip_details['tags'] = tags

    # return the results in the format of set
    return ip_details
