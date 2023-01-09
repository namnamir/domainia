#!/usr/bin/env python


"""
    ### Subdomain: Hacker Target API

    This function gets the list of subdomains and corresponding IPs by calling 
    the Hacker Target API.

    # Input:  - a single domain name
    # Output: - a dictionary contains SSL certificate details
"""


from colorama import Fore, Style

from config import config
from modules.utils import run_requests, printer
from modules.subdomain.utils import alt_name_sanitizer


def hacker_target(domain):
    # variables to store subdomains and related domains
    subdomains = set()
    related_domains = set()

    # print the subtitle: Hacker Target
    printer('      │        ├□ ' + Fore.GREEN + 
            'Hacker Target API is calling' + Style.RESET_ALL)

    # download the result page of Hacker Target
    url = config['api']['hacker_target']['url_hosts'].format(domain)
    results = run_requests('GET', url, '', '', '', 'text', 'Hacker Target API')[0]
    results = results.split('\n')

    # get subdomains and related domains out from the output of the API call
    if results:
        subdomains, related_domains = alt_name_sanitizer(results, domain)

    # return subdomain and related domain
    return [
        subdomains,
        related_domains
    ]
