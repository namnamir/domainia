#!/usr/bin/env python


"""
    ### General: html_meta

    This function gets the details of the robots.txt file and parse it based on 
    the user-agent.

    # Input:  - a single domain name
    # Output: - a dictionary contains robots.txt details
"""


from colorama import Fore, Style
from modules.utils import run_requests, printer


def html_meta(domain):
    # a variable to store cert info
    html_meta = dict()
    html_meta['sitemap'] = set()
    html_meta['user_agent'] = dict()
    allow_list = set()
    disallow_list = set()

    # download the certificate page on CRT
    url = 'http://' + domain + '/robots.txt'
    printer('      │        ├□ ' + Fore.GREEN + 'robots.txt is downloading' + Style.RESET_ALL)
    results = run_requests('GET', url, '', '', '', 'text', 'robots.txt file')[0]
    
    # check if 
    if not results:
        printer('      │        ├□ ' + Fore.RED + 'Could not download robots.txt or it does not exist' + Style.RESET_ALL)
        return html_meta

    # iterate over the lines in the robots.txt file
    for line in str(results).splitlines():
        # ignore comments and empty lines
        if not line or line.startswith('#'):
            continue
        # get the sitemap
        elif line.startswith('Sitemap:'):
            sitemap = line.split(':', maxsplit=1)[1].strip()
            html_meta['sitemap'].add(sitemap)
        # get the user-agent
        elif line.startswith('User-agent:'):
            # if the a new user-agent is found
            if flag:
                html_meta['user_agent'].add(
                    {
                        'name': user_agent,
                        'allow': allow_list,
                        'disallow': disallow_list,
                    }
                )
                allow_list = set()
                disallow_list = set()
                flag = False
            
            user_agent = line.split(':, maxsplit=1')[1].strip()
            flag = True
        # get the user-agent
        elif line.startswith('Allow:'):
            user_agent = line.split(':, maxsplit=1')[1].strip()
            allow_list.add(line)
        # get the user-agent
        elif line.startswith('Disallow:'):
            user_agent = line.split(':, maxsplit=1')[1].strip()
            disallow_list.add(line)
    
    # add the last user-agent to the dictionary
    html_meta['user_agent'].add(
        {
            'name': user_agent,
            'allow': allow_list,
            'disallow': disallow_list,
        }
    )

    return html_meta
