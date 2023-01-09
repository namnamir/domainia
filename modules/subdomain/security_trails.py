#!/usr/bin/env python


"""
    ### Vulnerability Scanner: Security Trails API

    This function gets the list of subdomains found by Security Trails.

    Read more: https://docs.securitytrails.com/reference/domain-subdomains

    # Input:  - a single domain name
    # Output: - a set of dictionaries contains blocked lists
"""


from datetime import datetime

from config import config
from modules.utils import run_requests, print_error, date_formatter
from modules.subdomain.utils import sub_related_domains


def security_trails(domain):
    # variables to store results
    alt_names = set()
    subdomains = set()
    related_domains = set()

    # the HTTP headers to be sent to Security Trails
    headers = {
        "accept": "application/json",
        "APIKEY": config['api']['security_trails']['api_key']
    }

    # form the URL
    url = config['api']['security_trails']['url_subdomain'].format(domain)

    # get the results in JSON from Security Trails
    results = run_requests('GET', url, '', '', headers, 'json', 'Security Trails API')

    # if the API call returns data
    if results[1] == 200:
        # get list of the alternative names
        for alt_name in results[0]['subdomains']:
            alt_names.add(
                {
                    'name': alt_name['indicator'],
                    'reason': 'Pulse Dive',
                    'date': date_formatter(datetime.now(), '')
                }
            )

        # call the function to extract subdomain & related-domains from 
        # the alternative names
        subdomains, related_domains = sub_related_domains(alt_names, domain)

    else:
        texts = [
            f'There was an error in getting data from Security Trails',
            '',
            f'Code: {results[1]} ➜ {results[0]["message"]}'
        ]
        print_error(True, texts)

    # return gathered data
    return [
        subdomains,
        related_domains
    ]
 