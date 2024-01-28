#!/usr/bin/env python

from typing import List, Dict
from bs4 import BeautifulSoup


def meta_parser(soup: BeautifulSoup) -> List[Dict[str, str]]:
    """
    Extracts meta data tags from the given BeautifulSoup object and returns a
    list of dictionaries containing the name and value attributes.

    Args:
        soup (BeautifulSoup): A BeautifulSoup object representing an HTML page.

    Returns:
        List[Dict[str, str]]: A list of dictionaries containing the extracted meta data.
    """
    # A list to store the extracted meta data
    html_meta_tags = []

    # Find "meta" tags within the HTML content
    # Ignore the ones has 'http-equiv' instead of 'name'
    meta_tags = soup.findAll('meta', {'http-equiv': None})

    # Iterate over the found metadata and extract the name and value attributes
    for tag in meta_tags:
        # Set the attribute type
        if tag.get('name'):
            attribute_type = 'name'
        elif tag.get('http-equiv'):
            attribute_type = 'http-equiv'
        elif tag.get('charset'):
            attribute_type = 'charset'
        elif tag.get('property'):
            attribute_type = 'property'
        elif tag.get('itemprop'):
            attribute_type = 'itemprop'
        else:
            print(f'Cannot parse the HTML Meta tag: {tag}')
            continue

        name = tag.get(attribute_type).lower()
        value = tag.get('content', '')

        html_meta_tags.append({
            'attribute': attribute_type,
            'name': name if attribute_type != 'charset' else 'charset',
            'value': value if attribute_type != 'charset' else name,
        })

    # Return results
    return html_meta_tags
