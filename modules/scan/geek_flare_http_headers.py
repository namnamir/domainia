#!/usr/bin/env python


"""
    ### Vulnerability Scanner: Geek Flare

    This function gets the list of HTTP headers.

    # Input:  - a single domain name
    # Output: - a set of dictionaries contains HTTP headers
"""


from config import config
from modules.utils import run_requests, print_error


def geek_flare_broken_link(domain):
    # a variable to store results
    http_headers = set()

    data = {
        "url": domain,
        "proxyCountry": config['api']['geek_flare']['proxy_country'],
        "followRedirect": True
    }
    headers = {
        'x-api-key': config['api']['geek_flare']['api_key'],
        'Content-Type': 'application/json'
    }

    # check if report exist
    url = config['api']['geek_flare']['url_http_headers']
    results = run_requests('POST', url, '', data, headers, 'json', 'Geek Flare')

    # check if there is any error
    if results['apiCode'] != 200:
        # get the list of HTTP headers
        for header in results['data']:
            # add the found header to the set
            http_headers.add(
                {
                    'name': header['name'].lower(),
                    'value': header['value'],
                }
            )

    else:
        errors = [
            f'There is an error in getting the data from Geek Flare',
            '',
            f'{results["message"]}',
            '',
            ''
        ]
        print_error(True, errors)
    
    # return gathered data
    return http_headers
