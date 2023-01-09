#!/usr/bin/env python


"""
    ### Vulnerability Scanner: Web Tech Survey

    This function gets the list of the technologies (services) used in the given 
    domain name alongside versions and categories.

    # Input:  - a single domain name
    # Output: - a set of dictionaries contains technologies used in the bacon
"""


import re
import json

from config import config
from modules.utils import run_requests, date_formatter


def web_tech_survey(domain):
    # variables to store results
    technologies = set()
    alt_names = set()

    # get the date format of the Rapid DNS from the config file
    date_format = config['api']['rapid_dns']['date_format']
    
    # get the results
    url = config['api']['web_tech_survey']['url'].format(domain)
    results = run_requests('GET', url, '', '', '', 'text', 'Web Tech Survey')

    # a regex to find technology and its version
    regex = r'<script>\s*window.__WTS_SSR_DATA__\s*=\s*(.*?)\s*</script>'
    results = json.loads(re.findall(regex, results))[0]['pageData']['results']

    # get the list of technologies and their versions
    for tech in results['AggregatedTechnologies']:
        for app in tech['Apps']:
            # add the found technology into the set
            technologies.add(
                {
                    'name': app['Technology'],
                    'version': app['Versions'][0],
                    'category': tech['Category'],
                    'date': date_formatter(tech['LastSeen'], date_format)
                }
            )
            for domain in app['Domains']:
                # add subdomains
                alt_names.add(
                    {
                        'value': domain['Domain'],
                        'reason': 'Technology',
                        'date': date_formatter(domain['LastSeen'], date_format)
                    }
                )
    
    # return gathered data
    return technologies
