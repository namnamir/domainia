#!/usr/bin/env python

from colorama import Fore, Back, Style

from config import config
from modules.utilities.printer import printer


# get the wohis of the domain form different sources
def whois_lookup(domain, api):
    # some variables
    i = 0

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
