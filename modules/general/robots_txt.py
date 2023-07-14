#!/usr/bin/env python

from typing import Dict, List, Set, Union
from colorama import Fore, Style

from modules.utilities.printer import printer
from modules.utilities.url_opener import url_opener


def robots_txt(domain: str) -> Dict[str, Union[Set[str], List[Dict[str, Union[str, Set[str]]]]]]:
    """
    Fetches and parses the robots.txt file of a given domain.

    Args:
        domain (str): A string representing the domain to fetch the robots.txt file from.

    Returns:
        A dictionary with keys "sitemap" and "user_agent" (contains "name", "allow_list", and "disallow_list").
        The "sitemap" key contains a set of URLs listed in the Sitemap directive.
        The "user_agent" key contains a list of dictionaries of user-agents. The "names" contains the user-agent name,
        while "allow_list" and "disallow_list" keys contain sets of URLs allowed and disallowed by the directives.
    """
    # a variable to store cert info
    user_agents = []
    user_agent = ""
    sitemap = set()
    allow_list = set()
    disallow_list = set()
    flag = False

    # download the robots.txt
    url = f"http://{domain}/robots.txt"
    printer(f"      │        ├□ {Fore.GREEN}robots.txt is downloading{Style.RESET_ALL}")
    text_data, *_ = url_opener("GET", url, "", "", "", "text", "robots.txt file")

    # check if
    if not text_data:
        printer(f"      │        ├□ {Fore.RED}Could not download robots.txt or it does not exist{Style.RESET_ALL}")
        return {
            "sitemap": "",
            "user_agent": ""
        }

    # iterate over the lines in the robots.txt file
    for line in str(text_data).splitlines():
        # ignore comments and empty lines
        if not line or line.startswith("#"):
            continue

        # get the sitemap
        elif line.lower().startswith("sitemap:"):
            sitemap.add(line.split(":", maxsplit=1)[1].strip())

        # get the user-agent name
        elif line.lower().startswith("user-agent:"):
            # if there is a new user-agent
            # add the user-agent alongside allow/disallow list to the list
            if flag:
                user_agents.append(
                    {
                        "name": user_agent,
                        "allow_list": list(allow_list),
                        "disallow_list": list(disallow_list),
                    }
                )

                # reset variables
                sitemap = set()
                allow_list = set()
                disallow_list = set()
                user_agent = ""
                flag = False
            else:
                user_agent = line.split(":", maxsplit=1)[1].strip()
                flag = True

        # get the user-agent allow list
        elif line.startswith("Allow:"):
            allow_list.add(line.split(":", maxsplit=1)[1].strip())

        # get the user-agent disallow list
        elif line.startswith("Disallow:"):
            disallow_list.add(line.split(":", maxsplit=1)[1].strip())

    # add the last user-agent to the dictionary
    robots_txt = {
        "sitemap": list(sitemap),
        "user_agent": user_agents
    }

    return robots_txt
