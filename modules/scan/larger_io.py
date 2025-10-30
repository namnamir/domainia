#!/usr/bin/env python


"""
    ### Vulnerability Scanner: Larger.io API

    This function gets the list of the technologies (services) used in the given
    domain name.

    Read more: - https://www.larger.io/user/api

    # Input:  - a single domain name or IP address
              - the scan type which would be deep or quick
    # Output: - a set contains emails related to the given bacon
              - a set of dictionaries contains technologies used in the bacon
"""


from time import sleep

from config import config
from modules.utils import url_opener, error_printer, json_key_checker, printer


def larger_io(bacon, scan_type):
    # variables to store results
    emails = set()
    technologies = set()

    # get the type of the scan; quick or deep
    # if it is defined by STDIN, the setting from the config file will be ignored
    if scan_type == '':
        scan_type = config['scan_type']['technology']

    # get the delay defined in the config file
    delay = config['delay']['large_io']

    # sleep for a certain time as the Large.io API has limits
    sleep(delay)

    # get the results in JSON from Larger.io based on the scan type
    api_key = config['api']['larger_io']['api_key']
    if scan_type == 'deep':
        url = config['api']['larger_io']['url_slow'].format(api_key, bacon)
    else:
        url = config['api']['larger_io']['url_fast'].format(api_key, bacon)
    results = url_opener('GET', url, '', '', '', 'json', 'Larger.io API')[0]

    # if the API call returns data
    if 'status' in results and results['status'] != 'false':
        # get the list of technologies
        if 'app' in results:
            for tech in results['apps']:
                technologies.add(
                    {
                        'name': json_key_checker(tech, ['name']),
                        'version': json_key_checker(tech, ['name']),
                    }
                )

        # get the list of emails
        if 'emails' in results:
            emails = json_key_checker(tech, ['emails'])

    else:
        errors = [
            f'There is an error in getting the data from Larger.io',
            '',
            f'{results["message"]}',
            '',
            ''
        ]
        error_printer(True, errors)

    # return gathered data
    return [
        technologies,
        emails
    ]
