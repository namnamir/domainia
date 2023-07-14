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
from modules.utilities.url_sanitizer import url_sanitizer
from modules.utilities.load_sitemap import load_sitemap
from modules.utilities.printer import printer
from modules.output_writer import output_writer


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
    # initiating Colorama
    init()

    # a variable to store data of all URNs
    urns_data = []

    # a set to maintain the list of the analyzed domains
    # it would prevent repetition
    analyzed_domains = set()

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
        '-s', '--sitemap',
        action="store_true",
        dest='sitemap',
        help='Scan all internal links via loading sitemap?'
    )
    arg.add_argument(
        '-D', '--delay',
        default=config['delay']['domain'],
        type=int,
        dest='delay',
        help='Add a delay between scanning domains in seconds.'
    )
    arg.add_argument(
        '-F', '--output_format',
        default=config['output']['format'],
        choices=['csv', 'json', 'yaml', 'txt', 'all',
                 'json_beautiful', 'json_b', 'b_json', 'beautiful_json'],
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
            domains = open(args.input, 'r', encoding='UTF8').read().splitlines()

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
    output_name = args.output
    if output_name:
        output_name = output_name.replace('.txt', '').replace('.csv', '')
        output_name = output_name.replace('.yaml', '').replace('.json', '')
    else:
        printer(f' ■ {Fore.MAGENTA}The the output file name is not properly '
                f'used: {output_name}. It will be ignored and the value of the config '
                f'file will be used.{Style.RESET_ALL}')

    # get the sitemap argument; if used, it will download all links provided in the sitemap
    sitemap = args.sitemap

    # get delays between scanning domains; it gos for the absolute value to avoid issues
    delay = abs(args.delay)

    # get the output file format (extension)
    output_format = str(args.output_format).strip().lower()
    if output_format not in ['txt', 'json', 'yaml', 'csv', 'all',
                             'json_beautiful', 'json_b', 'b_json', 'beautiful_json']:
        printer(f' ■ {Fore.MAGENTA}The the output file format (extension) is '
                f'not properly used: {output_format}. It will be ignored and the value '
                f'of the config file will be used.{Style.RESET_ALL}')
    if output_format == 'all':
        output_format = ['txt', 'json', 'yaml', 'csv']
    else:
        output_format = output_format.split(",")

    # get the verbosity
    if args.verbosity not in range(1, 5):
        verbosity = config['verbosity']
    else:
        verbosity = args.verbosity

    # print the logo
    printer(Fore.GREEN + logo + Style.RESET_ALL)

    # print the parsed arguments
    printer(' Arguments Used in this Scan:\n')
    for arg, value in vars(args).items():
        printer(f'  ✸ {Fore.GREEN}{arg:17}: {Fore.WHITE}{value}{Style.RESET_ALL}')
    printer('----------------------------------------------------\n\n')

    # get the start time of the scan
    start_time = datetime.now()

    # iterate over domains to get the data and write the result
    i = 1

    for init_domain in domains:
        # get the start time of the single domain
        start_time_domain = datetime.now()

        #################################################
        init_domain = init_domain.split(',')
        print(init_domain)
        city = init_domain[0]
        state = init_domain[1]
        init_domain = init_domain[2]
        #################################################

        # print the name of the domain
        printer(f'\n [{Fore.GREEN}+{Style.RESET_ALL}]──┬──{Fore.RED}{Back.WHITE}'
                f' {init_domain} {Style.RESET_ALL}{Fore.GREEN}'
                f' ({i}/{len(domains)} - {str(round(i/len(domains) * 100))}%)'
                f'{Fore.CYAN}  [{start_time.strftime(config["date_format"])}]'
                f'{Style.RESET_ALL}')

        # sanitize the domain name
        domain = url_sanitizer(init_domain)[1]

        # check if it should check all pages (via sitemap) or just the homepage
        if sitemap:
            printer(f'      │        ├□ {Fore.GREEN}Sitemap of {domain} is loading{Style.RESET_ALL}\n      │')
            pages = load_sitemap(domain)
            printer(f'      │        └□ {Fore.GREEN}{len(pages) - 1} pages retrieved.{Style.RESET_ALL}\n      │')
        else:
            printer('      │')
            pages = [domain] if domain else []

        # iterate over
        j = 1
        for init_page in pages:
            # get the start time of the single page (scan)
            start_time_page = datetime.now()
            # a temporary dictionary to save the data of the domain and its internal pages
            page_data = {}
            hostname = None

            # sanitize the domain name
            page = url_sanitizer(init_page)[2]

            # if the sitemap is activated (internal pages get scanned)
            if domain != page:
                printer(f'      │\n      ├──{Fore.BLACK}{Back.YELLOW} ➜ {Style.RESET_ALL}'
                        f'{Fore.WHITE} {page} {Fore.GREEN}(Pages: {j}/{len(pages)} '
                        f'- {str(round(j/len(pages) * 100))}% | Domains: '
                        f'{i}/{len(domains)}){Fore.CYAN}  '
                        f'[{start_time.strftime(config["date_format"])}]'
                        f'{Style.RESET_ALL}\n      │')
                hostname = domain

            # if domain format is not correct
            if not page:
                printer(f'      ├─── ■■ ERROR: {Fore.RED}The URN "{page}" is not '
                        f'formatted properly; it will be ignored. Check if it is '
                        f'written correctly.{Style.RESET_ALL}')
                page = init_page
            else:
                if page != init_page:
                    printer(f'      ├─── {Fore.YELLOW}The sanitized URN is: '
                            f'{Fore.GREEN}{page}{Style.RESET_ALL}\n      │')

                # check if the domain is already analyzed
                if page in analyzed_domains:
                    printer(f'      ├─── {Fore.YELLOW}The URN {page} is already '
                            f'analyzed. It will be ignored.{Style.RESET_ALL}\n      │')
                else:
                    analyzed_domains.add(page)

                #################################################
                page_data['city'] = city
                page_data['state'] = state
                page_data['country'] = 'NL'
                #################################################
                # get the data by calling relevant functions
                page_data['urn'] = "http://" + page
                page_data['hostname'] = hostname

                # start the scan based on the user's request
                if config['scan_type']['tags'][0]:
                    page_data['http'] = site_status(page)
                # if config['scan_type']['tags'][1]:
                #     page_data['dns_records'], page_data['subdomain'] = resolve_dns(domain)
                # if config['scan_type']['tags'][2]:
                #     page_data['whois'] = whois(d, whois_api)
                # if config['scan_type']['tags'][3]:
                #     page_data['ssl'] = ssl_parser(domain)
                # if config['scan_type']['tags'][4]:
                #     page_data['subdomain'], \
                #         page_data['related_domain'] = subdomain_finder(domain, scan_type,
                #                                                                   set(page_data['subdomain']))

                # add the data of the single domain to the list of all URNs
                urns_data.append(page_data)

            # get the end time and delta of the single scan
            delta_page = datetime.now() - start_time_page
            delta_domain = datetime.now() - start_time_domain
            delta_all = datetime.now() - start_time

            # add the elapsed time of each page
            page_data['elapsed_time'] = str(delta_page)

            # print a message shows the scan for the domain is finished
            if j >= len(pages):
                printer(f'      │\n      └───{Fore.RED}{Back.WHITE} THE END  ({domain}) '
                        f'{Style.RESET_ALL}{Fore.CYAN}  Finished in {delta_domain} '
                        f'(total time: {delta_all}){Style.RESET_ALL}\n')
            else:
                printer(f'      │\n      └──{Fore.BLACK}{Back.YELLOW} ✔ {Style.RESET_ALL}'
                        f'{Fore.WHITE} {page} {Fore.CYAN} Finished in {delta_page} '
                        f'(total time: {delta_all}){Style.RESET_ALL}')

            # increment the domains counter
            j += 1

            # add a delay between scans
            if j - 1 < len(pages):
                sleep(delay)

        # increment the domains counter
        i += 1

    # write the results into a TXT, CSV, and JSON files
    output_writer(output_name, output_format, urns_data)
