#!/usr/bin/env python

from config import config
from modules.utilities.url_opener import url_opener
from modules.whois.utils import validate_ip


def ip_api(ip):
    """
        ### Whois: IP API

        This function gets the whois of the given IP as well as some checks
        like if the IP hosts sites, provides VPN, or belongs to a mobile device.

        # Input:  - a single IP address
        # Output: - a dictionary contains whois details
                - a set contains tags related to the IP such as if the IP is used
                    for hosting, VPN, etc.
                - a string returns the reversed DNS of the given IP
    """
    # a variable to store results
    ip_whois = dict()
    vulnerabilities = set()
    reverse_dns = ''

    # check if the ip is a valid one
    if not validate_ip(ip):
        return ip_whois

    # call the API
    url = config['api']['ip_api']['url_lookup'].format(ip, config['api']['ip_api']['fields'])
    results = url_opener('GET', url, '', '', '', 'json', 'IP API')[0]

    # write the data into the dictionary
    if results:
        ip_whois['name'] = ip
        ip_whois['continent'] = results['continent']
        ip_whois['continent_code'] = results['continentCode']
        ip_whois['country'] = results['country']
        ip_whois['country_code'] = results['countryCode']
        ip_whois['region'] = results['regionName']
        ip_whois['district'] = results['district']
        ip_whois['city'] = results['city']
        ip_whois['zip_code'] = results['zip']
        ip_whois['latitude'] = results['lat']
        ip_whois['longitude'] = results['lon']
        ip_whois['timezone'] = results['timezone']
        ip_whois['time_offset'] = results['offset']
        ip_whois['isp'] = results['isp']
        ip_whois['organization'] = results['org']
        ip_whois['as_number'] = results['as']
        ip_whois['as_name'] = results['asname']

        reverse_dns = results['reverse']

        vulnerabilities.add(
            {
                'name': 'is_mobile',
                'risk':  None if results['mobile'] else 'info'
            },
            {
                'name': 'is_hosting',
                'risk':  None if results['hosting'] else 'info'
            },
            {
                'name': 'is_proxy',
                'risk': None if results['proxy'] else 'medium'
            },
        )

    # return the whois of the IP
    return [
        ip_whois,
        vulnerabilities,
        reverse_dns
    ]
