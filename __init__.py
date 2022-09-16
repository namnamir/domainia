#!/usr/bin/env python
import csv
import argparse
from colorama import init, Fore, Back, Style
from config import config
from modules.whois import whois
from modules.basic_status import site_status
from modules.ssl_parser import ssl_parser
from modules.dns_records import dns_resolver


if __name__ == '__main__':
    logo = """        
           ▄▄▄        ▄███▄
           ███▌      ▄█████
              '▄█████▄
               ███████
               ▀██████ ▄▄▄▄▄
 ___           ▄▄▀▀▀   ██████▌
(  _`\       ████      ▐█████    _         _   
| | ) |   _  ████__ ___     _ _ (_)  ___  (_)   _ _ 
| | | ) /'_`\ /' _ ` _ `\ /'_` )| |/' _ `\| | /'_` )
| |_) |( (_) )| ( ) ( ) |( (_| || || ( ) || |( (_| |
(____/'`\___/'(_) (_) (_)`\__,_)(_)(_) (_)(_)`\__,_)
----------------------------------------------------
            AN OSINT TOOL FOR DOMAINS
----------------------------------------------------
Version: 2.0
Source: https://github.com/namnamir/domainia

"""
    json_result = {}

    # initiating Colorama
    init()

    # initiate the argument
    arg = argparse.ArgumentParser('Get the public information of a domain')
    arg.add_argument('-f', '--file', help='Path to the list of domain names, e.g. domains.txt')
    arg.add_argument('-d', '--domain', help='The comma separated list of domains')
    arg.add_argument('-w', '--whois', help='Whois API; default "whoisxml".\nPossible options: "whoisxml" and "whoxy"')
    arg.add_argument('-t', '--type', help='Type of the scan. If it is set, it will ignore the config file value for the scan type.\nPossible options: "quick" and "deep"')
    arg.add_argument('-o', '--output', help='The name of the output CSV file, e.g. results.csv')
    args = arg.parse_args()

    if not (args.domain or args.file):
        print('\r\n ■ ' + Fore.RED + 'No domain is given to be evaluated! Consider using the argument "-h" or "--help" to get instructions.\r\n' + Style.RESET_ALL)
        arg.print_help()
        exit()
    # get the list of domains from the input
    domains = args.domain.split(',') if (args.domain) else open(args.file, 'r').read().splitlines()
    # get the whois API
    whois_api = str(args.whois).lower() 
    if (whois_api not in ['whoisxml', 'whoxy']):
        print(' ■ ' + Fore.RED + 'The API is not properly used: {0}. It will be ignored and "whoisxml" will be applied.'.format(whois_api) + Style.RESET_ALL)
        whois_api = 'whoisxml'
    # get the scan type
    scan_type = str(args.whois).lower() 
    if (scan_type not in ['deep', 'quick']):
        print(' ■ ' + Fore.RED + 'The scan type is not properly used: {0}. It will be ignored and the value of the config file will be used.'.format(scan_type) + Style.RESET_ALL)
        scan_type = ''
    # get the output file name
    args.output = args.output if (args.output) else 'results.csv'

    # write the result in the output file
    with open(args.output, mode='w', encoding='UTF8', newline='') as output_file:
        writer = csv.writer(output_file, delimiter=config['delimiter']['csv'], quoting=csv.QUOTE_MINIMAL)

        # formulate the header and write it into the CSV
        ssl_header = []
        if config['ssl']['issue_date']: ssl_header.append('ssl_issue_date')
        if config['ssl']['expiration_date']: ssl_header.append('ssl_expiration_date')
        if config['ssl']['signature']: ssl_header.append('ssl_signature')
        if config['ssl']['serial_number']: ssl_header.append('ssl_serial_number')
        if config['ssl']['issuer']['common_name']: ssl_header.append('ssl_issuer_common_name')
        if config['ssl']['issuer']['organization_name']: ssl_header.append('ssl_issuer_organization_name')
        if config['ssl']['issuer']['organization_unit_name']: ssl_header.append('ssl_issuer_organization_unit_name')
        if config['ssl']['issuer']['country']: ssl_header.append('ssl_issuer_country')
        if config['ssl']['subject']['common_name']: ssl_header.append('ssl_subject_common_name')
        if config['ssl']['subject']['organization_name']: ssl_header.append('ssl_subject_organization_name')
        if config['ssl']['subject']['locality_name']: ssl_header.append('ssl_subject_locality_name')
        if config['ssl']['subject']['country']: ssl_header.append('ssl_subject_country')
        whois_header = []
        if config['whois']['create_date']: whois_header.append('whois_register_date')
        if config['whois']['update_date']: whois_header.append('whois_update_date')
        if config['whois']['expiration_date']: whois_header.append('whois_expiration_date')
        if config['whois']['domain_age_days']: whois_header.append('whois_domain_age_in_days')
        if config['whois']['registrar']['name']: whois_header.append('whois_registrar_name')
        if config['whois']['registrar']['iana_id']: whois_header.append('whois_registrar_iana_id')
        if config['whois']['registrar']['website']: whois_header.append('whois_registrar_website')
        if config['whois']['registrar']['whois_server']: whois_header.append('whois_registrar_whois_server')
        if config['whois']['registrar']['email']: whois_header.append('whois_registrar_email')
        if config['whois']['registrar']['phone']: whois_header.append('whois_registrar_phone')
        if config['whois']['registrant']['name']: whois_header.append('whois_registrant_name')
        if config['whois']['registrant']['country']: whois_header.append('whois_registrant_country')
        if config['whois']['registrant']['email']: whois_header.append('whois_registrant_email')
        if config['whois']['registrant']['phone']: whois_header.append('whois_registrant_phone')
        if config['whois']['administrative']['name']: whois_header.append('whois_administrative_name')
        if config['whois']['administrative']['country']: whois_header.append('whois_administrative_country')
        if config['whois']['administrative']['email']: whois_header.append('whois_administrative_email')
        if config['whois']['administrative']['phone']: whois_header.append('whois_administrative_phone')
        if config['whois']['technical']['name']: whois_header.append('whois_technical_name')
        if config['whois']['technical']['country']: whois_header.append('whois_technical_country')
        if config['whois']['technical']['email']: whois_header.append('whois_technical_email')
        if config['whois']['technical']['phone']: whois_header.append('whois_technical_phone')
        if config['whois']['name_servers']: whois_header.append('whois_name_servers')
        
        header = ['domain', 'subdomain', 'related domain'] + \
                 ssl_header + \
                 config['dns_records'].copy() + \
                 whois_header + \
                 ['site_title', 'HTTP_status']
        writer.writerow(header)

        # print the header
        print(Fore.GREEN + logo + Style.RESET_ALL)

        # iterate over domains to get the data and write the result
        i = 1
        for d in domains:
            # print the name of the domain
            print('\r\n [' + Fore.GREEN + '+' + Fore.WHITE + ']──┬──' + \
                  Fore.RED + Back.WHITE +  ' {0} '.format(d) + Style.RESET_ALL + Fore.GREEN + \
                  ' ({0}/{1} - {2}%)'.format(i, len(domains), str(round(i/len(domains) * 100))) + \
                  Style.RESET_ALL + '\r\n      │')

            # get the data by calling relevant functions
            json_result[d] = {}
            json_result[d]['general'] = site_status(d)
            json_result[d]['dns_records'] = dns_resolver(d.replace(' ', ''))
            json_result[d]['whois'] = whois(d, whois_api)
            json_result[d]['ssl'], json_result[d]['subdomain'], json_result[d]['related_domain'] = ssl_parser(d, scan_type)

            # compose the line
            line = []
            line.append(d)
            line.append(config['delimiter']['subdomain'].join(json_result[d]['subdomain']))
            line.append(config['delimiter']['related_domain'].join(json_result[d]['related_domain']))
            # append data retrieved from SSL certificate to the line
            if config['ssl']['issue_date']:
                line.append(json_result[d]['ssl']['issue_date'])
            if config['ssl']['expiration_date']:
                line.append(json_result[d]['ssl']['expiration_date'])
            if config['ssl']['signature']:
                line.append(json_result[d]['ssl']['signature'])
            if config['ssl']['serial_number']:
                line.append(json_result[d]['ssl']['serial_number'])
            if config['ssl']['issuer']['common_name']:
                line.append(json_result[d]['ssl']['issuer']['common_name'])
            if config['ssl']['issuer']['organization_name']:
                line.append(json_result[d]['ssl']['issuer']['organization_name'])
            if config['ssl']['issuer']['organization_unit_name']:
                line.append(json_result[d]['ssl']['issuer']['organization_unit_name'])
            if config['ssl']['issuer']['country']:
                line.append(json_result[d]['ssl']['issuer']['country'])
            if config['ssl']['subject']['common_name']:
                line.append(json_result[d]['ssl']['subject']['common_name'])
            if config['ssl']['subject']['organization_name']:
                line.append(json_result[d]['ssl']['subject']['organization_name'])
            if config['ssl']['subject']['locality_name']:
                line.append(json_result[d]['ssl']['subject']['locality_name'])
            if config['ssl']['subject']['country']:
                line.append(json_result[d]['ssl']['subject']['country'])
            # append DNS records to the line
            for r in config['dns_records']:
                line.append(config['delimiter']['dns_records'].join(json_result[d]['dns_records'][r]))
            # append the whois results to the line
            if config['whois']['create_date']:
                line.append(json_result[d]['whois']['create_date'])
            if config['whois']['update_date']:
                line.append(json_result[d]['whois']['update_date'])
            if config['whois']['expiration_date']:
                line.append(json_result[d]['whois']['expiration_date'])
            if config['whois']['domain_age_days']:
                line.append(json_result[d]['whois']['domain_age_days'])
            if config['whois']['registrar']['name']:
                line.append(json_result[d]['whois']['registrar']['name'].replace(config['delimiter']['nameserver'], ' '))
            if config['whois']['registrar']['iana_id']:
                line.append(json_result[d]['whois']['registrar']['iana_id'])
            if config['whois']['registrar']['website']:
                line.append(json_result[d]['whois']['registrar']['website'])
            if config['whois']['registrar']['whois_server']:
                line.append(json_result[d]['whois']['registrar']['whois_server'])
            if config['whois']['registrar']['email']:
                line.append(json_result[d]['whois']['registrar']['email'])
            if config['whois']['registrar']['phone']:
                line.append(json_result[d]['whois']['registrar']['phone'])
            if config['whois']['registrant']['name']:
                line.append(json_result[d]['whois']['registrant']['name'].replace(config['delimiter']['nameserver'], ' '))
            if config['whois']['registrant']['country']:
                line.append(json_result[d]['whois']['registrant']['country'])
            if config['whois']['registrant']['email']:
                line.append(json_result[d]['whois']['registrant']['email'])
            if config['whois']['registrant']['phone']:
                line.append(json_result[d]['whois']['registrant']['phone'])
            if config['whois']['administrative']['name']:
                line.append(json_result[d]['whois']['administrative']['name'].replace(config['delimiter']['nameserver'], ' '))
            if config['whois']['administrative']['country']:
                line.append(json_result[d]['whois']['administrative']['country'])
            if config['whois']['administrative']['email']:
                line.append(json_result[d]['whois']['administrative']['email'])
            if config['whois']['administrative']['phone']:
                line.append(json_result[d]['whois']['administrative']['phone'])
            if config['whois']['technical']['name']:
                line.append(json_result[d]['whois']['technical']['name'].replace(config['delimiter']['nameserver'], ' '))
            if config['whois']['technical']['country']:
                line.append(json_result[d]['whois']['technical']['country'])
            if config['whois']['technical']['email']:
                line.append(json_result[d]['whois']['technical']['email'])
            if config['whois']['technical']['phone']:
                line.append(json_result[d]['whois']['technical']['phone'])
            if config['whois']['technical']['phone']:
                line.append(config['delimiter']['nameserver'].join(json_result[d]['whois']['name_servers']))
            # append the HTML info to the line
            line += [json_result[d]['general']['site_title'], 
                     json_result[d]['general']['http_status'],
                     json_result[d]['general']['site_description'],
                     config['delimiter']['keyword'].join(json_result[d]['general']['site_keyword']),
                    ]

            # write the line into the CSV file
            writer.writerow(line)
            i += 1