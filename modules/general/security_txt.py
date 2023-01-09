#!/usr/bin/env python


"""
    ### General: security_txt

    This function gets the details of the security.txt file and parse it.

    # Input:  - a single domain name
    # Output: - a dictionary contains security.txt details
"""


from colorama import Fore, Style

from modules.utils import run_requests, printer


def security_txt(domain):
    # a variable to store cert info
    security_txt = dict()
    contact = set()
    encryption_key = set()
    language = list()
    security_policy = set()
    acknowledgment = set()
    # set the print arguments for the function "except_error_print"
    print_args = [True, '      │        ├──■ ', '      │        ├──■■ ']

    # download the security.txt
    url = 'http://' + domain + '/.well-known/security.txt'
    printer('      │        ├□ ' + Fore.GREEN + 'security.txt is downloading' + Style.RESET_ALL)
    results = run_requests(url, '', 'text', 'security.txt file', print_args)[0]
    
    # check if 
    if not results:
        printer('      │        ├□ ' + Fore.RED + 'Could not download security.txt or it does not exist' + Style.RESET_ALL)
        return security_txt

    # iterate over the lines in the security.txt file
    for line in str(results).splitlines():
        # ignore comments and empty lines
        if not line or line.startswith('#'):
            continue
        elif line.startswith('Contact:'):
            contact.add(line.split(':', maxsplit=1)[1].strip())
        elif line.startswith('Expires:'):
            expiration_date = line.split(':', maxsplit=1)[1].strip()
            security_txt['expiration_date'] = expiration_date
        elif line.startswith('Encryption:'):
            encryption_key.add(line.split(':', maxsplit=1)[1].strip())
        elif line.startswith('Preferred-Languages:'):
            language += line.split(':', maxsplit=1)[1].strip().replace(' ', '').split(',')
        elif line.startswith('Canonical:'):
            canonical = line.split(':', maxsplit=1)[1].strip()
            security_txt['canonical'] = canonical
        elif line.startswith('Policy:'):
            security_policy.add(line.split(':', maxsplit=1)[1].strip())
        elif line.startswith('Acknowledgments:'):
            acknowledgment.add(line.split(':', maxsplit=1)[1].strip())
            security_txt['acknowledgments'] = acknowledgment
        elif line.startswith('Hiring:'):
            hiring = line.split(':', maxsplit=1)[1].strip()
            security_txt['hiring'] = hiring
        elif line.startswith('Hash:'):
            hash = line.split(':', maxsplit=1)[1].strip()
            security_txt['signature-hash'] = hash
    
    security_txt['contact'] = contact
    security_txt['encryption_key'] = encryption_key
    security_txt['language'] = set(language)
    security_txt['security_policy'] = security_policy
    security_txt['acknowledgments'] = acknowledgment

    return security_txt
