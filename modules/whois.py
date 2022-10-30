#!/usr/bin/env python

from datetime import datetime
from colorama import Fore, Back, Style
from config import config
from modules.utils import run_requests, date_formatter, json_key_checker, printer


# get the wohis of the domain form different sources
def whois(domain, api):
    # set the print arguments for the function "run_requests"
    print_args = [True, '      │      ■ ', '      │      ■■ ']
    
    # call the WhoisXML API and parse data
    def whoisxml(whois, domain):
        # check if the whois API key is set
        if config['api']['whoisxml']['api_key'] == '':
            printer('      │      ■ ' + Fore.RED + 'WhoisXML API key is not set. Do it in the "config.py" file.' + Style.RESET_ALL)
            return whois, False
        else:
            # call the API
            try:
                url = config['api']['whoisxml']['url_whois'].format(config['api']['whoisxml']['api_key'], domain)
                json_data = run_requests(url, '', 'json', 'Whoxy API', print_args)['WhoisRecord']
            except:
                return whois, True

            date_format = config['api']['whoisxml']['date_format']
            whois = {
                # convert string dates to the object date and format it accordingly
                'create_date': date_formatter(json_key_checker(json_data, 'registryData', 'createdDate'), date_format),
                'update_date': date_formatter(json_key_checker(json_data, 'registryData', 'updatedDate'), date_format),
                'expiration_date': date_formatter(json_key_checker(json_data, 'registryData', 'expiresDate'), date_format),
                'domain_age_days': (datetime.now() - datetime.strptime(json_key_checker(json_data, 'registryData', 'createdDate'), date_format)).days,
                'registrar': {
                    'name': json_key_checker(json_data, 'registrarName', ''),
                    'iana_id': json_key_checker(json_data, 'registrarIANAID', ''),
                    'website': '',
                    'whois_server': json_key_checker(json_data, 'whoisServer', ''),
                    'email': json_key_checker(json_data, 'contactEmail', ''),
                    'phone': ''
                },
                'registrant': {
                    'name': json_key_checker(json_data, 'registrant', 'organization'),
                    'country': json_key_checker(json_data, 'registrant', 'country'),
                    'email': '',
                    'phone': ''
                },
                'administrative': {
                    'name': json_key_checker(json_data, 'administrativeContact', 'organization'),
                    'country': json_key_checker(json_data, 'administrativeContact', 'country'),
                    'email': '',
                    'phone': ''
                },
                'technical': {
                    'name': json_key_checker(json_data, 'technicalContact', 'organization'),
                    'country': json_key_checker(json_data, 'technicalContact', 'country'),
                    'email': '',
                    'phone': ''
                },
                'name_servers': json_key_checker(json_data, 'nameServers', 'hostNames')
            }

            return whois, True


    # call the Whoxy API and parse data
    def whoxy(whois, domain):
        # check if the whois API key is set
        if config['api']['whoxy']['api_key'] == '':
            printer('      │      ■ ' + Fore.RED + 'Whoxy API key is not defined. Do it in the "config.py" file.' + Style.RESET_ALL)
            return whois, False
        else:
            # call the API
            try:
                url = config['api']['whoxy']['url_whois'].format(config['api']['whoxy']['api_key'], domain)
                json_data = run_requests(url, '', 'json', 'Whoxy API', print_args)
            except:
                return whois, True

            date_format = config['api']['whoxy']['date_format']
            whois = {
                # convert string dates to the object date and format it accordingly
                'create_date': date_formatter(json_key_checker(json_data, 'create_date', ''), date_format),
                'update_date': date_formatter(json_key_checker(json_data, 'update_date', ''), date_format),
                'expiration_date': date_formatter(json_key_checker(json_data, 'expiry_date', ''), date_format),
                'domain_age_days': (datetime.now() - datetime.strptime(json_key_checker(json_data, 'create_date', ''), date_format)).days,
                'registrar': {
                    'name': json_key_checker(json_data, 'domain_registrar', 'registrar_name'),
                    'iana_id': json_key_checker(json_data, 'domain_registrar', 'iana_id'),
                    'website': json_key_checker(json_data, 'domain_registrar', 'website_url'),
                    'whois_server': json_key_checker(json_data, 'domain_registrar', 'whois_server'),
                    'email': json_key_checker(json_data, 'domain_registrar', 'email_address'),
                    'phone': json_key_checker(json_data, 'domain_registrar', 'phone_number')
                },
                'registrant': {
                    'name': json_key_checker(json_data, 'registrant_contact', 'company_name'),
                    'country': json_key_checker(json_data, 'registrant_contact', 'country_name'),
                    'email': json_key_checker(json_data, 'registrant_contact', 'email_address'),
                    'phone': ''
                },
                'administrative': {
                    'name': json_key_checker(json_data, 'administrative_contact', 'company_name'),
                    'country': json_key_checker(json_data, 'administrative_contact', 'country_name'),
                    'email': json_key_checker(json_data, 'administrative_contact', 'email_address'),
                    'phone': ''
                },
                'technical': {
                    'name': json_key_checker(json_data, 'technical_contact', 'company_name'),
                    'country': json_key_checker(json_data, 'technical_contact', 'country_name'),
                    'email': json_key_checker(json_data, 'technical_contact', 'email_address'),
                    'phone': ''
                },
                'name_servers': json_key_checker(json_data, 'nameServers', '')
            }

            return whois, True


    # some variables
    i = 0
    whois = {
        'create_date': '',
        'update_date': '',
        'expiration_date': '',
        'domain_age_days': '',
        'registrar': {
            'name': '',
            'iana_id': '',
            'website': '',
            'whois_server': '',
            'email': '',
            'phone': ''
        },
        'registrant': {
            'name': '',
            'country': '',
            'email': '',
            'phone': ''
        },
        'administrative': {
            'name': '',
            'country': '',
            'email': '',
            'phone': ''
        },
        'technical': {
            'name': '',
            'country': '',
            'email': '',
            'phone': ''
        },
        'name_servers': []
    }

    # print findings
    printer('      │\n      ├───' + Fore.BLACK + Back.WHITE + ' Whois ' + Style.RESET_ALL)

    # call the asked whois API
    if api == 'whoisxml':
        whois, flag = whoisxml(whois, domain)
    elif api == 'whoxy':
        whois, flag = whoxy(whois, domain)
    else:
        printer(Fore.RED + '      │      ■ ' + Fore.RED + 'Whois API is not defined; read the help.' + Style.RESET_ALL)
        return whois    

    # print the result on STDOUT
    if flag:
        printer('      │      ■ Registration Date:      ' + Fore.YELLOW + whois['create_date'] + Style.RESET_ALL)
        printer('      │      ■ Last Modification Date: ' + Fore.YELLOW + whois['update_date'] + Style.RESET_ALL)
        printer('      │      ■ Expiration Date:        ' + Fore.YELLOW + whois['expiration_date'] + Style.RESET_ALL)
        printer('      │      ■ Domain Age:             ' + Fore.YELLOW + str(whois['domain_age_days']) + ' Days' + Style.RESET_ALL)
        if config['verbosity'] > 2:
            printer('      │      ' + Fore.CYAN + '■ Registrar Details' + Style.RESET_ALL)
            printer('      └┐      ■■  Name:                ' + Fore.YELLOW + whois['registrar']['name'] + Style.RESET_ALL)
            printer('       │      ■■  IANA ID:             ' + Fore.YELLOW + str(whois['registrar']['iana_id']) + Style.RESET_ALL)
            printer('       │      ■■  Website:             ' + Fore.YELLOW + whois['registrar']['website'] + Style.RESET_ALL)
            printer('       │      ■■  Wohis Server:        ' + Fore.YELLOW + whois['registrar']['whois_server'] + Style.RESET_ALL)
            printer('       │      ■■  Email:               ' + Fore.YELLOW + whois['registrar']['email'] + Style.RESET_ALL)
            printer('      ┌┘      ■■  Phone:               ' + Fore.YELLOW + whois['registrar']['phone'] + Style.RESET_ALL)
            printer('      │      ' + Fore.CYAN + '■ Registrant Details' + Style.RESET_ALL)
            printer('      └┐      ■■  Name:                ' + Fore.YELLOW + whois['registrant']['name'] + Style.RESET_ALL)
            printer('       │      ■■  Country:             ' + Fore.YELLOW + whois['registrant']['country'] + Style.RESET_ALL)
            printer('       │      ■■  Email:               ' + Fore.YELLOW + whois['registrant']['email'] + Style.RESET_ALL)
            printer('      ┌┘      ■■  Phone:               ' + Fore.YELLOW + whois['registrant']['phone'] + Style.RESET_ALL)
            printer('      │      ' + Fore.CYAN + '■ Administrative Details' + Style.RESET_ALL)
            printer('      └┐      ■■  Name:                ' + Fore.YELLOW + whois['administrative']['name'] + Style.RESET_ALL)
            printer('       │      ■■  Country:             ' + Fore.YELLOW + whois['administrative']['country'] + Style.RESET_ALL)
            printer('       │      ■■  Email:               ' + Fore.YELLOW + whois['administrative']['email'] + Style.RESET_ALL)
            printer('      ┌┘      ■■  Phone:               ' + Fore.YELLOW + whois['administrative']['phone'] + Style.RESET_ALL)
            printer('      │      ' + Fore.CYAN + '■ Technical Details' + Style.RESET_ALL)
            printer('      └┐      ■■  Name:                ' + Fore.YELLOW + whois['technical']['name'] + Style.RESET_ALL)
            printer('       │      ■■  Country:             ' + Fore.YELLOW + whois['technical']['country'] + Style.RESET_ALL)
            printer('       │      ■■  Email:               ' + Fore.YELLOW + whois['technical']['email'] + Style.RESET_ALL)
            printer('      ┌┘      ■■  Phone:               ' + Fore.YELLOW + whois['technical']['phone'] + Style.RESET_ALL)
        if config['verbosity'] >= 2:
            printer('      │      ' + Fore.CYAN + '■ Name Servers' + Style.RESET_ALL)
            for ns in whois['name_servers']:
                i += 1
                if i == 1:
                    printer('      └┐      ■■  Nameserver {0}:         '.format(i) + Fore.YELLOW + ns + Style.RESET_ALL)
                elif i == len(whois['name_servers']):
                    printer('      ┌┘      ■■  Nameserver {0}:         '.format(i) + Fore.YELLOW + ns + Style.RESET_ALL)
                else:
                    printer('       │      ■■  Nameserver {0}:         '.format(i) + Fore.YELLOW + ns + Style.RESET_ALL)

    else:
        if config['verbosity'] >= 4:
            printer('      │      ■■ Error: ' + Fore.RED + 'No valid Whois API key for "{0}" is set.'.format(api) + Style.RESET_ALL)
        return whois

    # return the result in the format of list instead of set
    return whois    
