#!/usr/bin/env python

from colorama import Fore, Back, Style

from modules.ssl.openssl import openssl
from modules.ssl.crt_sh import crt_sh
from modules.ssl.ssl_labs import ssl_labs
from modules.utilities.printer import printer
from modules.utils import json_value


def ssl_checker(domain):
    """
        This function is responsible for getting SSL certificate details through
        different methods. Therefore, it will print the summary results on STDOUT.

        # Input:  a single domain name
        # Output: a dictionary contains SSL certificate details
    """
    # a variable to store cert info
    cert_info = set()

    # get the data and update the set
    cert_info = openssl(domain)
    cert_info.update(crt_sh(domain))
    cert_info.update(ssl_labs(domain))

    # print out found SSL info
    printer('      │\n      ├───' + Fore.BLACK + Back.WHITE + ' SSL Certificate Details ' + Style.RESET_ALL)

    # print the results
    if cert_info:
        printer('      │      ■ Issue Date:            ' + Fore.YELLOW + json_value(cert_info['validity'], 'issue_date') + Style.RESET_ALL)
        printer('      │      ■ Expiration Date:       ' + Fore.YELLOW + json_value(cert_info['validity'], 'expiration_date') + Style.RESET_ALL)
        printer('      │      ■ Validity:              ' + Fore.YELLOW + json_value(cert_info['validity'], 'past_days') + ' days past & ' + json_value(cert_info['validity'], 'left_days') + ' days remained' + Style.RESET_ALL)
        printer('      │      ■ Signature:             ' + Fore.YELLOW + json_value(cert_info, 'signature') + Style.RESET_ALL)
        printer('      │      ■ Fingerprint (SHA-256): ' + Fore.YELLOW + json_value(cert_info['fingerprint'], 'sha256') + Style.RESET_ALL)
        printer('      │      ■ Serial Number:         ' + Fore.YELLOW + json_value(cert_info, 'serial_number') + Style.RESET_ALL)
        printer('      │      ' + Fore.CYAN + '■ Issuer' + Style.RESET_ALL)
        printer('      └┐      ■■  Name:           ' + Fore.YELLOW + json_value(cert_info['issuer'], 'common_name') + Style.RESET_ALL)
        printer('       │      ■■  Org. Name:      ' + Fore.YELLOW + json_value(cert_info['issuer'], 'organization_name') + Style.RESET_ALL)
        printer('       │      ■■  Org. Unit Name: ' + Fore.YELLOW + json_value(cert_info['issuer'], 'organization_unit_name') + Style.RESET_ALL)
        printer('       │      ■■  Country:        ' + Fore.YELLOW + json_value(cert_info['issuer'], 'country') + Style.RESET_ALL)
        printer('       │      ■■  State:          ' + Fore.YELLOW + json_value(cert_info['issuer'], 'state') + Style.RESET_ALL)
        printer('       │      ■■  City:           ' + Fore.YELLOW + json_value(cert_info['issuer'], 'city') + Style.RESET_ALL)
        printer('      ┌┘      ■■  email:          ' + Fore.YELLOW + json_value(cert_info['issuer'], 'email_address') + Style.RESET_ALL)
        printer('      │      ' + Fore.CYAN + '■ Subject' + Style.RESET_ALL)
        printer('      └┐      ■■  Name:           ' + Fore.YELLOW + json_value(cert_info['subject'], 'common_name') + Style.RESET_ALL)
        printer('       │      ■■  Org. Name:      ' + Fore.YELLOW + json_value(cert_info['subject'], 'organization_name') + Style.RESET_ALL)
        printer('       │      ■■  Org. Unit Name: ' + Fore.YELLOW + json_value(cert_info['subject'], 'organization_unit_name') + Style.RESET_ALL)
        printer('       │      ■■  Country:        ' + Fore.YELLOW + json_value(cert_info['subject'], 'country') + Style.RESET_ALL)
        printer('       │      ■■  State:          ' + Fore.YELLOW + json_value(cert_info['subject'], 'state') + Style.RESET_ALL)
        printer('       │      ■■  City:           ' + Fore.YELLOW + json_value(cert_info['subject'], 'city') + Style.RESET_ALL)
        printer('      ┌┘      ■■  email:          ' + Fore.YELLOW + json_value(cert_info['subject'], 'email_address') + Style.RESET_ALL)
    else:
        printer('      │      ■■ ' + Fore.RED + 'No SSL certificate detail is found.' + Style.RESET_ALL)

    # return the result in the format of list instead of set
    return cert_info
