#!/usr/bin/env python

from bs4 import BeautifulSoup
from urllib.parse import urlparse
from typing import Dict, Any

from config import config
from modules.utilities.url_sanitizer import url_sanitizer


def link_finder(soup: BeautifulSoup, domain: str) -> Dict[str, Any]:
    """
    This function looks for any links within the HTML page. It would checks if
    the link is internal or external and write them in the specified dictionary.

    Args:
        soup (BeautifulSoup): the BeautifulSoup format of the HTML page
        domain (str): the domain name

    Returns:
        links (dict): a dictionary contains all (external and internal) links
    """
    # a temporary variable
    temp = []
    # a variable to store results in
    links = {
        'internal': [],
        'external': [],
        'count': {
            'internal': 0,
            'external': 0,
        }
    }

    # Initialize element counts to 0
    for element_link in config['html']['elements_links']:
        links['count'][element_link[0]] = 0
        links['count'][f'int_{element_link[0]}'] = 0
        links['count'][f'ext_{element_link[0]}'] = 0

    # Find 'link' elements within the HTML content
    for element_link in config['html']['elements_links']:
        elements = soup.findAll(element_link[0])

        for element in elements:
            # Ignore the situation that the HTML element doesn't contain any link
            # e.g., <script>console.log('Hi!')</script>
            if not element.has_attr(element_link[1]):
                continue

            # Define link
            link = element[element_link[1]]

            # Ignore empty links or non-links like anchor, 'mailto', etc.
            if (
                link in temp
                or not link
                or link.startswith(tuple(config['html']['elements_links_ignore']))
            ):
                continue

            # Add the link to the temp in order to prevent duplication
            temp.append(link)

            # Check if the link is external
            # It looks for any scheme like http(s), (s)ftp, sip, etc.
            if (
                urlparse(link).hostname
                and urlparse(link).hostname.replace('www.', '') != url_sanitizer(domain)[1]
            ):
                links['external'].append({
                    'link': link,
                    'html_element': element_link[0]
                })
                # Count the total number of external links and per element
                links['count']['external'] += 1
                links['count'][element_link[0]] += 1
                links['count'][f'ext_{element_link[0]}'] += 1

            # If the link is internal
            else:
                links['internal'].append({
                    'link': link,
                    'html_element': element_link[0]
                })
                # Count the total number of internal links and per element
                links['count']['internal'] += 1
                links['count'][element_link[0]] += 1
                links['count'][f'int_{element_link[0]}'] += 1

    return links
