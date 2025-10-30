#!/usr/bin/env python

from modules.dns.dns_resolver import dns_resolver
from modules.dns.utils import dns_record_type, rr_record_finder


def dns_dig(domain, key, record):
    """
    ### DNS Checker: DNS Dig

    This function gets the value of all DNS records.

    # Input:  - a single domain name
              - the key, subdomain, or selector.subdomain
              - a single DNS record either in an RR type (int) or case-insensitive string; e.g. 1 or A or a
    # Output: - a set of dictionaries contains a single DNS record details
    """
    # A variable to store results
    results = set()

    # Get the RR type of the DNS record
    rr_record = rr_record_finder(record)

    # Resolve the DNS record
    answers = dns_resolver(domain, record)

    # Iterate over answers
    for answer in answers:
        results.add({
            'record': record,
            'type': dns_record_type(rr_record, key, answer),
            'key': key,
            'value': answer.to_text()
        })

    # Return the list of the DNS records
    return results
