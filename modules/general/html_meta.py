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
    # a list to store the extracted meta data
    html_meta_tags = []

    # find "meta" tags within the HTML content
    # ignore the ones has 'http-equiv' instead of 'name'
    meta_tags = soup.findAll('meta', {'http-equiv': None})

    # Iterate over the found metadata and extract the name and value attributes
    for tag in meta_tags:
        html_meta_tags.append({
            "name": tag.get("name").lower(),
            "value": tag.get("content", "")
        })

    # return results
    return html_meta_tags
