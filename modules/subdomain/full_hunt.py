#!/usr/bin/env python


"""
    ### Vulnerability Scanner: Full Hunt API

    This function returns all the subdomains found by Full Hunt.

    Read more: https://api-docs.fullhunt.io/

    # Input:  - a single domain name
    # Output: - a set of dictionaries contains the alternative domains
"""


from datetime import datetime

from config import config
from modules.utils import run_requests, print_error, date_formatter
from modules.subdomain.utils import sub_related_domains



def full_hunt(domain):
    # variables to store results
    alt_names = set()

    # the HTTP headers to be sent to Full Hunt
    headers = {'X-API-KEY': config['api']['full_hunt']['api_key']}

    # form the URL based on the type of the domain
    url = config['api']['full_hunt']['url_subdomain'].format(domain)

    # get the results in JSON from Full Hunt
    results = run_requests('GET', url, '', '', headers, 'json', 'Full Hunt API')[0]

    # if the API call returns data
    if results['status'] == 200:
        # get the date in epoch format
        date = ['data']['metadata']['last_scanned']
        date = datetime.fromtimestamp(date)  

        # get list of the alternative names
        for alt_name in results['subdomains']:
            alt_names.add(
                {
                    'name': alt_name,
                    'reason': 'Full Hunt',
                    'date': date_formatter(date, '')
                }
            )

        # call the function to extract subdomain & related-domains from 
        # the alternative names
        subdomains, related_domains = sub_related_domains(alt_names, domain)
    else:
        texts = [
            f'There was an error in getting data from Full Hunt',
            '',
            f'Code: {results["status"]} ➜ {results["message"]}'
        ]
        print_error(True, texts)

    # return gathered data
    return [
        subdomains,
        related_domains
    ]
 