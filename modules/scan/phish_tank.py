#!/usr/bin/env python


"""
    ### Vulnerability Scanner: Phish Tank

    This function checks if the domain is listed by Phish Tank or not

    # Input:  - a single domain name
    # Output: - a set of dictionaries contains results if listed
"""


from config import config
from modules.utils import url_opener, error_printer


def phish_tank(domain):
    # variables to store results
    blocked_list = set()

    url = config['api']['phish_tank']['url']

    # different basic formats to send to Phish Tank
    # it is needed as Phish Tank doesn't support the wildcard search
    formats = [
        'http://' + domain, 'https://' + domain,
        'http://' + domain + '/', 'https://' + domain + '/'
    ]

    # iterate over different formats
    for uri in formats:
        data = {'url': uri, 'format': 'json'}
        results = url_opener(
            'POST', url, '', data, '', 'text', 'Phish Tank'
        )[0]

        # if there is no issue
        if results['meta']['status'] == 'success':
            # if the URL is listed in Phish Tank
            if results['results']['in_database']:
                blocked_list.add(
                    {
                        'by': 'Phish Tank',
                        'reason': 'Phishing',
                        'type': 'Domain',
                        'name': domain
                    }
                )
        # if there was an error with getting info
        else:
            texts = [
                f'There is an issue in getting data from Phish Tank.',
                '',
                f'The error is: {results["errortext"]}'
            ]
            error_printer(True, texts)

# return gathered data
    return blocked_list
