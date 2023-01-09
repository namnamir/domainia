#!/usr/bin/env python


"""
    ### DNS Records: DNS Resolver

    This function resolves DNS records (something similar to DIG).
    
    # Input:  - a single domain name
              - a single DNS record
              - a list of print arguments
    # Output: - a list of values related to the given DNS record
"""


from colorama import Fore, Style
import dns.resolver

from config import config
from modules.utils import printer, exception_report


def dns_resolver(domain, record, print_args):
    results = list()
        
    # set the DNS server
    dns.resolver.Resolver().nameservers = config['dns']['dns_servers']

    try:
        answers = dns.resolver.resolve(domain, record)
        for answer in answers: 
            results.append(answer.to_text())

    except dns.resolver.NoAnswer:
        if print_args[0]:
            ex = exception_report()
            printer(print_args[1] + Fore.RED + 'The DNS query "{0}" for "{1}" returned no answer.'.format(record, domain) + Style.RESET_ALL)
            if config['verbosity'] >= 4:
                printer(print_args[2] + 'ERROR: ' + Fore.MAGENTA + ex[0] + ' → ' + ex[4] + ':' + ex[3] + Fore.RED + '  ' + ex[1] + Style.RESET_ALL)
    except dns.resolver.NXDOMAIN:
        if print_args[0]:
            ex = exception_report()
            printer(print_args[1] + Fore.RED + 'QUERY "{0}": The domain "{1}" does not exist.'.format(record, domain) + Style.RESET_ALL)
            if config['verbosity'] >= 4:
                printer(print_args[2] + 'ERROR: ' + Fore.MAGENTA + ex[0] + ' → ' + ex[4] + ':' + ex[3] + Fore.RED + '  ' + ex[1] + Style.RESET_ALL)
    except dns.resolver.NoNameservers:
        if print_args[0]:
            ex = exception_report()
            printer(print_args[1] + Fore.RED + 'All nameservers failed to answer the DNS query "{0}" for "{1}".'.format(record, domain) + Style.RESET_ALL)
            if config['verbosity'] >= 4:
                printer(print_args[2] + 'ERROR: ' + Fore.MAGENTA + ex[0] + ' → ' + ex[4] + ':' + ex[3] + Fore.RED + '  ' + ex[1] + Style.RESET_ALL)
    except Exception:
        if print_args[0]:
            ex = exception_report()
            printer(print_args[1] + Fore.RED + 'QUERY "{0}": No result is found for "{1}" or there was an error.'.format(record, domain) + Style.RESET_ALL)
            if config['verbosity'] >= 4:
                printer(print_args[2] + 'ERROR: ' + Fore.MAGENTA + ex[0] + ' → ' + ex[4] + ':' + ex[3] + Fore.RED + '  ' + ex[1] + Style.RESET_ALL)

    # return the list of the DNS results
    finally:
        return results
