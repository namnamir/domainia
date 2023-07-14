#!/usr/bin/env python

import base64
import hashlib

from config import config


def hash_validator(source: str, hashables: set()) -> str:
    """
    This function validates a hash value of a given source and returns a term to show if it is matched
    with the hashed code in the HTML elements.

    Args:
        source (str): The source string containing the hash value.
        hashables (set): The list of elements that can be hashed

    Returns:
        str: The string defined in config file that shows if the hash value is matched or not.
    """
    # a variable to store hashed elements
    hashed_base64 = ''

    # go further only if there are elements that can be hashed
    if hashables:
        # sanitize the list of hashables
        filter(None, hashables)

        # iterate over hashable items
        for hashable in hashables:
            # a temporary variable that stores the hash algorithm
            hash_algorithm = ''

            # find the hash algorithm and the hash value
            if source.lower().startswith('sha256-'):
                sha_hashed = hashlib.sha256(hashable.encode('utf-8'))
                hash_algorithm = 'sha256'
            elif source.lower().startswith('sha384-'):
                sha_hashed = hashlib.sha384(hashable.encode('utf-8'))
                hash_algorithm = 'sha384'
            elif source.lower().startswith('sha512-'):
                sha_hashed = hashlib.sha512(hashable.encode('utf-8'))
                hash_algorithm = 'sha512'
            else:
                hashed_base64 = 'error'

            # if there is no error, get the base64 of the SHA-hash item
            if hashed_base64 != 'error':
                # get the base64 hash value of the SHA-hashed value
                hashed_base64 = base64.b64encode(sha_hashed.digest()).decode('utf8')

                # remove the shaXXX- from the source
                hashed_base64 = f'{hash_algorithm}-{hashed_base64}'

            # check if the hash is matched with the generated hash from HTML elements
            if source == hashed_base64:
                return [
                    config['html'][f'{hash_algorithm}']['matched'],
                    hashable,
                    source
                ]

        # in case hash of any hashable items doesn't match with the give hash in the source
        if hashed_base64 == 'error':
            return [
                config['html']['hash_error']['undefined'],
                hashable,
                source
            ]
        else:
            return [
                config['html'][f'{hash_algorithm}']['unmatched'],
                hashable,
                source
            ]
    # if there is not element that can be hashed while it is set in the CSP header as the source
    else:
        hash_algorithm = source.split('-')[0]

        # return unmatched as there is no element to be hashed
        return [
            config['html'][f'{hash_algorithm}']['unmatched_'],
            '',
            source,
        ]
