#!/usr/bin/env python


"""
    ### Vulnerability Scanner: Maltiverse API

    This function gets the list of subdomains and corresponding IPs by calling 
    the Maltiverse API.

    Read more: https://app.swaggerhub.com/apis-docs/maltiverse/api/1.1

    # Input:  - a single domain name or IP address
              - the type of the asset that needs to be assessed
    # Output: - a set contains vulnerability assessment of the given domain
              - a set of dictionaries contains blocked lists
"""


from config import config
from modules.utils import run_requests, print_error
from modules.whois.utils import validate_ip


def maltiverse(bacon, type):
    # variables to store subdomains and related domains
    blocked_list = set()
    vulnerabilities = set()

    # the HTTP headers to be sent to Maltiverse
    headers = {'Accept': 'application/json'}

    # form the URL based on the type of the bacon
    if type.lower() == 'ip':
        url = config['api']['maltiverse']['url_ip'].format(bacon)
    if type.lower() == 'domain':
        url = config['api']['maltiverse']['url_domain'].format(bacon)

    # get the results in JSON from Maltiverse
    results = run_requests('GET', url, '', '', headers, 'json', 'Maltiverse API')[0]

    # if the API call returns data
    if not results['status']:
        # iterate over the 
        for listed in results['blacklist']:
            blocked_list.add({
                'by': listed['CIArmy'],
                'reason': listed['description'],
                'type': validate_ip(bacon) if validate_ip(bacon) else 'Domain',
                'name': bacon
            })

        # get the vulnerability data based on the type
        if type.lower() == 'domain':
            vulnerabilities.add(
                {
                    'name': 'is_iot_threat',
                    'risk': None if results['is_iot_threat'] else 'high'
                },
                {
                    'name': 'is_cnc',
                    'risk': None if results['is_cnc'] else 'critical'
                },
                {
                    'name': 'is_distributing_malware',
                    'risk': None if results['is_distributing_malware'] else 'critical'
                },
                {
                    'name': 'is_mining_pool',
                    'risk': None if results['is_mining_pool'] else 'medium'
                },
                {
                    'name': 'is_storing_phishing',
                    'risk': None if results['is_storing_phishing'] else 'high'
                },
                {
                    'name': 'is_phishing',
                    'risk': None if results['is_phishing'] else 'high'
                }
            )
        if type.lower() == 'ip':
            vulnerabilities.add(
                {
                    'name': 'is_cdn',
                    'risk': None if results['is_cdn'] else 'info'
                },
                {
                    'name': 'is_cnc',
                    'risk': None if results['is_cnc'] else 'critical'
                },
                {
                    'name': 'is_distributing_malware',
                    'risk': None if results['is_distributing_malware'] else 'critical'
                },
                {
                    'name': 'is_hosting',
                    'risk': None if results['is_hosting'] else 'info'
                },
                {
                    'name': 'is_known_attacker',
                    'risk': None if results['is_known_attacker'] else 'high'
                },
                {
                    'name': 'is_known_scanner',
                    'risk': None if results['is_known_scanner'] else 'medium'
                },
                {
                    'name': 'is_mining_pool',
                    'risk': None if results['is_mining_pool'] else 'medium'
                },
                {
                    'name': 'is_scanner',
                    'risk': None if results['is_scanner'] else 'medium'
                },
                {
                    'name': 'is_open_proxy',
                    'risk': None if results['is_open_proxy'] else 'medium'
                },
                {
                    'name': 'is_sinkhole',
                    'risk': None if results['is_sinkhole'] else 'low'
                },
                {
                    'name': 'is_tor_node',
                    'risk': None if results['is_tor_node'] else 'medium'
                },
                {
                    'name': 'is_vpn_node',
                    'risk': None if results['is_vpn_node'] else 'medium'
                },
            )

    else:
        errors = [
            f'There is an error in getting the data from Maltiverse',
            '',
            f'{results["message"]}',
            '',
            ''
        ]
        print_error(True, errors)

    # return gathered data
    return [
        blocked_list,
        vulnerabilities
    ]
 