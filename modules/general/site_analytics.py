#!/usr/bin/env python


"""
    ### General: site_analytics_parser

    This function looks for any site analytics tracking IDs within the HTML page.

    # Input:  - the HTML in the format of text
    # Output: - a dictionary contains all site analytics tracking IDs
"""


import re


def site_analytics_parser(html):
    # a variable to store site analytics tracking IDs
    analytics = dict()

    # parse analytics
    value = ''.join(re.findall('[\s"\']+(UA-[\d\-]*)["|\'\s]+', html, re.IGNORECASE))
    if value:
        analytics['Google'] = value

    # return results
    return analytics
