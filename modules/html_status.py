#!/usr/bin/env python


"""

"""


from bs4 import BeautifulSoup
from colorama import Fore, Back, Style
import re

from modules.utils import run_requests, printer, print_error


def site_status(domain):
    html_data = dict()
    html_data['meta'] = dict()
    html_data['http_headers'] = dict()
    html_data['redirects'] = ''
    html_data['analytics'] = dict()

    # print the title of the section
    printer(f'      ├───{Fore.BLACK}{Back.WHITE} General Info {Style.RESET_ALL}')

    # open the page
    text_data, \
    status_code, \
    history, \
    headers, \
    version = run_requests(
        'GET', 'http://' + domain, '', '', '', 'text', 'General Site Status'
    )
    
    
    # continues only if there is no error; HTTP status code 2xx and 3xx
    if status_code < 200 or status_code >= 400:
        texts = [
            f'Could not parse the HTML page.',
            f'HTML Status Code: {status_code}',
            f'History: {history}',
            f'HTTP Headers: {headers}',
            f'Request Result: text_data'
        ]
        print_error(True, texts)

        return html_data

    # get redirects
    if history:
        html_data['redirects'] += domain
        for step in history:
            html_data['redirects'] += ' ➜ ' + step.url

    # parse the data and write into a dict variable
    html_data['title'] = ''.join(re.findall('<title>(.*?)</title>', text_data, re.IGNORECASE))
    html_data['status_code'] = int(status_code)
    html_data['version'] = version
    
    # parse analytics
    value = ''.join(re.findall('[\s"\']+(UA-[\d\-]*)["|\'\s]+', text_data, re.IGNORECASE))
    if value:
        html_data['analytics']['Google'] = value

    # parse the HTML metadata
    soup = BeautifulSoup(text_data, "html.parser")
    soup = soup.findAll('meta')
    # iterate over the found metadata
    for meta in soup:
        # check if the attributes 'name' or 'http-equiv' are in it
        # if so, set it as the name
        if any(s.lower() == 'name' for s in meta.attrs.keys()):
            name = meta['name'].lower()
        elif any(s.lower() == 'http-equiv' for s in meta.attrs.keys()):
            name = meta['http-equiv'].lower()
        else:
            continue
        # set the content as the value
        value = meta['content']
        # add them to the list
        html_data['meta'][name] = value

    # print the result on STDOUT
    if html_data['status_code']:
        printer(f'      │      ■ HTTP Status:         {Fore.YELLOW} {html_data["status_code"]}{Style.RESET_ALL}')
    if html_data['redirects']:
        printer(f'      │      ■ HTTP Redirects:      {Fore.YELLOW} {html_data["redirects"]}{Style.RESET_ALL}')
    if html_data['title']:
        printer(f'      │      ■ Site Title:          {Fore.YELLOW} {html_data["title"]}{Style.RESET_ALL}')
    # print metadata
    for key, value in html_data['meta'].items():
        key = key.replace('_', ' ').replace('-', ' ').title()
        printer(f'      │      ■ {key+":":22}{Fore.YELLOW}{value}{Style.RESET_ALL}')
    # print analytics
    for key, value in html_data['analytics'].items():
        key = key.replace('_', ' ').replace('-', ' ').title()
        printer(f'      │      ■ {key+":":22}{Fore.YELLOW}{value}{Style.RESET_ALL}')
    # print HTTP headers
    if headers:
        printer(f'      │\n      ├───{Fore.BLACK}{Back.WHITE} HTTP Headers {Style.RESET_ALL}')

        # add the HTTP header to the list and print it
        for key, value in headers.items():
            key = key.lower()
            if key == 'content-security-policy':
                # print the key name
                printer(f'      │      ■ {key:22}')
                html_data['http_headers'][key] = dict()
                # get directives out of the value
                directives = value.strip().split(';')
                # iterate over the CSP directives
                for directive in directives:
                    if not directive:
                        continue
                    # split a directive
                    directive = directive.strip().split(' ')
                    # sanitize the directive
                    filter(None, directive)
                    directive = directive.remove(' ') if ' ' in directive else directive
                    # write the results in the output
                    html_data['http_headers'][key][directive[0]] = directive[1:]
                    # print the results
                    printer(f'      │          ∘ {Fore.BLUE}{directive[0] + ":":15}{Fore.YELLOW}{directive[1:]}{Style.RESET_ALL}')
            else:
                # write the results in the output
                html_data['http_headers'][key] = value
                # print the results
                printer(f'      │      ■ {key + ":":22}{Fore.YELLOW}{value}{Style.RESET_ALL}')

    # return results
    return html_data
