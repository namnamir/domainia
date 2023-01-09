#!/usr/bin/env python


"""
    ### Vulnerability Scanner: Virus Total API

    This function checks if the domain name or the IP address is listed in any 
    engines listed by Virus Total.

    Read more: https://developers.virustotal.com/reference

    # Input:  - a single domain name or IP address
    # Output: - a set of dictionaries contains blocked lists
"""


from datetime import datetime

from config import config
from modules.utils import run_requests, print_error, date_formatter


def virus_total(bacon):
    # variables to store results
    blocked_list = set()

    # the HTTP headers to be sent to Virus Total
    headers = {'x-apikey': config['api']['virus_total']['api_key']}

    # form the URL based on the type of the bacon
    if type.lower() == 'ip':
        url = config['api']['virus_total']['url_ip'].format(bacon)
    if type.lower() == 'domain':
        url = config['api']['virus_total']['url_domain'].format(bacon)

    # get the results in JSON from Virus Total
    results = run_requests('GET', url, '', '', headers, 'json', 'Virus Total API')[0]

    # if the API call returns data
    if not 'error' in results:
        # get the date in epoch format
        date = ['data']['attributes']['last_analysis_date']
        date = datetime.fromtimestamp(date)  

        # get the blocked lists
        results = results['data']['attributes']['last_analysis_results']

        # iterate over the results
        for result in results:
            if results['result'] in ('clean', 'unrated'):
                continue
            blocked_list.add(
                {
                    'by': result['engine_name'],
                    'reason': result['category'],
                    'type': 'IPv4',
                    'name': bacon,
                    'date': date_formatter(date , '')
                }
            )

    else:
        texts = [
            f'There was an error in getting data from Virus Total',
            '',
            f'Code: {results["code"]} ➜ {results["message"]}'
        ]
        print_error(True, texts)

    # return gathered data
    return blocked_list
 