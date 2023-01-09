#!/usr/bin/env python


"""
    ### General: robots_txt

    This function gets the details of the robots.txt file and parse it based on 
    the user-agent.

    # Input:  - a single domain name
    # Output: - a dictionary contains robots.txt details
"""


from colorama import Fore, Style

from modules.utils import run_requests, printer


def robots_txt(domain):
    # a variable to store cert info
    robots_txt = dict()
    robots_txt['sitemap'] = set()
    robots_txt['user_agent'] = dict()
    allow_list = set()
    disallow_list = set()

    # download the robots.txt
    url = 'http://' + domain + '/robots.txt'
    printer('      │        ├□ ' + Fore.GREEN + 'robots.txt is downloading' + Style.RESET_ALL)
    results = run_requests('GET', url, '', '', '', 'text', 'robots.txt file')[0]
    
    # check if 
    if not results:
        printer('      │        ├□ ' + Fore.RED + 'Could not download robots.txt or it does not exist' + Style.RESET_ALL)
        return robots_txt

    # iterate over the lines in the robots.txt file
    for line in str(results).splitlines():
        # ignore comments and empty lines
        if not line or line.startswith('#'):
            continue
        # get the sitemap
        elif line.startswith('Sitemap:'):
            sitemap = line.split(':', maxsplit=1)[1].strip()
            robots_txt['sitemap'].add(sitemap)
        # get the user-agent
        elif line.startswith('User-agent:'):
            # if the a new user-agent is found
            if flag:
                robots_txt['user_agent'].add(
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
    robots_txt['user_agent'].add(
        {
            'name': user_agent,
            'allow': allow_list,
            'disallow': disallow_list,
        }
    )

    return robots_txt
