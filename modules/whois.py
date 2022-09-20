import requests
import json
from datetime import datetime
from colorama import Fore, Back, Style
from config import config
from modules.utils import *


# get the wohis of the domain form different sources
def whois(domain, api):
    # call the WhoisXML API and parse data
    def whoisxml(whois, domain):
        # check if the whois API key is set
        if config['api']['whoisxml']['api_key'] == '':
            print('      │      ■ ' + Fore.RED + 'WhoisXML API key is not defined.' + Style.RESET_ALL)
            return whois
        else:
            # call the API
            r = requests.get(config['api']['whoisxml']['url_whois'].format(config['api']['whoisxml']['api_key'], domain))
            json_data = json.loads(r.text)['WhoisRecord']

            date_format = config['api']['whoisxml']['date_format']
            whois = {
                # convert string dates to the object date and format it accordingly
                'create_date': date_formatter(json_checker(json_data, 'registryData', 'createdDate'), date_format),
                'update_date': date_formatter(json_checker(json_data, 'registryData', 'updatedDate'), date_format),
                'expiration_date': date_formatter(json_checker(json_data, 'registryData', 'expiresDate'), date_format),
                'domain_age_days': (datetime.now() - datetime.strptime(json_checker(json_data, 'registryData', 'createdDate'), date_format)).days,
                'registrar': {
                    'name': json_checker(json_data, 'registrarName', ''),
                    'iana_id': json_checker(json_data, 'registrarIANAID', ''),
                    'website': '',
                    'whois_server': json_checker(json_data, 'whoisServer', ''),
                    'email': json_checker(json_data, 'contactEmail', ''),
                    'phone': ''
                },
                'registrant': {
                    'name': json_checker(json_data, 'registrant', 'organization'),
                    'country': json_checker(json_data, 'registrant', 'country'),
                    'email': '',
                    'phone': ''
                },
                'administrative': {
                    'name': json_checker(json_data, 'administrativeContact', 'organization'),
                    'country': json_checker(json_data, 'administrativeContact', 'country'),
                    'email': '',
                    'phone': ''
                },
                'technical': {
                    'name': json_checker(json_data, 'technicalContact', 'organization'),
                    'country': json_checker(json_data, 'technicalContact', 'country'),
                    'email': '',
                    'phone': ''
                },
                'name_servers': json_checker(json_data, 'nameServers', 'hostNames')
            }

            return whois


    # call the Whoxy API and parse data
    def whoxy(whois, domain):
        # check if the whois API key is set
        if config['api']['whoxy']['api_key'] == '':
            print('      │      ■ ' + Fore.RED + 'Whoxy API key is not defined.' + Style.RESET_ALL)
            return whois
        else:
            # call the API
            r = requests.get(config['api']['whoxy']['url_whois'].format(config['api']['whoxy']['api_key'], domain))
            json_data = json.loads(r.text)

            date_format = config['api']['whoxy']['date_format']
            whois = {
                # convert string dates to the object date and format it accordingly
                'create_date': date_formatter(json_checker(json_data, 'create_date', ''), date_format),
                'update_date': date_formatter(json_checker(json_data, 'update_date', ''), date_format),
                'expiration_date': date_formatter(json_checker(json_data, 'expiry_date', ''), date_format),
                'domain_age_days': (datetime.now() - datetime.strptime(json_checker(json_data, 'create_date', ''), date_format)).days,
                'registrar': {
                    'name': json_checker(json_data, 'domain_registrar', 'registrar_name'),
                    'iana_id': json_checker(json_data, 'domain_registrar', 'iana_id'),
                    'website': json_checker(json_data, 'domain_registrar', 'website_url'),
                    'whois_server': json_checker(json_data, 'domain_registrar', 'whois_server'),
                    'email': json_checker(json_data, 'domain_registrar', 'email_address'),
                    'phone': json_checker(json_data, 'domain_registrar', 'phone_number')
                },
                'registrant': {
                    'name': json_checker(json_data, 'registrant_contact', 'company_name'),
                    'country': json_checker(json_data, 'registrant_contact', 'country_name'),
                    'email': json_checker(json_data, 'registrant_contact', 'email_address'),
                    'phone': ''
                },
                'administrative': {
                    'name': json_checker(json_data, 'administrative_contact', 'company_name'),
                    'country': json_checker(json_data, 'administrative_contact', 'country_name'),
                    'email': json_checker(json_data, 'administrative_contact', 'email_address'),
                    'phone': ''
                },
                'technical': {
                    'name': json_checker(json_data, 'technical_contact', 'company_name'),
                    'country': json_checker(json_data, 'technical_contact', 'country_name'),
                    'email': json_checker(json_data, 'technical_contact', 'email_address'),
                    'phone': ''
                },
                'name_servers': json_checker(json_data, 'nameServers', '')
            }

            return whois


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
    print('      ├───' + Fore.BLACK + Back.WHITE + ' Whois ' + Style.RESET_ALL)

    try:
        # call the asked whois API
        if api == 'whoisxml':
            whois = whoisxml(whois, domain)
        elif api == 'whoxy':
            whois = whoxy(whois, domain)
        else:
            print(Fore.RED + '      │      ■ ' + Fore.RED + 'No valid Whois API is set.' + Style.RESET_ALL)

        # print the result on STDOUT
        print('      │      ■ Registration Date:      ' + Fore.YELLOW + whois['create_date'] + Style.RESET_ALL)
        print('      │      ■ Last Modification Date: ' + Fore.YELLOW + whois['update_date'] + Style.RESET_ALL)
        print('      │      ■ Expiration Date:        ' + Fore.YELLOW + whois['expiration_date'] + Style.RESET_ALL)
        print('      │      ■ Domain Age:             ' + Fore.YELLOW + str(whois['domain_age_days']) + ' Days' + Style.RESET_ALL)
        print('      │      ' + Fore.CYAN + '■ Registrar Detains' + Style.RESET_ALL)
        print('      └┐      ■■  Name:                ' + Fore.YELLOW + whois['registrar']['name'] + Style.RESET_ALL)
        print('       │      ■■  IANA ID:             ' + Fore.YELLOW + str(whois['registrar']['iana_id']) + Style.RESET_ALL)
        print('       │      ■■  Website:             ' + Fore.YELLOW + whois['registrar']['website'] + Style.RESET_ALL)
        print('       │      ■■  Wohis Server:        ' + Fore.YELLOW + whois['registrar']['whois_server'] + Style.RESET_ALL)
        print('       │      ■■  Email:               ' + Fore.YELLOW + whois['registrar']['email'] + Style.RESET_ALL)
        print('      ┌┘      ■■  Phone:               ' + Fore.YELLOW + whois['registrar']['phone'] + Style.RESET_ALL)
        print('      │      ' + Fore.CYAN + '■ Registrant Detains' + Style.RESET_ALL)
        print('      └┐      ■■  Name:                ' + Fore.YELLOW + whois['registrant']['name'] + Style.RESET_ALL)
        print('       │      ■■  Country:             ' + Fore.YELLOW + whois['registrant']['country'] + Style.RESET_ALL)
        print('       │      ■■  Email:               ' + Fore.YELLOW + whois['registrant']['email'] + Style.RESET_ALL)
        print('      ┌┘      ■■  Phone:               ' + Fore.YELLOW + whois['registrant']['phone'] + Style.RESET_ALL)
        print('      │      ' + Fore.CYAN + '■ Administrative Detains' + Style.RESET_ALL)
        print('      └┐      ■■  Name:                ' + Fore.YELLOW + whois['administrative']['name'] + Style.RESET_ALL)
        print('       │      ■■  Country:             ' + Fore.YELLOW + whois['administrative']['country'] + Style.RESET_ALL)
        print('       │      ■■  Email:               ' + Fore.YELLOW + whois['administrative']['email'] + Style.RESET_ALL)
        print('      ┌┘      ■■  Phone:               ' + Fore.YELLOW + whois['administrative']['phone'] + Style.RESET_ALL)
        print('      │      ' + Fore.CYAN + '■ Technical Detains' + Style.RESET_ALL)
        print('      └┐      ■■  Name:                ' + Fore.YELLOW + whois['technical']['name'] + Style.RESET_ALL)
        print('       │      ■■  Country:             ' + Fore.YELLOW + whois['technical']['country'] + Style.RESET_ALL)
        print('       │      ■■  Email:               ' + Fore.YELLOW + whois['technical']['email'] + Style.RESET_ALL)
        print('      ┌┘      ■■  Phone:               ' + Fore.YELLOW + whois['technical']['phone'] + Style.RESET_ALL)
        print('      │      ' + Fore.CYAN + '■ Name Servers' + Style.RESET_ALL)
        for ns in whois['name_servers']:
            i += 1
            if i == 1:
                print('      └┐      ■■  Nameserver {0}:         '.format(i) + Fore.YELLOW + ns + Style.RESET_ALL)
            elif i == len(whois['name_servers']):
                print('      ┌┘      ■■  Nameserver {0}:         '.format(i) + Fore.YELLOW + ns + Style.RESET_ALL)
            else:
                print('       │      ■■  Nameserver {0}:         '.format(i) + Fore.YELLOW + ns + Style.RESET_ALL)

    except requests.exceptions.HTTPError as e:
        print('      │      ■ ' + Fore.RED + 'Error in loading the HTTP page.' + Style.RESET_ALL)
        print('      │      ■■ ERROR: ' + Fore.RED + str(e) + Style.RESET_ALL)        
    except requests.exceptions.ConnectionError as e:
        print('      │      ■ ' + Fore.RED + 'Error in establishing the connection.' + Style.RESET_ALL)
        print('      │      ■■ ERROR: ' + Fore.RED + str(e) + Style.RESET_ALL)  
    except requests.exceptions.Timeout as e:
        print('      │      ■ ' + Fore.RED + 'Timeout error.' + Style.RESET_ALL)
        print('      │      ■■ ERROR: ' + Fore.RED + str(e) + Style.RESET_ALL)  
    except requests.exceptions.RequestException as e:
        print('      │      ■ ' + Fore.RED + 'Error in reading the data from the website.' + Style.RESET_ALL)
        print('      │      ■■ ERROR: ' + Fore.RED + str(e) + Style.RESET_ALL) 
    except ValueError as e:
        print('      │      ■ ' + Fore.RED + 'No Result is found or there was an error.' + Style.RESET_ALL)
        print('      │      ■■ ERROR: ' + Fore.RED + str(e) + '\r\n' + Style.RESET_ALL)

    # return the list instead of set
    return whois    
