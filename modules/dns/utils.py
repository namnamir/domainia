#!/usr/bin/env python


"""
    ### DNS: Utilities

    Here is the list of general functions used for DNS queries
"""


from config import config

import re


# get the rr_record and the answer, return the DNS record type
# i.e. for a TXT record, it might return SPF, DMARC or DKIM
def dns_record_type(rr_record, key, answer):
    # iterate over the list of terms used in TXT records
    # it is used to fill the 'type' filed
    if rr_record == 16:
        for txt_term in sorted(set(config['dns']['include_txt_records'])):
            if txt_term.lower() in [answer.lower(), key.lower()]:
                return txt_term.split(':')[0]
            else:
                return ''


# convert the DNS record to RR Type
def rr_record_finder(record):
    # check if record itself is an RR type
    if isinstance(record, int):
        rr_record = record
    else:
        rr_record = config['dns']['rr_dns_records'][record]
    
    return rr_record
