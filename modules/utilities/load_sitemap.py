#!/usr/bin/env python

from typing import List
import logging
from colorama import Fore, Style
from usp.tree import sitemap_tree_for_homepage
import usp.exceptions

from config import config
from modules.utilities.printer import printer
from modules.utilities.exception_handling import exception_details


def load_sitemap(hostname: str) -> List[str]:
    """
    Fetches the sitemap for the given hostname and returns a list of internal links.

    Args:
        hostname (str): A string representing the hostname.

    Returns:
        A list of internal page links.
    """
    # A variable to store retrieved pages from the sitemap
    pages = []

    # Disable logging of USP
    logging.getLogger('usp').disabled = True
    logging.getLogger('usp.helpers').disabled = True
    logging.getLogger('usp.fetch_parse').disabled = True
    logging.getLogger('usp.tree').disabled = True

    # Get the sitemap
    try:
        sitemap_tree = sitemap_tree_for_homepage(f'http://{hostname}')

        # Generate the internal page links
        pages = [page.url for page in sitemap_tree.all_pages()]

    except usp.exceptions.GunzipException:
        ex = exception_details()
        printer(f'      │ ■ {Fore.RED}Error in in I/O (input/output).{Style.RESET_ALL}')
        if config['verbosity'] >= 4:
            printer(f'      │ ■■ ERROR: {Fore.MAGENTA}{ex[0]} → {ex[4]}:{ex[3]} ({ex[3].errno}, {ex[3].strerror}) '
                    f'{Fore.RED}  {ex[1]}{Style.RESET_ALL}')

    except usp.exceptions.SitemapException:
        ex = exception_details()
        printer(f'      │ ■ {Fore.RED}Can\'t run further, e.g. wrong input parameters.{Style.RESET_ALL}')
        if config['verbosity'] >= 4:
            printer(f'      │ ■■ ERROR: {Fore.MAGENTA}{ex[0]} → {ex[4]}:{ex[3]} ({ex[3].errno}, {ex[3].strerror}) '
                    f'{Fore.RED}  {ex[1]}{Style.RESET_ALL}')

    except usp.exceptions.SitemapXMLParsingException:
        ex = exception_details()
        printer(f'      │ ■ {Fore.RED}XML parsing exception to be handled gracefully.{Style.RESET_ALL}')
        if config['verbosity'] >= 4:
            printer(f'      │ ■■ ERROR: {Fore.MAGENTA}{ex[0]} → {ex[4]}:{ex[3]} ({ex[3].errno}, {ex[3].strerror}) '
                    f'{Fore.RED}  {ex[1]}{Style.RESET_ALL}')

    except usp.exceptions.StripURLToHomepageException:
        ex = exception_details()
        printer(f'      │ ■ {Fore.RED}Error in in I/O (input/output).{Style.RESET_ALL}')
        if config['verbosity'] >= 4:
            printer(f'      │ ■■ ERROR: {Fore.MAGENTA}{ex[0]} → {ex[4]}:{ex[3]} ({ex[3].errno}, {ex[3].strerror}) '
                    f'{Fore.RED}  {ex[1]}{Style.RESET_ALL}')

    finally:
        pages += hostname

    # Return the results
    return pages
