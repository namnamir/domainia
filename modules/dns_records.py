import dns.resolver
from colorama import Fore, Back, Style
from config import config
from modules.ip_lookup import validate_ip, ip_lookup

# resolve the DNS and get all the defined records
def dns_resolver(domain):
    records = {}
        
    # set the DNS server
    dns.resolver.Resolver().nameservers = config['dns_servers']

    # print the title of the section
    print('      │\r\n      ├───' +  Fore.BLACK + Back.WHITE + ' DNS Records ' + Style.RESET_ALL)
        
    # iterate over records and resolve them
    for r in config['dns_records']:
        i = 0
        records[r] = {}
        temp = []

        # print the title of the section
        print('      │      ' + Fore.CYAN + '■ {0} Records       '.format(r) + Style.RESET_ALL)

        try:
            answers = dns.resolver.resolve(domain, r)
            # iterate over the DNS records and print the result on STDOUT
            for record in answers:
                i += 1
                record = str(record)
                # if it is a TXT record but not listed in the config file
                if r == 'TXT' and not any(txt.lower() in record.lower() for txt in config['include_txt_records']):
                    color = Fore.MAGENTA
                else:
                    color = Fore.YELLOW
                    temp.append(record)
                
                # print the result on STDOUT
                l_start = '       │' # for printing IP lookups
                if len(answers) == 1:
                    print('      ╞       ■■  ' + color + record + Style.RESET_ALL)
                    l_start = '      │ '
                elif i == 1:
                    print('      └┐      ■■  ' + color + record + Style.RESET_ALL)
                elif i == len(answers):
                    print('      ┌┘      ■■  ' + color + record + Style.RESET_ALL)
                    l_start = '      │ '
                else:
                    print('       │      ■■  ' + color + record + Style.RESET_ALL)
                
                # print the IP lookup results, if the result is an IP
                if validate_ip(record):
                    l = ip_lookup(record)
                    print(l_start + '              ├□ Location:    ' + Fore.CYAN + l['city'] + ', ' + l['country'] + Style.RESET_ALL)
                    print(l_start + '              ├□ ISP Name:    ' + Fore.CYAN + l['isp'] + Style.RESET_ALL)
                    print(l_start + '              ├□ Org. Name:   ' + Fore.CYAN + l['organization'] + Style.RESET_ALL)
                    print(l_start + '              ├□ Reverse DNS: ' + Fore.CYAN + l['reverse_dns'] + Style.RESET_ALL)
                    print(l_start + '              ├□ Is Mobile?   ' + Fore.CYAN + l['mobile'] + Style.RESET_ALL)
                    print(l_start + '              ├□ Is Proxy?    ' + Fore.CYAN + l['proxy'] + Style.RESET_ALL)
                    print(l_start + '              └□ Is Hosting?  ' + Fore.CYAN + l['hosting'] + Style.RESET_ALL)

            # add the result into the JSON
            records[r] = temp
    
        except Exception as e:
            records[r] = []
            print('      │       ■ ' + Fore.RED + 'No Result is found or there was an error.' + Style.RESET_ALL)
            print('      │       ■■ ERROR: ' + Fore.RED + str(e) + Style.RESET_ALL)
            continue
    
   # return the list of the records 
    return records