#!/usr/bin/env python

import csv
from unittest import result
from colorama import Back, Fore, Style
from config import config
from modules.utils import csv_maker, exception_report, printer

# write into a CSV file
def csv_writer(file_name, json_data):
    # write the result in the output file
    try:
        # print the name of the domain
        printer('\n [' + Fore.GREEN + '+' + Fore.WHITE + ']──┬──' + 
                Fore.RED + Back.WHITE + ' Write into {0} '.format(file_name) + Style.RESET_ALL +
                Fore.GREEN + Style.RESET_ALL + '\n      │')
        
        # open the file and start writing in it
        with open(file_name, mode='w', encoding='UTF8', newline='') as output_file:
            writer = csv.writer(output_file, delimiter=config['output']['csv']['delimiter']['column'], quoting=csv.QUOTE_MINIMAL)

            # formulate the header and write it into the CSV
            ssl_header = csv_maker(config['output']['include']['ssl'], config['output']['include']['ssl'])[0]
            whois_header = csv_maker(config['output']['include']['whois'], config['output']['include']['whois'])[0]
            http_header = csv_maker(config['output']['include']['http'], config['output']['include']['http'])[0]

            # form the header
            header = ['domain'] + \
                    ssl_header + \
                    config['dns']['dns_records'].copy() + \
                    whois_header + \
                    http_header
            
            # write the header
            writer.writerow(header)

            # iterate over domains
            for domain, results in json_data.items():
                # compose the line
                line = []

                # append the domain name to the line
                line.append(domain)
                line += csv_maker(json_data[domain]['ssl'], config['output']['include']['ssl'])[1]

                # append DNS records to the line
                for r in config['dns']['dns_records']:
                    # ignore the TXT details that are defined in the config file
                    # as all will be stored in the key 'txt'
                    # i.e. 'TXT/_dmarc'
                    if '/' in r:
                        continue
                    line.append(config['output']['csv']['delimiter']['dns_records'].join(results['dns_records'][r]))
                
                line += csv_maker(json_data[domain]['whois'], config['output']['include']['ssl'])[1]
                line += csv_maker(json_data[domain]['http'], config['output']['include']['ssl'])[1]

                # write the line into the CSV file
                writer.writerow(line)
            
        # close the file
        output_file.close()

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
        printer('      │\n      └───' + Fore.RED + Back.WHITE + ' Finish Writing in "{0}" '.format(file_name) + Style.RESET_ALL + '\n')