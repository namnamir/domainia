#!/usr/bin/env python


"""
    ### Vulnerability Scanner: Criminal IP API

    This function gets the list of subdomains and corresponding IPs by calling 
    the Criminal IP API.

    Read more: - https://www.criminalip.io/developer/api/

    # Input:  - a single domain name or IP address
              - the type of the asset that needs to be assessed
    # Output: - a set contains vulnerability assessment of the given domain
              - a set contains technologies used by the given domain
              - a set contains subdomains
              - a set contains related domains
              - a dictionary contains some details about the IP
"""


from colorama import Fore, Style

from config import config
from modules.utils import run_requests, printer, print_error
from modules.subdomain.utils import alt_name_sanitizer


def criminal_ip(bacon, type):
    # variables to store subdomains and related domains
    vulnerabilities = set()
    technologies = set()
    subdomains = set()
    related_domains = set()
    ip_data = dict()
    ip_data['vulnerabilities'] = set()
    ip_data['ports'] = set()

    # print the subtitle: Criminal IP
    printer('      │        ├□ ' + Fore.GREEN + 'Criminal IP API is calling' + Style.RESET_ALL)

    # for the HTTP headers to send to Criminal IP
    headers = {'x-api-key': config['api']['criminal_ip']['api_key']}

    # get the results in JSON from Criminal IP
    if type == 'domain':
        url = config['api']['criminal_ip']['url_domain'].format(bacon)
        results = run_requests('GET', url, '', '', headers, 'json', 'Criminal IP API')[0]
        
        # if the API call returns data
        if results['status'] == 200:
            # get the latest report ID
            report_id = results['data']['reports'][0]['scan_id']

            url = config['api']['criminal_ip']['url_domain_report'].format(report_id)
            report = run_requests('GET', url, '', '', headers, 'json', 'Criminal IP API')[0]

            # if the API call returns data
            if report['status'] == 200:
                # get the list of subdomains and related domains
                for subdomain in report['data']['subdomains']:
                    subdomains.add(subdomain['subdomain_name'])
                
                subdomains, related_domains = alt_name_sanitizer(subdomains, bacon)
                
                # get the vulnerability data
                summary = summary
                vulnerabilities.add(
                    {
                        'name': 'connect_to_ip_directly',
                        'risk': None if summary['connect_to_ip_directly'] else 'info'
                    },
                    {
                        'name': 'diff_domain_favicon',
                        'risk': None if summary['diff_domain_favicon'] else 'low'
                    },
                    {
                        'name': 'double_slash_url',
                        'risk': None if summary['double_slash_url'] else 'info'
                    },
                    {
                        'name': 'fake_domain',
                        'risk': None if summary['fake_domain'] else 'medium'
                    },
                    {
                        'name': 'fake_https_url',
                        'risk': None if summary['fake_https_url'] else 'high'
                    },
                    {
                        'name': 'fake_ssl',
                        'risk': None if summary['fake_ssl']['invalid'] else 'high'
                    },
                    {
                        'name': 'hidden_element',
                        'risk': None if summary['hidden_element'] else 'low'
                    },
                    {
                        'name': 'hidden_iframe',
                        'risk': None if summary['hidden_iframe'] else 'medium'
                    },
                    {
                        'name': 'js_obfuscated',
                        'risk': None if summary['js_obfuscated'] else 'low'
                    },
                    {
                        'name': 'mail_server',
                        'risk': None if summary['mail_server'] else 'info'
                    },
                    {
                        'name': 'many_subdomain',
                        'risk': None if summary['many_subdomain'] else 'low'
                    },
                    {
                        'name': 'mitm_attack',
                        'risk': None if summary['mitm_attack'] else 'critical'
                    },
                    {
                        'name': 'newborn_domain',
                        'risk': None if summary['newborn_domain'] else 'low'
                    },
                    {
                        'name': 'punycode',
                        'risk': None if summary['punycode'] else 'low'
                    },
                    {
                        'name': 'suspicious_cookie',
                        'risk': None if summary['suspicious_cookie'] else 'low'
                    }
                )
                
                # get the list of subdomains and related domains
                for tech in report['data']['technologies']:
                    technologies.add(
                        {
                            'name': tech['name'],
                            'version': tech['version'],
                            'date': ''
                        }
                    )


    elif type == 'ip':
        url = config['api']['criminal_ip']['url_ip'].format(bacon)
        results = run_requests('GET', url, '', '', '', 'json', 'Criminal IP API')[0]

        # if the API call returns data
        if results['status'] == 200:
            ip_data['vulnerabilities'].add(
                {
                    'name': 'is_mobile',
                    'risk': None if results['is_mobile'] else 'info'
                },
                {
                    'name': 'is_hosting',
                    'risk': None if results['is_hosting'] else 'info'
                },
                {
                    'name': 'is_proxy',
                    'risk': None if results['is_proxy'] else 'medium'
                },
                {
                    'name': 'is_cloud',
                    'risk': None if results['is_cloud'] else 'info'
                },
                {
                    'name': 'is_tor',
                    'risk': None if results['is_tor'] else 'medium'
                },
                {
                    'name': 'is_vpn',
                    'risk': None if results['is_vpn'] else 'medium'
                },
                {
                    'name': 'is_darkweb',
                    'risk': None if results['is_darkweb'] else 'medium'
                },
                {
                    'name': 'is_scanner',
                    'risk': None if results['is_scanner'] else 'medium'
                },
                {
                    'name': 'is_snort',
                    'risk': None if results['is_snort'] else 'info'
                }
            )

            # iterate over ports found by Criminal IP
            for port in range (0, results['port']['count'] - 1):
                ip_data['ports'].add(
                    {
                        'port': port['open_port_no'],
                        'status': port['port_status'],
                        'protocol': port['socket'],
                        'service': port['protocol'],
                    }
                )
    else:
        errors = [f'Criminal IP API does not support "{type}".']
        print_error(True, errors)

    # return gathered data
    return [
        ip_data,
        subdomains,
        related_domains,
        technologies,
        vulnerabilities
    ]
 