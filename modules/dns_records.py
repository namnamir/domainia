#!/usr/bin/env python

from colorama import Fore, Back, Style
from time import sleep
from config import config
from modules.ip_lookup import validate_ip, ip_lookup
from modules.dns_spy import dns_spy
from modules.dnssec import dnssec
from modules.utils import dns_resolver, printer

# resolve the DNS and get all the defined records
def resolve_dns(domain):
    # a variable to record responses
    subdomains = []
    written_rec = []
    records = {}
    # set the print arguments for the function "run_requests"
    print_args = [True, '      │      ■ ', '      │      ■■ ']

    # print the title of the section
    printer('      │\n      ├───' + Fore.BLACK + Back.WHITE + ' DNS Records ' + Style.RESET_ALL)
        
    # get data from DNS Spy or return an empty dict
    printer('      │        └□ ' + Fore.GREEN + 'DNS Spy API is calling' + Style.RESET_ALL)
    records, subdomains = dns_spy(domain)

    # iterate over sorted records and resolve them
    dns_records_list = sorted(config['dns']['dns_records'])
    for r in dns_records_list:
        i = 0
        answers = list()
        temp = list()
       
        # if there is any details in the name of record (see config.py)
        # it is used when we are interested in names like DMARC in TXT record
        if '/' in r:
            rec, name = r.split('/')
            name += '.'
        else:
            name = ''
            rec = r

        # print the title of the section
        if rec not in written_rec:
            printer('      │      ' + Fore.CYAN + '■ {0} Records       '.format(rec) + Style.RESET_ALL)
            written_rec.append(rec)

        # run the relevant DNS resolver
        if rec == 'RRSIG':
            records[rec] = [dnssec(domain)]
        else:
            # resolve the DNS record
            try:
                ans = dns_resolver(name + domain, rec, print_args)
            except:
                continue

            # form answers
            for a in ans:
                answers.append(str(a))

        # add collected results from other methods, if any
        if not name and rec in records:
            if not isinstance(records[rec], list):
                answers += [records[rec]]
            else:
                answers += list(records[rec])

        # iterate over the DNS records and print the result on STDOUT
        for answer in answers:
            i += 1

            # if it is a TXT record but not listed in the config file
            if rec == 'TXT' and not any(txt.lower() in answer.lower() for txt in config['dns']['include_txt_records']):
                color = Fore.MAGENTA
            else:
                color = Fore.YELLOW
                temp.append(answer)
            
            # print the result on STDOUT
            l_start = '       │' # for printing IP lookups
            if len(answers) == 1:
                printer('      ╞       ■■ ' + color + answer + Style.RESET_ALL)
                l_start = '      │ '
            elif i == 1:
                printer('      └┐      ■■ ' + color + answer + Style.RESET_ALL)
            elif i == len(answers):
                printer('      ┌┘      ■■ ' + color + answer + Style.RESET_ALL)
                l_start = '      │ '
            else:
                printer('       │      ■■ ' + color + answer + Style.RESET_ALL)
            
            # if the result is an IP, print the IP lookup results
            if validate_ip(answer):
                lookup = ip_lookup(answer)
                if config['verbosity'] >= 3:
                    printer(l_start + ' ' * 14 + '├□ Location:    ' + Fore.CYAN + lookup['city'] + ', ' + lookup['country'] + Style.RESET_ALL)
                    printer(l_start + ' ' * 14 + '├□ ISP Name:    ' + Fore.CYAN + lookup['isp'] + Style.RESET_ALL)
                    printer(l_start + ' ' * 14 + '├□ Org. Name:   ' + Fore.CYAN + lookup['organization'] + Style.RESET_ALL)
                    printer(l_start + ' ' * 14 + '├□ Reverse DNS: ' + Fore.CYAN + lookup['reverse_dns'] + Style.RESET_ALL)
                    printer(l_start + ' ' * 14 + '├□ Is Mobile?   ' + Fore.CYAN + lookup['mobile'] + Style.RESET_ALL)
                    printer(l_start + ' ' * 14 + '├□ Is Proxy?    ' + Fore.CYAN + lookup['proxy'] + Style.RESET_ALL)
                    printer(l_start + ' ' * 14 + '└□ Is Hosting?  ' + Fore.CYAN + lookup['hosting'] + Style.RESET_ALL)

        # add the result into the JSON and remove duplicates
        if rec in records:
            records[rec] += list(set(temp))
        else:
            records[rec] = list(set(temp))
    
        # add a delay between DNS queries
        sleep(config['delay']['dns'])

    # return the list of the DNS records and subdomains
    return [
        records,
        subdomains
    ]
