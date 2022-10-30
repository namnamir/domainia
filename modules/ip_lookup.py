#!/usr/bin/env python

import ipaddress
from config import config
from modules.utils import run_requests


# validate the Ipv4 or IPv6
def validate_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False


# lookup the ip
def ip_lookup(ip):
    # call the IP-API and parse the data
    def ip_api(ip):
        # call the API
        print_args = [True, '      │      ■ ', '      │      ■■ ']
        url = config['api']['ipapi']['url_lookup'].format(ip, config['api']['ipapi']['fields'])
        json_data = run_requests(url, '', 'json', 'IP API', print_args)[0]

        # write the data
        ip_lookup = {
            'continent': json_data['continent'],
            'continent_code': json_data['continentCode'],
            'country': json_data['country'],
            'country_code': json_data['countryCode'],
            'region': json_data['regionName'],
            'district': json_data['district'],
            'city': json_data['city'],
            'zip_code': json_data['zip'],
            'latitude': json_data['lat'],
            'longitude': json_data['lon'],
            'timezone': json_data['timezone'],
            'time_offset': json_data['offset'],
            'isp': json_data['isp'],
            'organization': json_data['org'],
            'as_number': json_data['as'],
            'as_name': json_data['asname'],
            'reverse_dns': json_data['reverse'],
            'mobile': str(json_data['mobile']),
            'proxy': str(json_data['proxy']),
            'hosting': str(json_data['hosting']),
        }

        return ip_lookup
    
    
    # define some variables
    ip_lookup = {
        'continent': '',
        'continent_code': '',
        'country': '',
        'country_code': '',
        'region': '',
        'city': '',
        'district': '',
        'zip_code': '',
        'latitude': '',
        'longitude': '',
        'time_offset': '',
        'offset': '',
        'isp': '',
        'organization': '',
        'as_number': '',
        'as_name': '',
        'reverse_dns': '',
        'mobile': '',
        'proxy': '',
        'hosting': ''
    }

    # check if the ip is a valid one
    if validate_ip(ip):
        ip_lookup = ip_api(ip)
    
    # return the results in the format of set
    return ip_lookup
