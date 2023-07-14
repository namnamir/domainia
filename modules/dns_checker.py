#!/usr/bin/env python


"""
    ### DNS Checker

    This function is responsible for getting SSL certificate details through
    different methods. Therefore, it will print the summary results on STDOUT.

    # Input:  - a single domain name
    # Output: - a dictionary contains SSL certificate details
"""


from colorama import Fore, Back, Style
from time import sleep

from config import config
from modules.dns.dns_dig import dns_dig
from modules.dns.google_dns import google_dns
from modules.dns.dns_spy import dns_spy
from modules.dns.dnssec import dnssec
from modules.whois.ip_api import validate_ip, ip_lookup
from modules.utilities.printer import printer

# resolve the DNS and get all the defined records
def dns_checker(domain):
    # a dictionary to store data
    dns_records = dict()
    # get the list of desired DNS records; remove duplicates and sort it
    dns_records_list = sorted(set(config['dns']['dns_records']))

    # print the title of the section
    printer('      │\n      ├───' + Fore.BLACK + Back.WHITE + ' DNS Records ' + Style.RESET_ALL)

    # get data from DNS Spy or return an empty dict
    printer('      │        └□ ' + Fore.GREEN + 'DNS Spy API is calling' + Style.RESET_ALL)
    records, subdomains = dns_spy(domain)

    # iterate over DNS records and resolve them
    for record in dns_records_list:
        # a list to store data
        dns_records[record] = list()

        # load data from built-in python module
        answers = dns_dig(domain, '', record)
        # update it by adding data from Google DNS API
        answers.update(google_dns(domain, '', record))

        # if it is a TXT record
        if record == 'TXT':
            # iterate over the list of subdomains given in the config.py file
            # it can be a brute-force to find more
            for subdomain in sorted(set(config['dns']['txt_records_helper'])):
                # update data from built-in python module for subdomains
                answers.update(dns_dig(subdomain + domain, subdomain, record))
                # update it by adding data from Google DNS API for subdomains
                answers.update(google_dns(subdomain + domain, subdomain, record))

        # print the title of the subsection (DNS Record Name)
        printer('      │      ' + Fore.CYAN + f'■ {record} Records       ' + Style.RESET_ALL)

        # iterate over the DNS records and print the result on STDOUT
        for answer in answers:
            i += 1

            # if it is a TXT record but not listed in the config file
            if record == 'TXT' and not any(txt.lower() in answer.lower() for txt in config['dns']['include_txt_records']):
                color = Fore.MAGENTA
            else:
                color = Fore.YELLOW

            # print the result on STDOUT
            l_start = '       │' # for printing IP lookups
            if i == len(answers):
                printer('      │      └◌ ' + color + answer['value'] + Style.RESET_ALL)
            else:
                printer('      │      ├◌ ' + color + answer + Style.RESET_ALL)

            # if the result is an IP, print the IP lookup results
            if validate_ip(answer):
                lookup = ip_lookup(answer)
                if config['verbosity'] >= 3:
                    printer(l_start + ' ' * 14 + '├□ Location:    ' + Fore.CYAN + lookup['city'] + ', ' + lookup['country'] + Style.RESET_ALL)
                    printer(l_start + ' ' * 14 + '├□ ISP Name:    ' + Fore.CYAN + lookup['isp'] + Style.RESET_ALL)
                    printer(l_start + ' ' * 14 + '├□ Org. Name:   ' + Fore.CYAN + lookup['organization'] + Style.RESET_ALL)
                    printer(l_start + ' ' * 14 + '├□ Reverse DNS: ' + Fore.CYAN + lookup['reverse_dns'] + Style.RESET_ALL)
                    printer(l_start + ' ' * 14 + '├□ Is Mobile?   ' + Fore.CYAN + lookup['mobile'] + Style.RESET_ALL)
                    printer(l_start + ' ' * 14 + '├□ Is Proxy?    ' + Fore.CYAN + lookup['proxy'] + Style.RESET_ALL)
                    printer(l_start + ' ' * 14 + '└□ Is Hosting?  ' + Fore.CYAN + lookup['hosting'] + Style.RESET_ALL)

        # add a delay between DNS queries
        sleep(config['delay']['dns'])

    # return the list of the DNS records
    return dns_records
