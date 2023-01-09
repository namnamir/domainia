#!/usr/bin/env python


"""
    ### Vulnerability Scanner: W3 Techs

    This function gets the list of the technologies (services) used in the given 
    domain name alongside versions.

    # Input:  - a single domain name
    # Output: - a set of dictionaries contains technologies used in the bacon
"""


import re
from time import sleep

from config import config
from modules.utils import run_requests


def w3_techs(domain):
    # variables to store results
    technologies = set()

    # get the delay defined in the config file
    delay = config['w3_techs']['delay']
    
    # check if report exist
    while True:
        url = config['api']['w3_techs']['url'].format(domain)
        results = run_requests('GET', url, '', '', '', 'text', 'W3 Techs')
        
        # find the "Crawl now!" button
        button = False if ('Crawl now!' in results) else True
        
        # if the doesn't exist, the report exits
        if button:
            break
        else:
            # sleep for a certain time to finish the scan
            sleep(delay)

            # send the HTTP request to scan
            data = {'add_site': '+Crawl+now!+'}
            run_requests('POST', url, '', data, '', 'text', 'W3 Techs')

    # get the results and remove data for "Site Elements" and others after it
    results = results.split('Site Elements')[0]

    # a regex to find technology and its version
    regex = r'<a href="https://w3techs.com/technologies.*?">(.*?)</a> (.*?)<br'

    # get the list of technologies and their versions
    for tech, version in re.findall(regex, results):
        # add the found technology into the set
        technologies.add(
            {
                'name': tech,
                'version': version.strip('</s>'),
                'category': '',
                'date': ''
            }
        )
    
    # return gathered data
    return technologies
