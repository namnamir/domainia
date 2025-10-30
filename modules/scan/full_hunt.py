#!/usr/bin/env python


"""
    ### Vulnerability Scanner: Full Hunt API

    This function checks if there is any information about the given domain name,
    including DNS records, open ports, ect.

    Read more: https://api-docs.fullhunt.io/

    # Input:  - a single domain name
    # Output: - a set of dictionaries contains blocked lists
"""


from config import config
from modules.utils import url_opener, error_printer


def full_hunt(domain):
    # variables to store results
    port_status = set()
    vulnerabilities = set()

    # the HTTP headers to be sent to Full Hunt
    headers = {'X-API-KEY': config['api']['full_hunt']['api_key']}

    # form the URL based on the type of the domain
    url = config['api']['full_hunt']['url_domain'].format(domain)

    # get the results in JSON from Full Hunt
    results = url_opener('GET', url, '', '', headers, 'json', 'Full Hunt API')[0]

    # if the API call returns data
    if not 'status' in results:
        # get the blocked lists
        results = results['data']['hosts']

        # add the port to the set
        for port in results['network_ports']:
            port_status.add(
                {
                    'port': port,
                    'status': 'Open',
                    'protocol': '',
                    'service': '',
                }
            )
        vulnerabilities.add(
            {
                'name': 'is_cdn',
                'risk': None if results['is_cdn'] else 'info'
            },
            {
                'name': 'is_cloud',
                'risk': None if results['is_cloud'] else 'info'
            },
            {
                'name': 'is_cloudflare',
                'risk': None if results['is_cloudflare'] else 'info'
            },
            {
                'name': 'is_resolvable',
                'risk': None if results['is_resolvable'] else 'info'
            }
        )

    else:
        texts = [
            f'There was an error in getting data from Full Hunt',
            '',
            f'Code: {results["status"]} ➜ {results["message"]}'
        ]
        error_printer(True, texts)

    # return gathered data
    return [
        vulnerabilities,
        port_status
    ]
