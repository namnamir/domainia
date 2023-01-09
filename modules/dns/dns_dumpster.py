#!/usr/bin/env python


"""
    ### DNS Checker: DNS Dumpster

    This function gets the value of DNS records provided by DNS Dumpster including 
    MX, NS, TXT records as well as subdomain.
    
    # Input:  - a single domain name
    # Output: - a set of dictionaries contains a single DNS record details
              - a set contains list of subdomains
              - a set contains list of related domains
"""

from bs4 import BeautifulSoup
from datetime import datetime

from config import config
from modules.subdomain.utils import sub_related_domains
from modules.utils import run_requests, print_error


def dns_dumpster(domain):
    # some variables to store data
    dns_records = set()
    alt_names = set()
    subdomains = set()
    related_domains = set()

    # get the API url from the config file
    url = config['api']['dns_dumpster']['url']

    # get the CSRF from the page
    result = run_requests('GET', url, '', '', '', 'text', 'DNS Dumpster')[0]
    soup = BeautifulSoup(result.content, 'html.parser')
    csrf = soup.findAll('input', attrs={'name': 'csrfmiddlewaretoken'})[0]['value']

    # set a POST request to get the results
    cookies = {'csrftoken': csrf}
    headers = {'Referer': url}
    data = {'csrfmiddlewaretoken': csrf, 'targetip': domain, 'user': 'free'}
    post_request = run_requests('POST', url, cookies, data, headers, 'text', 'DNS Dumpster')

    # go further only if the POST request was successful
    if post_request.status_code == 200:
        # get all tables from the page
        tables = BeautifulSoup(post_request.content, 'html.parser').findAll('table')

        # iterate over NS rows
        for row in tables[0].findAll('tr'):
            columns = row.findAll('td')
            dns_records.add(
                {
                    'record': 'NS',
                    'value': str(columns[0]).split('<br/>')[0].split('>')[1].split('<')[0]
                }
            )
        # iterate over MX rows
        for row in tables[1].findAll('tr'):
            columns = row.findAll('td')
            dns_records.add(
                {
                    'record': 'MX',
                    'value': str(columns[0]).split('<br/>')[0].split('>')[1].split('<')[0]
                }
            )
        # iterate over A rows
        for row in tables[3].findAll('tr'):
            columns = row.findAll('td')
            dns_records.add(
                {
                    'record': 'A',
                    'value': str(columns[1]).split('<br/>')[0].split('>')[1].split('<')[0]
                }
            )
            alt_names.add(
                str(columns[0]).split('<br/>')[0].split('>')[1].split('<')[0]
            )
        # iterate over TXT rows
        for column in tables[2].findAll('td'):
            dns_records.add(
                {
                    'record': 'TXT',
                    'value': column.text
                }
            )

        # form the domain info list
        domain_info = [
            domain,
            'DNS Dumpster',
            datetime.now(),
            ''
        ]
        # call the function to define if the alt name is a subdomain or not
        subdomains, related_domains = sub_related_domains(alt_names, domain_info)
    
    # if there was an error with getting info
    else:
        texts = [
            f'Open the DSN Dumpster faced an issue.',
            '',
            f'The error code is: {post_request.status_code}'
        ]
        print_error(True, texts)

    # return gathered data
    return [
        dns_records,
        subdomains,
        related_domains
    ]
