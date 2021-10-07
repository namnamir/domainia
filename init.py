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
    json_result = {}

    # initiating Colorama
    init()
    
    # initiate the argumant
    arg = argparse.ArgumentParser('Get the public information of a domain')
    arg.add_argument('-f', '--file', help='Path to the list of domain names, e.g. domains.txt')
    arg.add_argument('-d', '--domain', help='The comma separated list of domains')
    arg.add_argument('-o', '--output', help='The name of the output CSV file, e.g. results.csv')
    args = arg.parse_args()

    # get the list of domains from the input
    domains = args.domain.split(',') if (args.domain) else open(args.file, 'r').read().splitlines()
    # get the output file name
    args.output = args.output if (args.output) else 'results.csv'
   
    # write the result in the output file
    with open(args.output, mode='w', encoding='UTF8', newline='') as output_file:
        writer = csv.writer(output_file, delimiter=config['delimiter']['csv'], quoting=csv.QUOTE_MINIMAL)
        
        # formulate the header and write it into the CSV
        header = ['domain', 'subdomain', 'related domain'] + \
                 ['ssl_issue_date', 'ssl_expriration_date', 'ssl_signature', 'ssl_serial_number',
                  'ssl_issuer_common_name', 'ssl_issuer_organization_name', 'ssl_issuer_organization_unit_name', 
                  'ssl_issuer_country', 'ssl_subject_common_name', 'ssl_subject_organization_name', 
                  'ssl_subject_locality_name', 'ssl_subject_country'] + \
                 config['records'].copy() + config['whois'].copy() + ['site_title', 'HTTP_status']
        writer.writerow(header)
        
        # iterate over domains to get the data and write the result
        i = 1
        for d in domains:
            # print the name of the domain
            print(Fore.WHITE + '\r\n [' + Fore.GREEN + '+' + Fore.WHITE + ']──┬──' + \
                  Fore.RED + Back.WHITE +  ' {0} '.format(d) + Style.RESET_ALL + Fore.GREEN + \
                  ' ({0}/{1} - {2}%)'.format(i, len(domains), str(round(i/len(domains) * 100))) + \
                  Style.RESET_ALL + '\r\n      │')
            
            # get the data by calling relevant functions
            json_result[d] = {}
            json_result[d]['general'] = site_status(d)
            json_result[d]['dns_records'] = dns_resolver(d.replace(' ', ''))
            json_result[d]['whois'] = whois(d)
            json_result[d]['ssl'], json_result[d]['subdomain'], json_result[d]['related_domain'] = ssl_parser(d)

            # compose the line
            line = []
            line.append(d)
            line.append(config['delimiter']['subdomain'].join(json_result[d]['subdomain']))
            line.append(config['delimiter']['related_domain'].join(json_result[d]['related_domain']))
            line.append(json_result[d]['ssl']['issue_date'])
            line.append(json_result[d]['ssl']['expriration_date'])
            line.append(json_result[d]['ssl']['signature'])
            line.append(json_result[d]['ssl']['serial_number'])
            line.append(json_result[d]['ssl']['issuer']['common_name'])
            line.append(json_result[d]['ssl']['issuer']['organization_name'])
            line.append(json_result[d]['ssl']['issuer']['organization_unit_name'])
            line.append(json_result[d]['ssl']['issuer']['country'])
            line.append(json_result[d]['ssl']['subject']['common_name'])
            line.append(json_result[d]['ssl']['subject']['organization_name'])
            line.append(json_result[d]['ssl']['subject']['locality_name'])
            line.append(json_result[d]['ssl']['subject']['country'])
            for r in config['records']:
                line.append(config['delimiter']['dns_records'].join(json_result[d]['dns_records'][r]))
            for w in config['whois']:
                line.append(json_result[d]['whois'][w])    
            line += [json_result[d]['general']['site_title'], json_result[d]['general']['HTTP_status']]

            # write the line into the CSV file
            writer.writerow(line)
            i += 1