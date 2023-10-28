#!/usr/bin/env python

from bs4 import BeautifulSoup
from colorama import Fore, Back, Style
from typing import Dict

from modules.general.html_meta import meta_parser
from modules.general.html_form import form_finder
from modules.general.html_links import link_finder
from modules.general.site_analytics import site_analytics_parser
from modules.http_header.csp import csp_parser
from modules.utilities.printer import printer
from modules.utilities.error_printer import error_printer
from modules.utilities.url_opener import url_opener
from modules.utilities.url_sanitizer import url_sanitizer


def site_status(domain: str) -> Dict[str, any]:
    """
    Retrieves general information and metadata about a website.

    Args:
        domain: The domain of the website to retrieve information from.

    Returns:
        A dictionary containing information and metadata about the website.
    """
    # some variables to store HTML data
    html_data = {
        'meta': {},
        # CSP headers are added as they might not be used in the page
        # however, we need to parse them later
        'http_headers': [
        ],
        'redirects': [],
        'analytics': {},
        'csp_nonces': [],
        'csp_hashes': [],
    }

    # print the title of the section
    printer(f'      ├───{Fore.BLACK}{Back.WHITE} General Info {Style.RESET_ALL}')

    # sanitize the URL
    url = url_sanitizer(domain)[0]

    # open the page
    text_data, status_code, history, headers, version = url_opener(
        'GET', url, '', '', '', 'text', 'General Site Status function',
    )

    # continues only if there is no error; HTTP status code 2xx and 3xx
    if status_code < 200 or status_code >= 400:
        texts = [
            'Could not parse the HTML page.',
            f'HTTP Status Code: {status_code}',
            f'History: {history}',
            f'HTTP Headers: {headers}',
            f'Request Result: {text_data}',
        ]
        error_printer(True, texts)
        return html_data

    # parse the HTML metadata
    soup = BeautifulSoup(text_data, "html.parser")

    # # get redirects
    # if history:
    #     html_data['redirects'].append(domain)
    #     # iterate over the redirection history
    #     for step in history:
    #         html_data['redirects'].append(step.url)

    # # get site analytics
    # html_data['analytics'] = site_analytics_parser(text_data)

    # # parse the meta data and add them to the dictionary
    # html_data['meta'] = meta_parser(soup)

    # # find any links in the page
    # html_data['links'] = link_finder(soup, domain)

    # find any forms in the page
    html_data['forms'] = form_finder(soup)

    # parse the 'title' element and other data and write into a dict variable
    html_data['title'] = soup.find('title').text if soup.find('title') else ''
    html_data['status_code'] = int(status_code)
    html_data['version'] = version

    # print the result
    printer(f'      │      ■ Scanned URN:            {Fore.YELLOW}{domain}{Style.RESET_ALL}')
    if 'status_code' in html_data and html_data['status_code']:
        printer('      │      ■ HTTP Status:            '
                f'{Fore.YELLOW}{html_data["status_code"]}{Style.RESET_ALL}')
    if 'redirects' in html_data and html_data['redirects']:
        printer('      │      ■ HTTP Redirects:         '
                f'{Fore.YELLOW}{" ➜ ".join(html_data["redirects"])}{Style.RESET_ALL}')
    if 'title' in html_data and html_data['title']:
        printer('      │      ■ Site Title:             '
                f'{Fore.YELLOW}{html_data["title"]}{Style.RESET_ALL}')
    if 'links' in html_data and html_data['links']:
        printer('      │      ■ No. of Links:           '
                f'Internal -> {Fore.YELLOW} {html_data["links"]["count"]["internal"]}{Style.RESET_ALL}  |  '
                f'External -> {Fore.YELLOW} {html_data["links"]["count"]["external"]}{Style.RESET_ALL}')

        # print the number of HTML element
        if 'count' in html_data['links'] and html_data['links']['count']:
            printer(f'      │\n      ├───{Fore.BLACK}{Back.WHITE} HTML elements with Links {Style.RESET_ALL}')

            for element in html_data['links']['count']:
                if (
                    not element.startswith(tuple(['int_', 'ext_', 'internal', 'external']))
                    and html_data["links"]["count"][element]
                ):
                    printer(f'      │      ■ No. of Elements {"<" + element + ">:":11}'
                            f'{Fore.YELLOW} {html_data["links"]["count"][element]}{Style.RESET_ALL}')

    # print metadata
    if 'meta' in html_data and html_data['meta']:
        printer(f'      │\n      ├───{Fore.BLACK}{Back.WHITE} HTML Metadata {Style.RESET_ALL}')

        for key, value in html_data['meta'].items():
            key = key.replace('_', ' ').replace('-', ' ').title()
            printer(f'      │      ■ {key + ":":24}{Fore.YELLOW}{value}{Style.RESET_ALL}')

    # print analytics
    if 'analytics' in html_data and html_data['analytics']:
        printer(f'      │\n      ├───{Fore.BLACK}{Back.WHITE} Site Analytics Tracking IDs  {Style.RESET_ALL}')

        for key, value in html_data['analytics'].items():
            key = key.replace('_', ' ').replace('-', ' ').title()
            printer(f'      │      ■ {key + ":":24}{Fore.YELLOW}{value}{Style.RESET_ALL}')

    # print HTTP headers
    if headers:
        printer(f'      │\n      ├───{Fore.BLACK}{Back.WHITE} HTTP Headers {Style.RESET_ALL}')

        # add the HTTP header to the list and print it
        for key, value in headers.items():
            key = key.lower()

            # get the CSP
            if key in ('content-security-policy', 'content-security-policy-report-only'):
                # print the results
                printer(f'      │      ■ {key}')
                # parse CSP as well as get nonces and hashes
                csp_value, nonces, hashes = csp_parser(value, soup)
                # write the CSP results in the output
                html_data['http_headers'].append(
                    {
                        'name': key,
                        'value': csp_value
                    }
                )
                # add nonces and hashes to the output
                html_data['csp_nonces'] += nonces
                html_data['csp_hashes'] += hashes
            else:
                # print the results
                printer(f'      │      ■ {key + ":":24}{Fore.YELLOW}{value}{Style.RESET_ALL}')
                # write the results in the output
                html_data['http_headers'].append(
                    {
                        'name': key,
                        'value': value
                    }
                )

    # get CSP headers in HTML meta element; it should contain the attribute 'http-equiv'
    for csp in ('content-security-policy', 'content-security-policy-report-only'):
        # find <meta> elements contains the attribute 'http-equiv' with certain values
        csp_header = soup.find('meta', {'http-equiv': csp})
        if csp_header:
            # parse CSP as well as get nonces and hashes
            csp_value, nonces, hashes = csp_parser(csp_header.attrs['content'], soup)
            # write the results in the output
            html_data['http_headers'].append(
                {
                    'name': csp,
                    'value': csp_value
                }
            )
            # add nonces and hashes to the output
            html_data['csp_nonces'] += nonces
            html_data['csp_hashes'] += hashes

    # # remove duplications from the list
    # html_data['csp_nonces'] = list(set(html_data['csp_nonces']))
    # html_data['csp_hashes'] = list(set(html_data['csp_hashes']))

    # return results
    return html_data
