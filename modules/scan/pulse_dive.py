#!/usr/bin/env python


"""
    ### Vulnerability Scanner: Pulse Dive

    This function gets the scan results from Pulse Dive.

    # Input:  - a single domain name
    # Output: - a dictionary contains the domain
"""


from datetime import datetime
from time import sleep

from config import config
from modules.utils import url_opener, date_formatter
from modules.subdomain.utils import sub_related_domains


def pulse_dive(domain):
    # variables to store results
    vulnerabilities = set()
    port_status = set()
    technologies = set()
    http_headers = set()
    html_meta = set()
    alt_names = set()
    related_domains = set()
    subdomains = set()

    # get the scan type (active or passive) and the delay
    scan_type = 1 if config['api']['pulse_dive']['scan_type'].lower() == 'active' else 0
    delay = config['api']['pulse_dive']['delay']
    date_format = config['api']['pulse_dive']['date_format']

    # form the data to be sent to the API (start the scan)
    data = {
        "value": domain,
        "probe": scan_type,
        "pretty": "0",
        "key": config['api']['pulse_dive']['api_key']
    }

    # send the scan request to Pulse Dive and get the scan ID
    url = config['api']['pulse_dive']['url_scan']
    results = url_opener('POST', url, '', data, '', 'json', 'Pulse Dive')
    scan_id = results[0]['qid']

    url = config['api']['pulse_dive']['url_result'].format(
        scan_id,
        config['api']['pulse_dive']['api_key']
    )

    # check if result is ready
    while True:
        # send the HTTP request to scan
        results = url_opener('GET', url, '', '', '', 'json', 'Pulse Dive')[0]

        # if the doesn't exist, the report exits
        if results['status'] == 'done':
            break
        else:
            # sleep for a certain time to finish the scan
            sleep(delay)

    # get the results
    results = results['data']

    # get the list of vulnerabilities
    for risk_factor in results['riskfactors']:
        # define the risk level
        if risk_factor['riskfactors']['risk'] in ('none', 'unknown'):
            risk = 'info'
        else:
            risk_factor['riskfactors']['risk']
        # add the results to vulnerabilities
        vulnerabilities.add(
                {
                    'name': risk_factor['description'],
                    'risk': risk
                }
        )

    # get the list of open ports
    for port in results['attributes']['port']:
        port_status.add(
            {
                'port': port,
                'status': 'open',
                'protocol': '',
                'service': '',
            }
        )

    # get the list of technologies
    for tech in results['attributes']['technology']:
        technologies.add(
            {
                'name': tech,
                'version': '',
                'category': '',
                'date': date_formatter(results['stamp_updated'], date_format)
            }
        )

    # get the list of HTTP headers
    for name, value in results['properties']['http'].items():
        # ignore the illegal headers
        if name.startswith('++'):
            continue
        # add the HTTP header to the list
        http_headers.add(
            {
                'name': name.lower(),
                'value': value,
            }
        )

    # get the list of HTML meta data
    for name, value in results['properties']['meta'].items():
        html_meta.add(
            {
                'name': name.lower(),
                'value': value,
            }
        )

    # get list of the alternative names
    for alt_name in results['links']['Related Domains']:
        alt_names.add(
            {
                'name': alt_name['indicator'],
                'reason': 'Pulse Dive',
                'date': date_formatter(alt_name['stamp_linked'], date_format)
            }
        )

    # call the function to extract subdomain & related-domains from
    # the alternative names
    subdomains, related_domains = sub_related_domains(alt_names, domain)

    # return gathered data
    return [
        {
            "name": domain,
            "technologies" : technologies,
            "ports": port_status,
            "vulnerabilities": vulnerabilities,
            "http_headers": http_headers,
            "http_meta": html_meta,
            "subdomains": subdomains,
            "related_domains": related_domains
        }
    ]
