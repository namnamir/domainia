#!/usr/bin/env python


"""
    ### Whois: Whoxy API

    This function gets the whois of the given domain.

    # Input:  - a single domain name
    # Output: - a dictionary contains robots.txt details
              - a list of name servers (NS)
"""

from datetime import datetime
from colorama import Fore, Style

from config import config
from modules.utils import url_opener, printer, date_formatter, json_key_checker


def whoxy(domain):
    # a variable to store results
    domain_whois = dict()
    name_servers = list()

    # check if the whois API key is set
    if config['api']['whoxy']['api_key'] == '':
        printer('      │      ■ ' + Fore.RED + 'Whoxy API key is not defined. Do it in the "config.py" file.' + Style.RESET_ALL)
        return domain_whois
    else:
        # get the date format of the Whoxy from the config file
        date_format = config['api']['whoxy']['date_format']

        # call the API
        url = config['api']['whoxy']['url_whois'].format(config['api']['whoxy']['api_key'], domain)
        results = url_opener('GET', url, '', '', '', 'json', 'Whoxy API')[0]

        # convert string dates to the object date and format it accordingly
        # only if there is any data
        if results:
            domain_whois['validity']['create_date'] = date_formatter(json_key_checker(results, ['create_date', '']), date_format)
            domain_whois['validity']['update_date'] = date_formatter(json_key_checker(results, ['update_date', '']), date_format)
            domain_whois['validity']['expiration_date'] = date_formatter(json_key_checker(results, ['expiry_date', '']), date_format)
            domain_whois['validity']['age'] = (datetime.strptime(domain_whois['validity']['expiration_date'], config['date_format']) - datetime.strptime(domain_whois['validity']['create_date'], config['date_format'])).days
            domain_whois['validity']['past_days'] = (datetime.now() - datetime.strptime(domain_whois['validity']['create_date'], config['date_format'])).days
            domain_whois['validity']['left_days'] = (datetime.strptime(domain_whois['validity']['expiration_date'], config['date_format']) - datetime.now()).days

            domain_whois['registrar']['name'] = json_key_checker(results, ['domain_registrar', 'registrar_name'])
            domain_whois['registrar']['iana_id'] = json_key_checker(results, ['domain_registrar', 'iana_id'])
            domain_whois['registrar']['website'] = json_key_checker(results, ['domain_registrar', 'website_url'])
            domain_whois['registrar']['whois_server'] = json_key_checker(results, ['domain_registrar', 'whois_server'])
            domain_whois['registrar']['email'] = json_key_checker(results, ['domain_registrar', 'email_address'])
            domain_whois['registrar']['phone'] = json_key_checker(results, ['domain_registrar', 'phone_number'])

            domain_whois['registrant']['name'] = json_key_checker(results, ['registrant_contact', 'full_name'])
            domain_whois['registrant']['company'] = json_key_checker(results, ['registrant_contact', 'company_name'])
            domain_whois['registrant']['country'] = json_key_checker(results, ['registrant_contact', 'country_name'])
            domain_whois['registrant']['state'] = json_key_checker(results, ['registrant_contact', 'state_name'])
            domain_whois['registrant']['city'] = json_key_checker(results, ['registrant_contact', 'city_name'])
            domain_whois['registrant']['zip_code'] = json_key_checker(results, ['registrant_contact', 'zip_code'])
            domain_whois['registrant']['address'] = json_key_checker(results, ['registrant_contact', 'mailing_address'])
            domain_whois['registrant']['email'] = json_key_checker(results, ['registrant_contact', 'email_address'])
            domain_whois['registrant']['phone'] = json_key_checker(results, ['registrant_contact', 'phone_number'])

            domain_whois['administrative']['name'] = json_key_checker(results, ['administrative_contact', 'full_name'])
            domain_whois['administrative']['company'] = json_key_checker(results, ['administrative_contact', 'company_name'])
            domain_whois['administrative']['country'] = json_key_checker(results, ['administrative_contact', 'country_name'])
            domain_whois['administrative']['state'] = json_key_checker(results, ['administrative_contact', 'state_name'])
            domain_whois['administrative']['city'] = json_key_checker(results, ['administrative_contact', 'city_name'])
            domain_whois['administrative']['zip_code'] = json_key_checker(results, ['administrative_contact', 'zip_code'])
            domain_whois['administrative']['address'] = json_key_checker(results, ['administrative_contact', 'mailing_address'])
            domain_whois['administrative']['email'] = json_key_checker(results, ['administrative_contact', 'email_address'])
            domain_whois['administrative']['phone'] = json_key_checker(results, ['administrative_contact', 'phone_number'])

            domain_whois['technical']['name'] = json_key_checker(results, ['technical_contact', 'full_name'])
            domain_whois['technical']['company'] = json_key_checker(results, ['technical_contact', 'company_name'])
            domain_whois['technical']['country'] = json_key_checker(results, ['technical_contact', 'country_name'])
            domain_whois['technical']['state'] = json_key_checker(results, ['technical_contact', 'state_name'])
            domain_whois['technical']['city'] = json_key_checker(results, ['technical_contact', 'city_name'])
            domain_whois['technical']['zip_code'] = json_key_checker(results, ['technical_contact', 'zip_code'])
            domain_whois['technical']['address'] = json_key_checker(results, ['technical_contact', 'mailing_address'])
            domain_whois['technical']['email'] = json_key_checker(results, ['technical_contact', 'email_address'])
            domain_whois['technical']['phone'] = json_key_checker(results, ['technical_contact', 'phone_number'])

            domain_whois['billing']['name'] = json_key_checker(results, ['billing_contact', 'full_name'])
            domain_whois['billing']['company'] = json_key_checker(results, ['billing_contact', 'company_name'])
            domain_whois['billing']['country'] = json_key_checker(results, ['billing_contact', 'country_name'])
            domain_whois['billing']['state'] = json_key_checker(results, ['billing_contact', 'state_name'])
            domain_whois['billing']['city'] = json_key_checker(results, ['billing_contact', 'city_name'])
            domain_whois['billing']['zip_code'] = json_key_checker(results, ['billing_contact', 'zip_code'])
            domain_whois['billing']['address'] = json_key_checker(results, ['billing_contact', 'mailing_address'])
            domain_whois['billing']['email'] = json_key_checker(results, ['billing_contact', 'email_address'])
            domain_whois['billing']['phone'] = json_key_checker(results, ['billing_contact', 'phone_number'])

            name_servers = json_key_checker(results, ['nameServers', ''])

        return [
            domain_whois,
            name_servers
        ]
