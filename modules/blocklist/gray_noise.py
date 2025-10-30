#!/usr/bin/env python


"""
    ### Vulnerability: Gray Noise API

    This function gets any report provided for IPs by the Gray Noise community.

    Read more: - https://github.com/GreyNoise-Intelligence/api.greynoise.io

    # Input:  - a single IPv4 address
    # Output: - a set of dictionaries contains verdict by the Gray Noise community
"""


from config import config
from modules.utils import url_opener, error_printer
from modules.whois.utils import validate_ip


def gray_noise(ip):
    # a set to store results
    blocked_list = set()

    # continue only if the provide IP is valid and is version 4
    if validate_ip(ip) == "4":
        # download the JSON response
        url = config['api']['gray_noise']['url_ip'].format(ip)
        results = url_opener('GET', url, '', '', '', 'json', 'Gray Noise API')[0]

        # check if there is any error in the API call
        # 0 means no error
        if results['message'] != "Success":
            errors = [
                f'There was an error in the API call {url}',
                '',
                f'Message: {results["message"]}',
                '',
                ''
            ]
            error_printer(True, errors)
            return blocked_list
        else:
            blocked_list.add({
                'by': 'Gray Noise',
                'reason': results['classification'],
                'type': 'IPv4',
                'name': ip
            })

    return blocked_list
