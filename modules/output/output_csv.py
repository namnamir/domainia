#!/usr/bin/env python


"""
    ### Output: CSV

    This function generates a CSV file based on the data
    
    # Input:  - a filename
              - a dictionary contains all the data
              - a list of tags define what data should be written into the CSV file
                [ssl, whois, http, dns, related_sub_domains]
    # Output: - a CSV file
"""


import csv
from colorama import Back, Fore, Style

from config import config
from modules.output.utils import csv_maker, flat_json
from modules.utils import exception_report, printer


def csv_writer(file_name, json_data, tags):
    # some variables
    ssl_header = list()
    whois_header = list()
    http_header = set()
    dns_records = list()
    related_sub_domains = list()

    # write the result in the output file
    try:
        # print the name of the domain
        printer('\n [' + Fore.GREEN + '+' + Fore.WHITE + ']──┬──' + 
                Fore.RED + Back.WHITE + ' Write into {0} '.format(file_name) + Style.RESET_ALL +
                Fore.GREEN + Style.RESET_ALL + '\n      │')
        
        # open the file and start writing in it
        with open(file_name, mode='w', encoding='UTF8', newline='') as output_file:
            writer = csv.writer(output_file, delimiter=config['output']['csv']['delimiter']['column'], quoting=csv.QUOTE_MINIMAL)

            # iterate over domains
            for domain, results in json_data.items():
                # update all HTTP headers
                if tags[2]:
                    print('+++++++',results['http'])
                    http_header.update(
                        csv_maker(results['http'], '')[0]
                    )

            http_header = list(http_header)
            # # formulate the header and write it into the CSV
            # if tags[0]:
            #     ssl_header = csv_maker(
            #         config['output']['include']['ssl'],
            #         config['output']['include']['ssl']
            #     )[0]
            # if tags[1]:
            #     whois_header = csv_maker(
            #         config['output']['include']['whois'],
            #         config['output']['include']['whois']
            #     )[0]
            # if tags[2]:
            #     http_header = csv_maker(
            #         config['output']['include']['http'],
            #         config['output']['include']['http']
            #     )[0]
            # if tags[3]:
            #     dns_records = config['dns']['dns_records'].copy()
            # if tags[4]:
            #     related_sub_domains = ['related_domains', 'subdomains']

            # form the header
            header = ['domain'] + \
                    ssl_header + \
                    dns_records + \
                    whois_header + \
                    http_header + \
                    related_sub_domains
            
            # write the header
            writer.writerow(header)

            # iterate over domains
            for domain, results in json_data.items():
                # compose the line
                line = []
                f=''

                # append the domain name to the line
                line.append(domain)

                # append the SSL data
                if tags[0]:
                    line += csv_maker(
                        json_data[domain]['ssl'],
                        config['output']['include']['ssl']
                    )[1]

                # append the DNS records data
                if tags[3]:
                    # append DNS records to the line
                    for r in config['dns']['dns_records']:
                        # ignore the TXT details that are defined in the config file
                        # as all will be stored in the key 'txt'
                        line.append(config['output']['csv']['delimiter']['dns_records'].join(results['dns_records'][r]))
                
                # append the whois data
                if tags[1]:
                    line += csv_maker(
                        json_data[domain]['whois'],
                        config['output']['include']['whois']
                    )[1]
                
                # append the HTTP data
                if tags[2]:
                    # print(results['http'])
                    f1=csv_maker(results['http'],'')[2]
                    i=0
                    for key in http_header:
                        # if 'redirects' in key:
                        #     print('=========',key, f1)
                        i+=1
                        if key in f1:
                            # print(f'--{i}-',key,'----    ',f1[key])
                            line.append(f1[key])
                        else:
                            # print(f'+-{i}-',key,'----    ')
                            line.append('')
                    # line += f
                    # print(line)
                
                # # append the related domains and subdomains
                # if tags[4]:
                #     line += csv_maker(
                #         json_data[domain]['related_domain'],
                #         's'
                #     )[1]
                #     line += csv_maker(
                #         json_data[domain]['subdomain'],
                #         ''
                #     )[1]

                # write the line into the CSV file
                writer.writerow(line)

    except IOError:
        ex = exception_report()
        printer('      │ ■ ' + Fore.RED + 'Error in in I/O (input/output).' + Style.RESET_ALL)
        if config['verbosity'] >= 4:
            printer('      │ ■■ ' + 'ERROR: ' + Fore.MAGENTA + ex[0] + ' → ' + ex[4] + ':' + ex[3] (ex[3].errno, ex[3].strerror)+ Fore.RED + '  ' + ex[1] + Style.RESET_ALL)
    except csv.Error:
        ex = exception_report()
        printer('      │ ■ ' + Fore.RED + 'Error in the CSV module.' + Style.RESET_ALL)
        if config['verbosity'] >= 4:
            printer('      │ ■■ ' + 'ERROR: ' + Fore.MAGENTA + ex[0] + ' → ' + ex[4] + ':' + ex[3] + Fore.RED + '  ' + ex[1] + Style.RESET_ALL)
    except ValueError:
        ex = exception_report()
        printer('      │ ■ ' + Fore.RED + 'Error in values are going to be written in the CSV file.' + Style.RESET_ALL)
        if config['verbosity'] >= 4:
            printer('      │ ■■ ' + 'ERROR: ' + Fore.MAGENTA + ex[0] + ' → ' + ex[4] + ':' + ex[3] + Fore.RED + '  ' + ex[1] + Style.RESET_ALL)
    except Exception:
        ex = exception_report()
        printer('      │ ■ ' + Fore.RED + 'Error in writing into the CSV file.' + Style.RESET_ALL)
        if config['verbosity'] >= 4:
            printer('      │ ■■ ' + 'ERROR: ' + Fore.MAGENTA + ex[0] + ' → ' + ex[4] + ':' + ex[3] + Fore.RED + '  ' + ex[1] + Style.RESET_ALL)
    finally:
        # print a message shows the scan for the domain is finished
        printer('      │\n      └──' + Fore.RED + Back.WHITE + ' Finish Writing in "{0}" '.format(file_name) + Style.RESET_ALL + '\n')
