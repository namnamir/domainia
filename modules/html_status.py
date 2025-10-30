#!/usr/bin/env python

from bs4 import BeautifulSoup
from colorama import Fore, Back, Style
from typing import Dict

from config import config
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
    # A variable to store HTML data
    html_data = {
        'meta': {},
        # CSP headers are added as they might not be used in the page
        # However, we need to parse them later
        'http_headers': [],
        'redirects': [],
        'analytics': {},
        'csp_nonces': [],
        'csp_hashes': [],
    }

    # Print the title of the section
    printer(f'      ├───{Fore.BLACK}{Back.WHITE} General Info {Style.RESET_ALL}')

    # Sanitize the URL
    url = url_sanitizer(domain)[0]

    # Open the page
    text_data, status_code, history, headers, version, url = url_opener(
        'GET', url, '', '', '', 'text', 'General Site Status function',
    )

    # Continues only if there is no error; HTTP status code 2xx and 3xx
    if status_code < 200 or status_code >= 400:
        texts = [
            'Could not parse the HTML page.',
            f'HTTP Status Code: {status_code}',
            f'History: {history}',
            f'HTTP Headers: {headers}',
            f'Request Result: {text_data}',
        ]
        error_printer(True, texts)
        html_data['status_code'] = int(status_code)

    # If there is no error
    else:
        # Parse the HTML metadata
        soup = BeautifulSoup(text_data, "html.parser")

        # Get redirects
        if config['scan_type']['http_switch'][0] and history:
            html_data['redirects'].append(domain)
            # iterate over the redirection history
            for step in history:
                html_data['redirects'].append(step.url)

        # Get site analytics
        if config['scan_type']['http_switch'][1]:
            html_data['analytics'] = site_analytics_parser(text_data)

        # Parse the meta data and add them to the dictionary
        if config['scan_type']['http_switch'][2]:
            html_data['meta'] = meta_parser(soup)

        # Find any links in the page
        if config['scan_type']['http_switch'][3]:
            html_data['links'] = link_finder(soup, domain)

        # Find any forms in the page
        if config['scan_type']['http_switch'][4]:
            html_data['forms'] = form_finder(soup)

        # Parse the 'title' element and other data and write into a dict variable
        html_data['title'] = soup.find('title').text.strip() if soup.find('title') else ''
        html_data['status_code'] = int(status_code)
        html_data['version'] = version

        # Print the result
        printer(f'      │      ■ Domain:                 {Fore.YELLOW}{domain}{Style.RESET_ALL}')
        printer(f'      │      ■ Scanned URL:            {Fore.YELLOW}{url}{Style.RESET_ALL}')
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

            # Print the number of HTML element
            if 'count' in html_data['links'] and html_data['links']['count']:
                printer(f'      │\n      ├───{Fore.BLACK}{Back.WHITE} HTML elements with Links {Style.RESET_ALL}')

                # Iterate over HTTP elements
                for element in html_data['links']['count']:
                    if (
                        not element.startswith(tuple(['int_', 'ext_', 'internal', 'external']))
                        and html_data["links"]["count"][element]
                    ):
                        printer(f'      │      ■ No. of Elements {"<" + element + ">:":11}'
                                f'{Fore.YELLOW} {html_data["links"]["count"][element]}{Style.RESET_ALL}')

        # Print metadata
        if 'meta' in html_data and html_data['meta']:
            printer(f'      │\n      ├───{Fore.BLACK}{Back.WHITE} HTML Metadata {Style.RESET_ALL}')

            # Iterate over metadata
            for meta in html_data['meta']:
                for key, value in meta.items():
                    key = key.replace('_', ' ').replace('-', ' ').title()
                    printer(f'      │      ■ {key + ":":24}{Fore.YELLOW}{value}{Style.RESET_ALL}')

        # Print analytics
        if 'analytics' in html_data and html_data['analytics']:
            printer(f'      │\n      ├───{Fore.BLACK}{Back.WHITE} Site Analytics Tracking IDs {Style.RESET_ALL}')

            # Iterate over the analytics codes
            for key, value in html_data['analytics'].items():
                key = key.replace('_', ' ').replace('-', ' ').title()
                printer(f'      │      ■ {key + ":":24}{Fore.YELLOW}{value}{Style.RESET_ALL}')

        # Print HTTP headers
        if config['scan_type']['http_switch'][5] and headers:
            printer(f'      │\n      ├───{Fore.BLACK}{Back.WHITE} HTTP Headers {Style.RESET_ALL}')

            # Add the HTTP header to the list and print it
            for key, value in headers.items():
                key = key.lower()
                csp_flag = True

                # Get the CSP
                if key in ('content-security-policy', 'content-security-policy-report-only'):
                    csp_flag = False
                    # Print the results
                    printer(f'      │      ■ {key}')
                    # Parse CSP as well as get nonces and hashes
                    csp_value, nonces, hashes = csp_parser(value, soup)
                    # Write the CSP results in the output
                    html_data['http_headers'].append(
                        {
                            'name': key,
                            'value': csp_value
                        }
                    )
                    # Add nonces and hashes to the output
                    html_data['csp_nonces'] += nonces
                    html_data['csp_hashes'] += hashes

                # Other HTTP headers rather than CSP or CSP-Report-Only
                else:
                    # Print the results
                    printer(f'      │      ■ {key + ":":24}{Fore.YELLOW}{value}{Style.RESET_ALL}')
                    # Write the results in the output
                    html_data['http_headers'].append(
                        {
                            'name': key,
                            'value': value
                        }
                    )
            # If CSP or CSP-Report-Only is not set
            if csp_flag:
                # Write the error message of no CSP is set
                html_data['http_headers'].append(
                    {
                        'name': '__WARNING__',
                        'value': 'NO_CSP'
                    }
                )
        # If there HTTP header is not retrieved or doesn't exist
        elif config['scan_type']['http_switch'][5] and not headers:
            html_data['http_headers'] = {
                'name': '__ERROR__',
                'value': 'NO_HTTP_HEADER'
            }

        # Get CSP headers in HTML meta element; it should contain the attribute 'http-equiv'
        for csp in ('content-security-policy', 'content-security-policy-report-only'):
            # Find <meta> elements contains the attribute 'http-equiv' with certain values
            csp_header = soup.find('meta', {'http-equiv': csp})
            if csp_header:
                # Parse CSP as well as get nonces and hashes
                csp_value, nonces, hashes = csp_parser(csp_header.attrs['content'], soup)
                # Write the results in the output
                html_data['http_headers'].append(
                    {
                        'name': csp,
                        'value': csp_value
                    }
                )
                # Add nonces and hashes to the output
                html_data['csp_nonces'] += nonces
                html_data['csp_hashes'] += hashes

        # Remove duplications from the list
        html_data['csp_nonces'] = list(set(html_data['csp_nonces']))
        html_data['csp_hashes'] = list(set(html_data['csp_hashes']))

    # Return results
    return [
        html_data,
        url
    ]
