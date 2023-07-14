#!/usr/bin/env python

from typing import List
from bs4 import BeautifulSoup


def nonce_finder(soup: BeautifulSoup) -> List[str]:
    """
    This function looks for any HTML <script> or <style> element has a nonce.
    CSP HTTP Header would be like: Content-Security-Policy: script-src 'nonce-{RANDOM}';
    HTML <script> element would be like: <script nonce="nonce-{RANDOM}"> CODE </script>

    Args:
        soup (BeautifulSoup): the BeautifulSoup format of the HTML page

    Returns:
        nonce (list): a list contains all unique nonces
    """
    nonces = set()

    # get all <style> and <script> elements that contain the 'nonce' attribute
    elements = soup.findAll('style', nonce=True)
    elements += soup.findAll('script', nonce=True)

    # iterate over elemnts
    for element in elements:
        # add the nonce to the set
        nonces.add(element['nonce'])

    # return results
    return list(nonces)
