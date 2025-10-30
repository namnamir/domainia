#!/usr/bin/env python

from typing import Dict
from colorama import Fore, Style

from modules.utilities.printer import printer
from modules.utilities.url_opener import url_opener


def security_txt(domain: str) -> Dict[str, object]:
    """
    Gets the details of the security.txt file and parses it.

    Args:
        domain: A single domain name.

    Returns:
        A dictionary contains security.txt details.
    """
    # a variable to store cert info
    security_txt = {
        'contact': set(),
        'encryption_key': set(),
        'language': set(),
        'security_policy': set(),
        'acknowledgments': set(),
        'hiring': '',
        'expiration_date': '',
        'signature_hash': '',
        'canonical': '',
    }

    # set the print arguments for the function "except_error_print"
    print_args = [True, '      │        ├──■ ', '      │        ├──■■ ']

    # download the security.txt and print the task
    printer(f'      │        ├□ {Fore.GREEN}security.txt is downloading{Style.RESET_ALL}')
    # open the page
    url = f'http://{domain}/.well-known/security.txt'
    text_data = url_opener('GET', url, '', '', '', 'text', 'security.txt file')[0]

    # check if there any 'security.txt' page exists
    if not text_data:
        printer(f'      │        ├□ {Fore.RED}Could not download security.txt or it does not exist{Style.RESET_ALL}')
        return security_txt

    # iterate over the lines in the security.txt file
    for line in str(text_data).splitlines():
        # ignore comments and empty lines
        if not line or line.startswith('#'):
            continue
        elif line.startswith('Contact:'):
            security_txt['contact'].add(line.split(':', maxsplit=1)[1].strip())
        elif line.startswith('Expires:'):
            security_txt['expiration_date'] = line.split(':', maxsplit=1)[1].strip()
        elif line.startswith('Encryption:'):
            security_txt['encryption_key'].add(line.split(':', maxsplit=1)[1].strip())
        elif line.startswith('Preferred-Languages:'):
            security_txt['language'].add(line.split(':', maxsplit=1)[1].strip().replace(' ', '').split(','))
        elif line.startswith('Canonical:'):
            security_txt['canonical'] = line.split(':', maxsplit=1)[1].strip()
        elif line.startswith('Policy:'):
            security_txt['security_policy'].add(line.split(':', maxsplit=1)[1].strip())
        elif line.startswith('Acknowledgments:'):
            security_txt['acknowledgments'].add(line.split(':', maxsplit=1)[1].strip())
        elif line.startswith('Hiring:'):
            security_txt['hiring'] = line.split(':', maxsplit=1)[1].strip()
        elif line.startswith('Hash:'):
            security_txt['signature_hash'] = line.split(':', maxsplit=1)[1].strip()

    return security_txt
