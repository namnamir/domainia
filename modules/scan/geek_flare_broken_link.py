#!/usr/bin/env python


"""
    ### Vulnerability Scanner: Geek Flare

    This function gets the list of internal and external links as well as their 
    HTTP status that defines which is broken and which is not

    # Input:  - a single domain name
    # Output: - a set of dictionaries contains non-broken internal links
              - a set of dictionaries contains non-broken external links
              - a set of dictionaries contains broken internal links
              - a set of dictionaries contains broken external links
"""


from config import config
from modules.utils import run_requests, print_error


def geek_flare_broken_link(domain):
    # variables to store results
    broken_internal_links = set()
    broken_external_links = set()
    internal_links = set()
    external_links = set()

    data = {
        "url": domain,
        "proxyCountry": config['api']['geek_flare']['proxy_country'],
        "followRedirect": True
    }
    headers = {
        'x-api-key': config['api']['geek_flare']['api_key'],
        'Content-Type': 'application/json'
    }

    # check if report exist
    url = config['api']['geek_flare']['url_broken_link']
    results = run_requests('POST', url, '', data, headers, 'json', 'Geek Flare')

    # check if there is any error
    if results['apiCode'] != 200:
        # get the list of links & specify if it is internal, external or broken
        for link in results['data']:
            if link['status'] != 404:
                if domain in link['link']:
                    # add the found broken internal link into the set
                    broken_internal_links.add(
                        {
                            'name': link['link'],
                            'status': link['status'],
                        }
                    )
                else:
                    # add the found broken external link into the set
                    broken_external_links.add(
                        {
                            'name': link['link'],
                            'status': link['status'],
                        }
                    )
            else:
                if domain in link['link']:
                    # add the found internal link into the set
                    internal_links.add(
                        {
                            'name': link['link'],
                            'status': link['status'],
                        }
                    )
                else:
                    # add the found external link into the set
                    external_links.add(
                        {
                            'name': link['link'],
                            'status': link['status'],
                        }
                    )

    else:
        errors = [
            f'There is an error in getting the data from Geek Flare',
            '',
            f'{results["message"]}',
            '',
            ''
        ]
        print_error(True, errors)
    
    # return gathered data
    return [
        broken_internal_links,
        broken_external_links,
        internal_links,
        external_links
    ]
