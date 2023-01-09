#!/usr/bin/env python


"""
    ### Vulnerability Scanner: Geek Flare

    This function checks if the given domain supports different versions of HTTP, 
    including ver. 1.0, ver. 1.1, ver. 2.0, and ver. 3.0.

    # Input:  - a single domain name
    # Output: - a set of dictionaries contains HTTP headers
"""


from config import config
from modules.utils import run_requests, print_error


def geek_flare_broken_link(domain):
    # a variable to store results
    versions = dict()

    data = {
        "url": domain,
        "followRedirect": True
    }
    headers = {
        'x-api-key': config['api']['geek_flare']['api_key'],
        'Content-Type': 'application/json'
    }

    # check if report exist
    url = config['api']['geek_flare']['url_http_protocol']
    results = run_requests('POST', url, '', data, headers, 'json', 'Geek Flare')

    # check if there is any error
    if results['apiCode'] != 200:
        # add the found versions to the dictionary
        versions = results['data']

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
    return versions
