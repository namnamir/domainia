#!/usr/bin/env python

from typing import List, Dict
from colorama import Fore, Style
from bs4 import BeautifulSoup

from modules.utilities.printer import printer
from modules.http_header.nonce_finder import nonce_finder
from modules.http_header.nonce_validator import nonce_validator
from modules.http_header.hashable_finder import hashable_finder
from modules.http_header.hash_validator import hash_validator


def csp_parser(csp: str, soup: BeautifulSoup) -> List[Dict[str, List[str]]]:
    """
    Parse the directives and sources of the HTTP Header "content-security-policy".
    The CSP is in this format: "directive1 source11 source12; directive2 source21 source22 source23;"

    Args:
        csp (str): The value of the CSP header.
        soup (BeautifulSoup): the BeautifulSoup format of the HTML page

    Returns:
        A list of dictionaries containing the directive and sources.

    Example:
        >>> csp_parser("default-src 'self'; img-src https://*")
        [{'directive': 'default-src', 'sources': ["'self'"]},
         {'directive': 'img-src', 'sources': ['https://*']}]
    """
    # a variable to store list of hashable elements, attributes, and events
    hashables = {
        'base-uri': set(),
        'child-src': set(),
        'connect-src': set(),
        'default-src': set(),
        'font-src': set(),
        'frame-src': set(),
        'img-src': set(),
        'manifest-src': set(),
        'media-src': set(),
        'object-src': set(),
        'prefetch-src': set(),
        'script-src': set(),
        'script-src-elem': set(),
        'script-src-attr': set(),
        'style-src': set(),
        'style-src-elem': set(),
        'style-src-attr': set(),
        'worker-src': set(),
    }
    # a dictionary to store data
    CSPs = []
    # two variables to store nonces and hashes
    nonces = []
    hashes = []
    # for each of the directives contains '-src' that are absent, the user agent looks for the 'default-src'
    # this variable assures that finding hashes for 'default-src' doesn't stop looking for other directives
    default_src_directive = False

    # get directives after sanitizing the CSP header
    csp = ' '.join(csp.split())
    directives = csp.strip().replace('; ', ';').replace(' ;', ';').split(';')

    # if 'default-src' is one of the directives bring it to the beginning of the the list
    # with this, we assure that it will be parsed at the first and would not mess with other directives
    if 'default_src' in directives:
        # flag it
        default_src_directive = True
        # bring 'default_src' to the position 0 in the list; so we'll have ['default_src', ...]
        directives = directives.insert(0, directives.pop(directives.index('default_src')))

    # iterate over the CSP directives
    for directive_source in directives:
        # sanitize each CSP value
        directive_source = directive_source.strip().replace('"', '').replace('\'', '')
        filter(None, directive_source)

        # get the directive and sources from the value
        directive = directive_source.split(' ')[0].strip()
        sources = directive_source.split(' ')[1:]

        # sanitize the list of sources
        filter(None, sources)

        # remove the nonce value
        # nonce is a random value that would be generated per each page load
        # so, it is not unique. read more: https://web.dev/strict-csp/
        for i, source in enumerate(sources):
            # check for nonces
            if source.lower().startswith('nonce-'):
                # find nonces in in-line JavaScript and CSS Style codes
                if not nonces:
                    nonces = nonce_finder(soup)

                # validate nonces
                sources[i] = nonce_validator(source, nonces)

            # check for hashes
            elif source.lower().startswith('sha'):
                # if the directive is 'default_src', get all data
                if directive == 'default_src':
                    hashables = hashable_finder(soup, directive)
                # if the directive is not parsed previously and if it is not 'default-src'
                elif not hashables[directive] or default_src_directive:
                    # get the hashable elements, events, and attributes
                    hashables[directive].update(hashable_finder(soup, directive)[directive])

                # validate hashes
                sources[i], hashable, hash = hash_validator(source, hashables[directive])

                # remove the hashed element from the list to prevent hashing elements multiple times
                if hashable in hashables[directive]:
                    hashables[directive].remove(hashable)

                # add the hash value to a list
                if hash:
                    hashes.append(hash)

        # continue only if there is a directive
        if directive:
            # write the results in the output
            CSPs.append(
                {
                    'directive': directive,
                    'sources': sources
                }
            )

            # print the results
            printer(f'      │          ∘ {directive + ":":20}{Fore.YELLOW}{sources}{Style.RESET_ALL}')

    # return results
    return [
        CSPs,
        nonces,
        hashes
    ]
