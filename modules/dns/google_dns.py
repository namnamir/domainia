#!/usr/bin/env python

from colorama import Fore, Style

from config import config
from modules.utilities.url_opener import url_opener
from modules.dns.utils import dns_record_type, rr_record_finder
from modules.utilities.printer import printer


def google_dns(domain, key, record):
    """
        ### DNS: Google DNS API

        This function gets DNS records from Google DNS API.

        Read more: - https://developers.google.com/speed/public-dns/docs/doh/json
                - https://en.wikipedia.org/wiki/List_of_DNS_record_types

        # Input:  - a single domain name
                - the key, subdomain, or selector.subdomain
                - a single DNS record either in an RR type (int) or case-insensitive string; e.g. 1 or A or a
        # Output: - a set of dictionaries contains a single DNS record details
    """
    # A set to store results
    results = set()

    # Get the RR type of the DNS record
    rr_record = rr_record_finder(record)

    # Download the JSON response
    url = config['api']['google_dns']['url'].format(domain, record)
    printer('      │        ├□ ' + Fore.GREEN + 'Google DNS is downloading' + Style.RESET_ALL)
    answers = url_opener('GET', url, '', '', '', 'json', 'Google DNS API')[0]

    # Check if there is any error in the API call
    # 0 means no error
    if answers['Status'] != 0:
        printer('      │        ├■ ' + Fore.RED + f'There was an error in the API call {url}' + Style.RESET_ALL)
        return results

    # Iterate over the lines in the Google DNS API
    for answer in answers['Answer']:
        if answer['type'] != rr_record:
            printer('      │        ├■ ' + Fore.RED +
                    f'The API call {url} returned "{answer["type"]}" record instead of "{rr_record}".' +
                    Style.RESET_ALL)
            continue
        else:
            results.add({
                'record': record,
                'type': dns_record_type(rr_record, key, answer),
                'key': key,
                'value': answer['data']
            })

    return results
