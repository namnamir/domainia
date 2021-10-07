from dns.rdatatype import NULL
import dns.resolver
from config import config
from colorama import Fore, Back, Style

# resolve the DNS and get all the defined records
def dns_resolver(domain):
    records = {}
        
    # set the DNS server
    Resolver = dns.resolver.Resolver()
    Resolver.nameservers = config['dns_servers']

    # iterate over records and resolve them
    for r in config['records']:
        records[r] = {}
        temp = []
        # print the record
        print('      ├───' +  Fore.BLACK + Back.WHITE + ' {0} Records '.format(r) + Style.RESET_ALL)

        try:
            answers = Resolver.resolve(domain, r)
            # iterate over the DNS records
            for rdata in answers:
                rd = rdata.to_text()
                if r == 'TXT' and not ('spf' in rd or 'dmarc' in rd or 'domainkey' in rd.lower()):
                    print(Fore.WHITE + '      │      ■ (will not be stored): ' + Fore.YELLOW + rd + Style.RESET_ALL)
                    continue
                else:
                    print(Fore.WHITE + '      │      ■ ' + Fore.YELLOW + rd + Style.RESET_ALL)
                    temp.append(rd)

            # add the result into the JSON
            records[r] = temp
    
        except Exception as e:
            records[r] = []
            print(Fore.WHITE + '      │      ■ ' + Fore.RED + 'No Result is found or there was an error.' + Style.RESET_ALL)
            print(Fore.WHITE + '      │      ■■ ERROR: ' + Fore.RED + str(e) + Style.RESET_ALL)
            continue
    
   # return the list of the records 
    return records