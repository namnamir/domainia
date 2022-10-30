#!/usr/bin/env python

import re
from colorama import Fore, Back, Style
from config import config
from modules.utils import run_requests, re_position, date_formatter, printer


# parse the SSL certificate
def ssl_parser(domain):
    # some variables
    ssl_info = {
        'issue_date': '',
        'expiration_date': '',
        'signature': '',
        'serial_number': '',
        'issuer': {
            'common_name': '',
            'organization_name': '',
            'country': '',
            'organization_unit_name': '',
        },
        'subject': {
            'common_name': '',
            'organization_name': '',
            'country': '',
            'locality_name': '',
        }
    }

    # print out found SSL info
    printer('      │\n      ├───' + Fore.BLACK + Back.WHITE + ' SSL Certificate Details ' + Style.RESET_ALL)
    
    # get the date format of the crt.sh from the config file
    date_format = config['api']['crt_sh']['date_format']
    # set the print arguments for the function "run_requests"
    print_args = [True, '      │      ■ ', '      │      ■■ ']

    # download the certificate page on CRT
    try:
        printer('      │        ├□ ' + Fore.GREEN + 'CRT.sh API is calling' + Style.RESET_ALL)
        url = config['api']['crt_sh']['url'].format(domain)
        json_data = run_requests(url, '', 'json', 'Crt.sh API', print_args)
    except:
        printer('      │        ├──■ ' + Fore.RED + 'Error in getting the list of SSL certificates.' + Style.RESET_ALL)
        return ssl_info

    # continue only if there is any data for it
    if json_data:
        # sort certificates by ID to get the details of the latest one
        json_data = sorted(json_data, key=lambda k: k['id'], reverse=True)

        try:
            url = config['api']['crt_sh']['url_single'].format(json_data[0]['id'])
            cert = run_requests(url, '', 'text', 'Crt.sh API', print_args)
        except:
            printer('      │      ■■ ' + Fore.RED + 'Error in parsing the SSL certificate.' + Style.RESET_ALL)
            return ssl_info

        # fix the HTML format of the space
        cert = (cert.text).replace('&nbsp;', ' ')

        # get the latest info of the latest certificate
        ssl_info = {
            'issue_date': date_formatter(re_position(re.findall(r"Not Before[ =:]*(.*?)<BR>", cert), 0), date_format),
            'expiration_date': date_formatter(re_position(re.findall(r"Not After[ =:]*(.*?)<BR>", cert), 0), date_format),
            'signature': re_position(re.findall(r"Signature Algorithm[ :]*(.*?)<BR>", cert), 0),
            'serial_number': re_position(re.findall(r"Serial Number[ :]<\/A><BR>[ =]*(.*?)<BR>", cert), 0),
            'issuer': {
                'common_name': re_position(re.findall(r"commonName[ =]*(.*?)<BR>", cert), 0),
                'organization_name': re_position(re.findall(r"organizationName[ =]*(.*?)<BR>", cert), 0),
                'country': re_position(re.findall(r"countryName[ =]*(.*?)<BR>", cert), 0),
                'organization_unit_name': re_position(re.findall(r"organizationalUnitName[ =]*(.*?)<BR>", cert), 0),
            },
            'subject': {
                'common_name': re_position(re.findall(r"commonName[ =]*(.*?)<BR>", cert), 1),
                'organization_name': re_position(re.findall(r"organizationName[ =]*(.*?)<BR>", cert), 1),
                'country': re_position(re.findall(r"countryName[ =]*(.*?)<BR>", cert), 1),
                'locality_name': re_position(re.findall(r"localityName[ =]*(.*?)<BR>", cert), 0),
            },
        }
    
        # print the results
        printer('      │      ■ Issue Date: ' + Fore.YELLOW + ssl_info['issue_date'] + Style.RESET_ALL)
        printer('      │      ■ Expiration Date: ' + Fore.YELLOW + ssl_info['expiration_date'] + Style.RESET_ALL)
        printer('      │      ■ Signature: ' + Fore.YELLOW + ssl_info['signature'] + Style.RESET_ALL)
        printer('      │      ■ Serial Number: ' + Fore.YELLOW + ssl_info['serial_number'] + Style.RESET_ALL)
        printer('      │      ' + Fore.CYAN + '■ Issuer' + Style.RESET_ALL)
        printer('      └┐      ■■  Name: ' + Fore.YELLOW + ssl_info['issuer']['common_name'] + Style.RESET_ALL)
        printer('       │      ■■  Org. Name: ' + Fore.YELLOW + ssl_info['issuer']['organization_name'] + Style.RESET_ALL)
        printer('       │      ■■  Org. Unit Name: ' + Fore.YELLOW + ssl_info['issuer']['organization_unit_name'] + Style.RESET_ALL)
        printer('      ┌┘      ■■  Country: ' + Fore.YELLOW + ssl_info['issuer']['country'] + Style.RESET_ALL)
        printer('      │      ' + Fore.CYAN + '■ Subject' + Style.RESET_ALL)
        printer('      └┐      ■■  Name: ' + Fore.YELLOW + ssl_info['subject']['common_name'] + Style.RESET_ALL)
        printer('       │      ■■  Org. Name: ' + Fore.YELLOW + ssl_info['subject']['organization_name'] + Style.RESET_ALL)
        printer('       │      ■■  Local Name: ' + Fore.YELLOW + ssl_info['subject']['locality_name'] + Style.RESET_ALL)
        printer('      ┌┘      ■■  Country: ' + Fore.YELLOW + ssl_info['subject']['country'] + Style.RESET_ALL)
    else:
        printer('      │      ■■ ' + Fore.RED + 'No SSL certificate detail is found.' + Style.RESET_ALL)

    # return the result in the format of list instead of set
    return ssl_info
