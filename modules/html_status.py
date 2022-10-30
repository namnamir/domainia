#!/usr/bin/env python

import re
from colorama import Fore, Back, Style
from modules.dnsbl import dsn_blocklist
from modules.utils import dns_resolver, run_requests, printer

# get the basic site status
def site_status(domain):
    results = {}

    # print the title of the section
    printer('      ├───' +  Fore.BLACK + Back.WHITE + ' General Info ' + Style.RESET_ALL)
    # set the print arguments for the function "run_requests"
    print_args = [True, '      │      ■ ', '      │      ■■ ']

    # open the domain
    try:
        text_data, status_code, history, headers = run_requests('http://' + domain, '', 'http', 'General Site Status', print_args)
        if status_code != 200:
            printer('      │      ' + Fore.RED + '■ Could not parse the HTML page.' + Style.RESET_ALL)
            printer('      │      ■■ Content:     ' + Fore.YELLOW + text_data + Style.RESET_ALL)
            printer('      │      ■■ Status Code: ' + Fore.YELLOW + status_code + Style.RESET_ALL)
            printer('      │      ■■ History:     ' + Fore.YELLOW + history + Style.RESET_ALL)
            printer('      │      ■■ Headers:     ' + Fore.YELLOW + headers + Style.RESET_ALL)
            return results
    except:
        return results

    # get redirects
    redirect = ''
    if history:
        redirect = domain
        for step in history:
            redirect += ' → ' + step.url
    
    # parse the data and write into a dict variable
    text_data = text_data.text
    results = {
        'title': ''.join(re.findall('<title>(.*?)</title>', text_data, re.IGNORECASE)),
        'google_ua': ''.join(re.findall('[\s"\']+(UA-[\d\-]*)["|\'\s]+', text_data, re.IGNORECASE)),
        'status_code': str(status_code),
        'redirect': redirect,
        'meta': {
            'description': ''.join(re.findall('<meta\s*name\s*=[\s"\']+description[\s"\']+content\s*=[\s"\']*(.*?)["|\'\s]*>', text_data, re.IGNORECASE)),
            'keywords': ''.join(re.findall('<meta\s*name\s*=[\s"\']+keywords[\s"\']+content\s*=[\s"\']*(.*?)["|\'\s]*>', text_data, re.IGNORECASE)),
            'robots': ''.join(re.findall('<meta\s*name\s*=[\s"\']+robots[\s"\']+content\s*=[\s"\']*(.*?)["|\'\s]*>', text_data, re.IGNORECASE)),
            'twitter_site': ''.join(re.findall('<meta\s*property\s*=[\s"\']+twitter:site[\s"\']+content\s*=[\s"\']*(.*?)["|\'\s]*>', text_data, re.IGNORECASE)),
            'twitter_author': ''.join(re.findall('<meta\s*property\s*=[\s"\']+twitter:creator[\s"\']+content\s*=[\s"\']*(.*?)["|\'\s]*>', text_data, re.IGNORECASE)),
            'facebook_site': ''.join(re.findall('<meta\s*property\s*=[\s"\']+article:publisher[\s"\']+content\s*=[\s"\']*(.*?)["|\'\s]*>', text_data, re.IGNORECASE)),
            'facebook_author': ''.join(re.findall('<meta\s*property\s*=[\s"\']+article:author[\s"\']+content\s*=[\s"\']*(.*?)["|\'\s]*>', text_data, re.IGNORECASE)),
            'canonical': ''.join(re.findall('<meta\s*rel\s*=[\s"\']+canonical[\s"\']+href\s*=[\s"\']*(.*?)["|\'\s]*>', text_data, re.IGNORECASE)),
        },
    }
    # get the blocklisted IPs and domain name
    try:
        results['blocked_domain'] = dsn_blocklist(domain, 'domain')
        results['blocked_ip'] = dsn_blocklist(dns_resolver(domain, 'A', print_args), 'ipv4') + \
                                dsn_blocklist(dns_resolver(domain, 'AAAA', print_args), 'ipv6')
    except:
        pass
    
    # print the result on STDOUT
    if results['status_code']:
        printer('      │      ■ HTTP Status:         ' + Fore.YELLOW + results['status_code'] + Style.RESET_ALL)
    if results['redirect']:
        printer('      │      ■ HTTP Redirects:      ' + Fore.YELLOW + results['redirect'] + Style.RESET_ALL)
    if results['title']:
        printer('      │      ■ Site Title:          ' + Fore.YELLOW + results['title'] + Style.RESET_ALL)
    if results['meta']['description']:
        printer('      │      ■ Site Description:    ' + Fore.YELLOW + results['meta']['description'] + Style.RESET_ALL)
    if results['meta']['keywords']:
        printer('      │      ■ Site Keywords:       ' + Fore.YELLOW + results['meta']['keywords'] + Style.RESET_ALL)
    if results['meta']['twitter_site']:
        printer('      │      ■ Twitter Account:     ' + Fore.YELLOW + results['meta']['twitter_site'] + Style.RESET_ALL)
    if results['meta']['twitter_author']:
        printer('      │      ■ Twitter Author:      ' + Fore.YELLOW + results['meta']['twitter_author'] + Style.RESET_ALL)
    if results['meta']['facebook_site']:
        printer('      │      ■ Facebook Account:    ' + Fore.YELLOW + results['meta']['facebook_site'] + Style.RESET_ALL)
    if results['meta']['facebook_author']:
        printer('      │      ■ Facebook Author:     ' + Fore.YELLOW + results['meta']['facebook_author'] + Style.RESET_ALL)
    if results['meta']['canonical']:
        printer('      │      ■ Canonical Link:      ' + Fore.YELLOW + results['meta']['canonical'] + Style.RESET_ALL)
    if results['google_ua']:
        printer('      │      ■ Google Analytics ID: ' + Fore.YELLOW + results['google_ua'] + Style.RESET_ALL)
    if results['blocked_domain']:
        printer('      │      ■ Domain Blocked:      ' + Fore.RED + ' / '.join(results['blocked_domain']) + Style.RESET_ALL)
    if results['blocked_ip']:
        printer('      │      ■ Site IP Blocked:     ' + Fore.RED + ' / '.join(results['blocked_ip']) + Style.RESET_ALL)

    # print HTTP header elements and add HTTP header of the page to the results
    results['headers'] = headers

    if results['headers']:
        printer('      │\n      ├───' +  Fore.BLACK + Back.WHITE + ' HTTP Headers ' + Style.RESET_ALL)

        for name, value in results['headers'].items():
            printer('      │      ■ {0}:  '.format(name) + Fore.YELLOW + value + Style.RESET_ALL)

    # return results
    return results
