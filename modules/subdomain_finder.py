#!/usr/bin/env python

from bs4 import BeautifulSoup
import random
import re
from colorama import Fore, Back, Style
from time import sleep

from config import config
from modules.utils import run_requests, printer


# find subdomains and related with different techniques
def subdomain_finder(domain, scan_type, existing_subdomains):
    subdomains = set()
    related_domains = set()

    # set the print arguments for the function "run_requests"
    print_args = [True, '      │        ├──■ ', '      │        │  ■■ ']

    # update the list with existing subdomains
    subdomains.update(existing_subdomains)


    # call the Hacker Target API and parse data
    def hacker_target(domain):
        subdomains = set()

        # print the subtitle: Hacker Target
        printer('      │        ├□ ' + Fore.GREEN + 
              'Hacker Target API is calling' + Style.RESET_ALL)

        # download the result page of Hacker Target
        url = config['api']['hacker_target']['url_hosts'].format(domain)
        text_data = run_requests(url, '', 'text', 'Hacker Target API', print_args)[0]
        text_data = text_data.split('\n')

        # continue only if there is any data for it
        if text_data:
            # iterate over the found alternative names
            for d in text_data:
                d = d.split(',')[0]
                # ignore the main domain
                if (d != domain):
                    # find subdomains
                    if d.endswith(domain):
                        sd = d.split('.' + domain)[0]
                        subdomains.add(sd)
        return subdomains
    

    # call the Security Trails API and parse data
    def security_trails(domain):
        subdomains = set()

        # print the subtitle: crt.sh
        printer('      │        ├□ ' + Fore.GREEN + 
              'Security Trails API is calling' + Style.RESET_ALL)

        # check if the whois API key is set
        if config['api']['security_trails']['api_key'] == '':
            printer('      │        ├──■ ' + Fore.RED + 
                  'Security Trails API key is not set. Do it in the "config.py" file.' + 
                  Style.RESET_ALL)
            return subdomains
        else:
            # download the result page of Security Trials
            url = config['api']['security_trails']['url_subdomain'].format(domain)
            api_key = config['api']['security_trails']['api_key']
            headers = {'APIKEY': api_key}
            result = run_requests(url, headers, 'json', 'Security Trails API', print_args)[0]
            subdomains = set(result['subdomains'])

        return subdomains


    # scrap the CRT.sh for certificates and parse them
    def crt_sh(domain, scan_type):
        subdomains = set()
        related_domains = set()
        alt_names = set()

        # get the type of the scan; quick or deep
        # if it is defined by STDIN, the setting from the config file will be ignored
        if scan_type == '':
            scan_type = config['scan_type']['ssl']
        
        # print the subtitle: crt.sh
        printer('      │        ├□ ' + Fore.GREEN + 
              'crt.sh SSL load is running (Scan type: "{0}")'.format(scan_type) + 
              Style.RESET_ALL)

        # download the certificate page on CRT
        url = config['api']['crt_sh']['url_all'].format(domain)
        json_data = run_requests(url, '', 'json', 'CRT.sh All Certs API', print_args)[0]

        # continue only if there is any data for it
        if json_data:
            json_data = sorted(json_data, key=lambda k: k['id'], reverse=True)

            # iterate over each issued certificate (cert history)
            for i in range(0, len(json_data)):
                # if it is a quick search, ignore loading each certificate
                if (scan_type == "quick") and (i > 0):
                    break
                url = config['api']['crt_sh']['url_single'].format(json_data[i]['id'])
                cert = run_requests(url, '', 'text', 'CRT.sh Single Cert API', print_args)[0]
                # fix the HTML format of the space
                cert = (cert.text).replace('&nbsp;', ' ')

                if scan_type == 'deep':
                    # print the progress
                    printer('      │      ■■■■  ' + Fore.GREEN + 
                          '{0} cert(s) out of {1} certificates is loaded '.format(i+1, len(json_data)) + Fore.CYAN + 
                          '({0}%)'.format(str(round((i+1)/len(json_data) * 100))) + Fore.WHITE + ' ■■■■' + Style.RESET_ALL)

                # aggregate all alternative names
                alt_names.update(re.findall(r"DNS:(.*?)<BR>", cert))

                # add a delay between downloading SSL certificates
                sleep(config['delay']['ssl'])

            # if it is a quick search
            if scan_type == 'quick':
                # iterate over the found results
                for (key, value) in enumerate(json_data):
                    # aggregate all alternative names
                    alt_names.update(value['name_value'].split('\n'))

            # iterate over the found alternative names
            for d in alt_names:
                # ignore the main domain
                if (d != domain):
                    if d.startswith('*.'):
                        d = d.split('*.')[1]
                    # find subdomains
                    if d.endswith(domain):
                        d = d.split('.' + domain)[0]
                        subdomains.add(d)
                    # find related domains (not subdomain)
                    else:
                        related_domains.add(d)

        return [subdomains, related_domains]


    # scrap the SSL Mate for certificates and parse them
    def ssl_mate(domain):
        subdomains = set()
        related_domains = set()
        alt_names = set()

        # print the subtitle: SSL Mate
        printer('      │        └□ ' + Fore.GREEN + 'SSL Mate API is running' + Style.RESET_ALL)

        # download the certificate page
        url = config['api']['ssl_mate']['url_all'].format(domain)
        json_data = run_requests(url, '', 'json', 'SSL Mate API', print_args)[0]

        # continue only if there is any data for it
        if json_data:
            # iterate over each issued certificate (cert history)
            for cert in json_data:
                # aggregate all alternative names
                alt_names.update(set(cert['dns_names']))

            # iterate over the found alternative names
            for d in alt_names:
                # ignore the main domain
                if (d != domain):
                    if d.startswith('*.'):
                        d = d.split('*.')[1]
                    # find subdomains
                    if d.endswith(domain):
                        d = d.split('.' + domain)[0]
                        subdomains.add(d)
                    # find related domains (not subdomain)
                    else:
                        related_domains.add(d)

        return [subdomains, related_domains]


    # scrap the Domain History for subdomains and parse them
    def dns_history(domain):
        subdomains = set()

        # print the subtitle: DNS History
        printer('      │        ├□ ' + Fore.GREEN + 'DNS History API is running' + Style.RESET_ALL)

        # download the DNS History page related to subdomains
        url = config['api']['dns_history']['url_subdomain'].format(domain)
        text_data = run_requests(url, '', 'text', 'DNS History API', print_args)[0]

        items = BeautifulSoup(text_data, "html.parser").find('div', {'id': 'mainarea'}).find_all('div', {'class': 'clearfix'})[1].find_all('a')

        # continue only if there is any data for it
        if items:
            # iterate over each subdomains
            for item in items:
                # aggregate all found subdomains
                subdomains.add(item.string.split('.' + domain)[0])

        return subdomains


    # get subdomains and related domains
    sub_sm, rel_sm, sub_cr, rel_cr, sub_ht ,sub_st, sub_dh = '', '', '', '', '', '', ''

    sub_ht = hacker_target(domain)
    sub_st = security_trails(domain)
    sub_dh = dns_history(domain)
    sub_cr, rel_cr = crt_sh(domain, scan_type)
    sub_sm, rel_sm = ssl_mate(domain)

    # join results
    subdomains = sub_ht.union(sub_st)
    subdomains.update(sub_cr)
    subdomains.update(sub_sm)
    subdomains.update(sub_dh)
    related_domains = rel_sm.union(rel_cr)

    # remove the domain from the set
    if subdomains and (domain in subdomains):
        subdomains.remove(domain)

    # print the title: Subdomains
    printer('      │\n      ├───' + Fore.BLACK + Back.WHITE + ' Subdomains (total: {0}) '.format(len(subdomains)) + Style.RESET_ALL)

    # print out found subdomains
    if subdomains:
        for subdomain in subdomains:
            printer('      │      ■ ' + Fore.YELLOW + subdomain + Style.RESET_ALL)
    else:
        printer('      │      ■■ ' + Fore.RED + 'No subdomain is found for "{0}".'.format(domain) + Style.RESET_ALL)

    # print the title: Related Domains
    printer('      │\n      ├───' + Fore.BLACK + Back.WHITE + ' Related Domains (total: {0}) '.format(len(related_domains)) + Style.RESET_ALL)

    # print out found related domains
    if related_domains:
        for rd in related_domains:
            printer('      │      ■ ' + Fore.YELLOW + rd + Style.RESET_ALL)
    else:
        printer('      │      ■■ ' + Fore.RED + 'No related domain is found.' + Style.RESET_ALL)

    # return the result in the format of list instead of set
    return [
        sorted(subdomains),
        sorted(related_domains)
    ]
