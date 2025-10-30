#!/usr/bin/env python

from typing import List

from config import config


def nonce_validator(source: str, nonces: List[str]) -> str:
    """
    This function validates a nonce of a given source and returns a term to show if it is matched
    with the value of the nonce attribute in the HTML element.

    Args:
        source (str): The source string containing the nonce.
        nonces (list): The list of nonces

    Returns:
        str: The string defined in config file that shows if the nonce is matched or not.
    """
    # check if the nonce is matched with the gathered nonces from HTML <script> or <style> elements
    if nonces:
        if source.replace('nonce-', '') in nonces:
            return config['html']['nonce']['matched']
        else:
            return config['html']['nonce']['unmatched']
    # if there is no element with the attribute 'nonce' while it is set in the CSP header as the source
    else:
        return config['html']['nonce']['unmatched_']
