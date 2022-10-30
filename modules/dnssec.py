#!/usr/bin/env python

import dns.resolver
from colorama import Fore, Style
from config import config
from modules.utils import dns_resolver, printer


# get and validate RRSIG as it can't be retrieved directly by querying 'RRSIG'
# it needs a UDP query on port 53
def dnssec(domain):
    # set the print arguments for the function "run_requests"
    print_args = [False, '       │      ■ ', '       │      ■■ ']

    try: 
        # get the nameserver (NS) and A records of the domain
        ns_server = dns_resolver(domain, 'NS', print_args).rrset[0].to_text()
        a_record  = dns_resolver(ns_server, 'A', print_args).rrset[0].to_text()
        # get the DNSKEY of the domain
        dnskey = dns.message.make_query(domain, 'DNSKEY', want_dnssec=True)

        # send a UDP query on port 53 to get the RRSIG
        response = dns.query.udp(dnskey, a_record)

        # if there is any error based on the DNS RCODEs
        if response.rcode() != 0:
            error = config['dns']['dns_rcode'][response.rcode()]
            printer('      │       ■ ' + Fore.RED + 'There is an error: {0}.'.format(error) + Style.RESET_ALL)
        # parse the RRSIG for the DNSKEY from the response
        else:
            dns_sec = response.answer

            # if the array doesn't contain the DNSKEY and RRSIG
            if len(dns_sec) != 2:
                printer('      │       ■ ' + Fore.RED + 'Could not find any DNSKEY and RRSIG record in the zone' + Style.RESET_ALL)
            else:
                printer(dns_sec)
                printer('      │       ■■  ' + Fore.YELLOW + str(dns_sec[1]) + Style.RESET_ALL)
                
                # resolve the DNSSEC
                try:
                    name = dns.name.from_text(domain)
                    dns.dnssec.validate(dns_sec[0], dns_sec[1], {name:dns_sec[0]})
                except dns.dnssec.ValidationFailure:
                    printer('      │' + ' ' * 14 + '└□ ' + Fore.RED + 'The DNSSEC signature (RRSIG) is invalid.' + Style.RESET_ALL)
                except dns.dnssec.UnsupportedAlgorithm:
                    printer('      │' + ' ' * 14 + '└□ ' + Fore.CYAN + 'The DNSSEC algorithm is not supported.' + Style.RESET_ALL)
                else:
                    printer('      │' + ' ' * 14 + '└□ ' + Fore.GREEN + 'The DNSSEC is valid.' + Style.RESET_ALL)

                return str(dns_sec[1])

        return ''
    except:
        return ''