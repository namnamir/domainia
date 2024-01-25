#!/usr/bin/env python

from colorama import Fore, Style
import dns.resolver

from config import config
from modules.utilities.printer import printer
from modules.utilities.error_printer import error_printer

def dns_resolver(domain, record, print_args):
    """
        ### DNS Checker: DNS Dig

        This function gets the value of all DNS records.

        # Input:  - a single domain name
                - the key, subdomain, or selector.subdomain
                - a single DNS record either in an RR type (int) or case-insensitive string; e.g. 1 or A or a
        # Output: - a set of dictionaries contains a single DNS record details
    """
    results = list()

    # set the DNS server
    dns.resolver.Resolver().nameservers = config['dns']['dns_servers']

    try:
        answers = dns.resolver.resolve(domain, record)
        for answer in answers:
            results.append(answer.to_text())

    except dns.resolver.NoAnswer:
        if print_args[0]:
            ex = error_printer()
            printer(print_args[1] + Fore.RED + 'The DNS query "{0}" for "{1}" returned no answer.'.format(record, domain) + Style.RESET_ALL)
            if config['verbosity'] >= 4:
                printer(print_args[2] + 'ERROR: ' + Fore.MAGENTA + ex[0] + ' → ' + ex[4] + ':' + ex[3] + Fore.RED + '  ' + ex[1] + Style.RESET_ALL)
    except dns.resolver.NXDOMAIN:
        if print_args[0]:
            ex = error_printer()
            printer(print_args[1] + Fore.RED + 'QUERY "{0}": The domain "{1}" does not exist.'.format(record, domain) + Style.RESET_ALL)
            if config['verbosity'] >= 4:
                printer(print_args[2] + 'ERROR: ' + Fore.MAGENTA + ex[0] + ' → ' + ex[4] + ':' + ex[3] + Fore.RED + '  ' + ex[1] + Style.RESET_ALL)
    except dns.resolver.NoNameservers:
        if print_args[0]:
            ex = error_printer()
            printer(print_args[1] + Fore.RED + 'All nameservers failed to answer the DNS query "{0}" for "{1}".'.format(record, domain) + Style.RESET_ALL)
            if config['verbosity'] >= 4:
                printer(print_args[2] + 'ERROR: ' + Fore.MAGENTA + ex[0] + ' → ' + ex[4] + ':' + ex[3] + Fore.RED + '  ' + ex[1] + Style.RESET_ALL)
    except Exception:
        if print_args[0]:
            ex = error_printer()
            printer(print_args[1] + Fore.RED + 'QUERY "{0}": No result is found for "{1}" or there was an error.'.format(record, domain) + Style.RESET_ALL)
            if config['verbosity'] >= 4:
                printer(print_args[2] + 'ERROR: ' + Fore.MAGENTA + ex[0] + ' → ' + ex[4] + ':' + ex[3] + Fore.RED + '  ' + ex[1] + Style.RESET_ALL)

    # return the list of the DNS results
    finally:
        return results
