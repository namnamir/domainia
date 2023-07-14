#!/usr/bin/env python


"""
    ### Whois: WhoisXML API

    This function gets the whois of the given domain.

    # Input:  - a single domain name
    # Output: - a dictionary contains robots.txt details
              - a list of name servers (NS)
"""

from datetime import datetime
from colorama import Fore, Style

from config import config
from modules.utils import url_opener, printer, date_formatter, json_key_checker


def whois_xml(domain):
    # a variable to store results
    domain_whois = dict()
    name_servers = list()

    # check if the whois API key is set
    if config['api']['WhoisXML']['api_key'] == '':
        printer('      │      ■ ' + Fore.RED + 'WhoisXML API key is not defined. Do it in the "config.py" file.' + Style.RESET_ALL)
        return domain_whois
    else:
        # get the date format of the WhoisXML from the config file
        date_format = config['api']['whois_xml']['date_format']

        # call the API
        url = config['api']['whois_xml']['url_whois'].format(config['api']['WhoisXML']['api_key'], domain)
        results = url_opener('GET', url, '', '', '', 'json', 'WhoisXML API')[0]['WhoisRecord']

        # convert string dates to the object date and format it accordingly
        # only if there is any data
        if results:
            domain_whois['validity']['create_date'] = date_formatter(json_key_checker(results, ['create_date', '']), date_format)
            domain_whois['validity']['update_date'] = date_formatter(json_key_checker(results, ['update_date', '']), date_format)
            domain_whois['validity']['expiration_date'] = date_formatter(json_key_checker(results, ['expiry_date', '']), date_format)
            domain_whois['validity']['age'] = (datetime.strptime(domain_whois['validity']['expiration_date'], config['date_format']) - datetime.strptime(domain_whois['validity']['create_date'], config['date_format'])).days
            domain_whois['validity']['past_days'] = (datetime.now() - datetime.strptime(domain_whois['validity']['create_date'], config['date_format'])).days
            domain_whois['validity']['left_days'] = (datetime.strptime(domain_whois['validity']['expiration_date'], config['date_format']) - datetime.now()).days

            domain_whois['registrar']['name'] = json_key_checker(results, ['registrarName', ''])
            domain_whois['registrar']['iana_id'] = json_key_checker(results, ['registrarIANAID', ''])
            domain_whois['registrar']['whois_server'] = json_key_checker(results, ['whoisServer', ''])

            domain_whois['registrant']['company'] = json_key_checker(results, ['registrant', 'organization'])
            domain_whois['registrant']['country'] = json_key_checker(results, ['registrant', 'country'])
            domain_whois['registrant']['state'] = json_key_checker(results, ['registrant', 'state'])

            domain_whois['administrative']['company'] = json_key_checker(results, ['administrativeContact', 'organization'])
            domain_whois['administrative']['country'] = json_key_checker(results, ['administrativeContact', 'country'])
            domain_whois['administrative']['state'] = json_key_checker(results, ['administrativeContact', 'state'])

            domain_whois['technical']['company'] = json_key_checker(results, ['technicalContact', 'organization'])
            domain_whois['technical']['country'] = json_key_checker(results, ['technicalContact', 'country'])
            domain_whois['technical']['state'] = json_key_checker(results, ['technicalContact', 'state'])

            domain_whois['billing']['company'] = json_key_checker(results, ['billing_contact', 'organization'])
            domain_whois['billing']['country'] = json_key_checker(results, ['billing_contact', 'country'])
            domain_whois['billing']['state'] = json_key_checker(results, ['billing_contact', 'state'])

            name_servers = json_key_checker(results, ['nameServers', 'hostNames'])

        return [
            domain_whois,
            name_servers
        ]
