#!/usr/bin/env python

import argparse
from datetime import datetime
from colorama import init, Fore, Back, Style
from time import sleep
from config import config

from setup import setup_args
from modules.whois import whois
from modules.html_status import site_status
from modules.ssl_parser import ssl_parser
from modules.dns_records import resolve_dns
from modules.subdomain_finder import subdomain_finder
from modules.utils import domain_sanitizer, printer
from modules.output_csv import csv_writer
from modules.output_json import json_writer
from modules.output_txt import txt_writer


if __name__ == '__main__':
    logo = """        
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
 Version: {0}
 Source:  {1}
 PyPI:    {2}
 By:      {3} ({4})
----------------------------------------------------

""".format(setup_args['version'], setup_args['url'], setup_args['download_url'], setup_args['author'], setup_args['author_email'])

    # a variable to store data in the JSON format
    json_result = {}

    # a set to maintain the list of the analyzed domains
    # it would prevent repetition
    analyzed_domains = set()

    # initiating Colorama
    init()

    # initiate the argument
    arg = argparse.ArgumentParser('Get the public information of a domain')
    arg.add_argument('-i', '--input', help='Path to the list of domain names, e.g. domains.txt. Each domain name should be in a line.')
    arg.add_argument('-d', '--domain', help='The comma separated list of domains')
    arg.add_argument('-w', '--whois', help='Whois API; default "whoisxml".\nPossible options: "whoisxml" and "whoxy"')
    arg.add_argument('-t', '--type', help='Type of the scan. If it is set, it will ignore the config file value for the scan type.\nPossible options: "quick" and "deep"')
    arg.add_argument('-o', '--output', help='The name of the output CSV and txt files, e.g. results.csv, results.txt, or results')
    arg.add_argument('-F', '--output_format', help='The format (extension) of the output file\nPossible options: "csv", "json", "txt", or "all"')
    arg.add_argument('-v', '--verbosity', help='Set the verbosity; a number between 1 and 5.')
    args = arg.parse_args()

    # get the list of domains from the input
    print(args)
    if not (args.domain or args.input):
        printer('\n ■ ' + Fore.MAGENTA + 'No domain is given to be evaluated! Consider using the argument "-h" or "--help" to get instructions.\n' + Style.RESET_ALL)
        arg.print_help()
        exit()
    else:
        domains = args.domain.split(',') if (args.domain) else open(args.input, 'r').read().splitlines()
    
    # get the whois API
    whois_api = str(args.whois).lower() 
    if whois_api not in ['whoisxml', 'whoxy']:
        printer(' ■ ' + Fore.MAGENTA + 'The API is not properly used: {0}. It will be ignored and "whoisxml" will be applied.'.format(whois_api) + Style.RESET_ALL)
        whois_api = 'whoisxml'
    
    # get the scan type
    scan_type = str(args.whois).lower() 
    if (scan_type not in ['deep', 'quick']):
        printer(' ■ ' + Fore.MAGENTA + 'The scan type is not properly used: {0}. It will be ignored and the value of the config file will be used.'.format(scan_type) + Style.RESET_ALL)
        scan_type = ''
    
    # get the output file name
    output = args.output
    if output:
        output = output.replace('.txt', '').replace('.csv', '').replace('.json', '')
    else:
        printer(' ■ ' + Fore.MAGENTA + 'The the output file name is not properly used: {0}. It will be ignored and the value of the config file will be used.'.format(output) + Style.RESET_ALL)
        output = config['output']['filename']
    
    # get the output file format (extension)
    output_format = str(args.output_format).lower()
    if output_format not in ['txt', 'json', 'csv', 'all']:
        printer(' ■ ' + Fore.MAGENTA + 'The the output file format (extension) is not properly used: {0}. It will be ignored and the value of the config file will be used.'.format(output_format) + Style.RESET_ALL)
        output_format = config['output']['format']
    if output_format == 'all':
        output_format = ['txt', 'json', 'csv']

    # get the verbosity
    if not args.verbosity in range (1, 5):
        verbosity = config['verbosity'] if (config['verbosity'] in range (1, 5)) else 1
    else:
        verbosity = args.verbosity

    # print the logo
    printer(Fore.GREEN + logo + Style.RESET_ALL)

    # iterate over domains to get the data and write the result
    i = 1
    for dom in domains:
        # get the start time of the scan
        start_time = datetime.now()

        # print the name of the domain
        printer('\n [' + Fore.GREEN + '+' + Fore.WHITE + ']──┬──' + 
                Fore.RED + Back.WHITE + ' {0} '.format(dom) + Style.RESET_ALL + Fore.GREEN + 
                ' ({0}/{1} - {2}%)'.format(i, len(domains), str(round(i/len(domains) * 100))) + 
                Fore.CYAN + '  [{0}]'.format(start_time.strftime(config['date_format'])) +
                Style.RESET_ALL + '\n      │')
        
        # sanitize the domain name
        d = domain_sanitizer(dom)
        
        # if domain format is not correct
        if not d:
            printer('      ├─── ■■ ERROR: ' + Fore.RED + 'The domain "{0}" is not formatted properly; it will be ignored. Check if it is written correctly.'.format(dom) + Style.RESET_ALL)
            d = dom
        else:
            if d != dom:
                printer('      ├─── ' + 'The sanitized domain is: ' + Fore.GREEN + d + Style.RESET_ALL + '\n      │')
            
            # check if the domain is already analyzed
            if d in analyzed_domains:
                printer('      ├─── ' + Fore.YELLOW + 'The domain {0} is already analyzed. It will be ignored.'.format(d) + Style.RESET_ALL + '\n      │')
            else:
                analyzed_domains.add(d)

            # get the data by calling relevant functions
            verbosity = 2
            json_result[d] = {}
            json_result[d]['http'] = site_status(d)
            json_result[d]['dns_records'], \
            json_result[d]['subdomain'] = resolve_dns(d)
            json_result[d]['whois'] = whois(d, whois_api)
            json_result[d]['ssl'] = ssl_parser(d)
            json_result[d]['subdomain'], \
            json_result[d]['related_domain'] = subdomain_finder(d, scan_type, set(json_result[d]['subdomain']))

        end_time = datetime.now()
        delta = end_time - start_time

        # print a message shows the scan for the domain is finished
        printer('      │\n      └───' + Fore.RED + Back.WHITE + ' THE END  ({0}) '.format(d) + 
            Style.RESET_ALL + Fore.CYAN + '  Finished in {0}'.format(delta) +
            Style.RESET_ALL + '\n')

        i += 1
        # add a delay between investigating domains
        if i-1 < len(domains):
            sleep(config['delay']['domain'])

    # write the results into a TXT, CSV, and JSON files
    if 'csv' in output_format:
        csv_writer(output + '.csv', json_result)
    # if 'json' in output_format:
    #     json_writer(output + '.json', json_result)
    if 'txt' in output_format:
        txt_writer(output + '.txt')
