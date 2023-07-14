#!/usr/bin/env python


"""
    ### Vulnerability Scanner: Rapid DNS

    This function gets the list of historical DNS records and the reverse DNS of
    the given IP address or domain name.
    It contains duplicated subdomains and related domains as the date or the
    reason might be different.

    # Input:  - a single domain name or IP address
    # Output: - a set of dictionaries contains technologies used in the bacon
"""


from bs4 import BeautifulSoup

from config import config
from modules.subdomain.utils import alt_name_sanitizer
from modules.utils import url_opener, date_formatter


def rapid_dns(bacon, type):
    # variables to store results
    alt_names = set()
    subdomains = set()
    related_domains = set()
    dns_records = set()

    # get the date format of the Rapid DNS from the config file
    date_format = config['api']['rapid_dns']['date_format']

    # get the results
    url = config['api']['rapid_dns']['url'].format(bacon)
    results = url_opener('GET', url, '', '', '', 'text', 'Rapid DNS')

    # find the table contains results using Beautiful Soup
    results = BeautifulSoup(results, 'html.parser')
    results = results.find(
        "table", {"class": "table table-striped table-bordered"}
    )
    results = results.find_all('tr')

    # parse the table and get the DNS data out of it
    for row in results:
        # add the found technology into the set
        row = row.find_all('td')

        if type.lower() == 'ip':
            related_domains.add(
                {
                    'value': row[0].text.strip(),
                    # why it is a related domain
                    'reason': row[2].text.strip(),
                    # the date that the relationship is found
                    'date': date_formatter(row[3].text.strip(), date_format)
                }
            )
        else:
            subdomains.add(
                {
                    'value': row[2].text.strip().split('.' + bacon)[0],
                    'reason': row[2].text.strip(),
                    'date': date_formatter(row[3].text.strip(), date_format)
                }
            )

    # return gathered data
    return [
        dns_records
    ]
