#!/usr/bin/env python

import argparse
from datetime import datetime
from colorama import init, Fore, Back, Style
from time import sleep
from config import config

from setup import setup_args
# from modules.whois_lookup import whois
from modules.html_status import site_status
# from modules.ssl_checker import ssl_parser
# from modules.dns_checker import resolve_dns
# from modules.subdomain_finder import subdomain_finder
from modules.utils import domain_sanitizer, printer
from modules.output.output_csv import csv_writer
from modules.output.output_json import json_writer
from modules.output.output_txt import txt_writer


if __name__ == '__main__':
    logo = f"""        
   ##  ##
 ##        ##
     ##  ##  ##  ########
 ##  ##  ###################
   ##    ####       #########
     ####  ####       ########
     ##  ####         ########
       ####  ##       ########
         ####        ########
       ##################### DOMAINIA
       ###################
----------------------------------------------------
            AN AUTOMATED DOMAIN SCANNER
----------------------------------------------------
 Version: {setup_args["version"]}
 Source:  {setup_args["url"]}
 PyPI:    {setup_args["download_url"]}
 By:      {setup_args["author"]} ({setup_args["author_email"]})
----------------------------------------------------

"""

    # a variable to store data in the JSON format
    json_result = {}

    # a set to maintain the list of the analyzed domains
    # it would prevent repetition
    analyzed_domains = set()

    # initiating Colorama
    init()

    # initiate the argument
    arg = argparse.ArgumentParser('Get the public information of a domain')
    arg.add_argument(
        '-i', '--input',
        dest='input',
        help='Path to the list of domain names, e.g. domains.txt. '
             'Each domain name should be in a line.'
    )
    arg.add_argument(
        '-d', '--domain',
        dest='domain',
        help='The comma separated list of domains'
    )
    arg.add_argument(
        '-w', '--whois',
        default='whoisxml',
        choices=['whoisxml', 'whoxy'],
        dest='whois_api',
        help='Whois API; default "whoisxml".\n'
             'Possible options: "whoisxml" and "whoxy"'
    )
    arg.add_argument(
        '-t', '--type',
        default='quick',
        choices=['quick', 'deep'],
        dest='scan_type',
        help='Type of the scan. If it is set, it will ignore the config file '
             'value for the scan type.\nPossible options: "quick" and "deep"'
    )
    arg.add_argument(
        '-o', '--output',
        default=config['output']['filename'],
        dest='output',
        help='The name of the output CSV and txt files, e.g. results.csv, '
             'results.txt, or results'
    )
    arg.add_argument(
        '-F', '--output_format',
        default=config['output']['format'],
        choices=['csv', 'json', 'yaml', 'txt', 'all'],
        dest='output_format',
        help='The format (extension) of the output file\nPossible options: '
             '"csv", "json", "yaml", "txt", or "all"'
    )
    arg.add_argument(
        '-v', '--verbose',
        default=config['verbosity'],
        action='count',
        dest='verbosity',
        help='Set the verbosity; a number between 1 and 5.'
    )
    arg.add_argument(
        '--version',
        action='version',
        version=setup_args['version'],
        help='Get the version of the app.'
    )
    
    args = arg.parse_args()

    # get the list of domains from the input
    if not (args.domain or args.input):
        printer(f'\n ■ {Fore.MAGENTA}No domain is given to be evaluated! '
                f'Consider using the argument "-h" or "--help" to get '
                f'instructions.\n{Style.RESET_ALL}')
        arg.print_help()
        exit()
    else:
        if (args.domain):
            domains = args.domain.split(',')
        else:
            domains = open(args.input, 'r').read().splitlines()
    
    # get the whois API
    whois_api = str(args.whois_api).lower() 
    if whois_api not in ['whoisxml', 'whoxy']:
        printer(f' ■ {Fore.MAGENTA}The API is not properly used: {whois_api}. '
                f'It will be ignored and "whoisxml" will be applied.'
                f'{Style.RESET_ALL}')
    
    # get the scan type
    scan_type = str(args.scan_type).lower() 
    if (scan_type not in ['deep', 'quick']):
        printer(f' ■ {Fore.MAGENTA}The scan type is not properly used: '
                f'{scan_type}. It will be ignored and the value of the config '
                f'file will be used.{Style.RESET_ALL}')
    
    # get the output file name
    output = args.output
    if output:
        output = output.replace('.txt', '').replace('.csv', '')
        output = output.replace('.yaml', '').replace('.json', '')
    else:
        printer(f' ■ {Fore.MAGENTA}The the output file name is not properly '
        f'used: {output}. It will be ignored and the value of the config '
        f'file will be used.{Style.RESET_ALL}')
    
    # get the output file format (extension)
    output_format = str(args.output_format).lower()
    if output_format not in ['txt', 'json', 'yaml', 'csv', 'all']:
        printer(f' ■ {Fore.MAGENTA}The the output file format (extension) is '
        f'not properly used: {output_format}. It will be ignored and the value '
        f'of the config file will be used.{Style.RESET_ALL}')
    if output_format == 'all':
        output_format = ['txt', 'json', 'yaml', 'csv']

    # get the verbosity
    if not args.verbosity in range (1, 5):
        verbosity = config['verbosity']
    else:
        verbosity = args.verbosity

    # print the logo
    printer(Fore.GREEN + logo + Style.RESET_ALL)

    # print the parsed arguments
    printer(' Arguments Used in this Scan:')
    for arg, value in vars(args).items():
        printer(f'  ✸ {Fore.GREEN}{arg:15}: {Fore.WHITE}{value}{Style.RESET_ALL}')
    printer('----------------------------------------------------\n\n')

    # get the start time of the scan
    start_time = datetime.now()

    # iterate over domains to get the data and write the result
    i = 1
    for dom in domains:
        # get the start time of the single scan
        start_time_d = datetime.now()

        # print the name of the domain
        printer(f'\n [{Fore.GREEN}+{Style.RESET_ALL}]──┬──{Fore.RED}{Back.WHITE}'
                f' {dom} {Style.RESET_ALL}{Fore.GREEN}'
                f' ({i}/{len(domains)} - {str(round(i/len(domains) * 100))}%)'
                f'{Fore.CYAN}  [{start_time.strftime(config["date_format"])}]'
                f'{Style.RESET_ALL}\n      │')
        
        # sanitize the domain name
        d = domain_sanitizer(dom)
        
        # if domain format is not correct
        if not d:
            printer(f'      ├─── ■■ ERROR: {Fore.RED}The domain "{dom}" is not' 
                    f'formatted properly; it will be ignored. Check if it is '
                    f'written correctly.{Style.RESET_ALL}')
            d = dom
        else:
            if d != dom:
                printer(f'      ├─── {Fore.YELLOW}The sanitized domain is: ' 
                        f'Fore.GREEN{d}{Style.RESET_ALL}\n      │')
            
            # check if the domain is already analyzed
            if d in analyzed_domains:
                printer(f'      ├─── {Fore.YELLOW}The domain {d} is already '
                        f'analyzed. It will be ignored.'
                        f'{Style.RESET_ALL}\n      │')
            else:
                analyzed_domains.add(d)

            # get the data by calling relevant functions
            verbosity = 2
            json_result[d] = {}
            json_result[d]['http'] = site_status(d)
            # json_result[d]['dns_records'], \
            # json_result[d]['subdomain'] = resolve_dns(d)
            # json_result[d]['whois'] = whois(d, whois_api)
            # json_result[d]['ssl'] = ssl_parser(d)
            # json_result[d]['subdomain'], \
            # json_result[d]['related_domain'] = subdomain_finder(d, scan_type, set(json_result[d]['subdomain']))

        # get the end time and delta of the single scan
        end_time_d = datetime.now()
        delta_d = end_time_d - start_time_d
        delta_all = end_time_d - start_time

        # print a message shows the scan for the domain is finished
        printer(f'      │\n      └───{Fore.RED}{Back.WHITE} THE END  ({d}) '
                f'{Style.RESET_ALL}{Fore.CYAN}  Finished in {delta_d} '
                f'(total time: {delta_all}){Style.RESET_ALL}\n')

        i += 1
        # add a delay between investigating domains
        # if i-1 < len(domains):
        #     sleep(config['delay']['domain'])

    # write the results into a TXT, CSV, and JSON files
    # tags format: [ssl, whois, http, dns, related_sub_domains]
    tags = [0, 0, 1, 0, 0]
    if 'csv' in output_format:
        csv_writer(output + '.csv', json_result, tags)
    # if 'json' in output_format:
    #     json_writer(output + '.json', json_result)
    if 'txt' in output_format:
        txt_writer(output + '.txt')
