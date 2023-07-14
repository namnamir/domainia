#!/usr/bin/env python
"""
This module contains functions to send HTTP requests and return results in either text or JSON format.
"""

from colorama import Fore, Style
import random
import json
import requests
from typing import List, Union

from config import config
from modules.utilities.printer import printer
from modules.utilities.error_printer import error_printer


def url_opener(method: str, url: str, cookies: dict = None, data: dict = None, headers: dict = None,
               resp_type: str = 'text', name: str = '') -> List[Union[List, int, List, List, str]]:
    """
    This function sends the HTTP request based on the given method, cookies, data, headers, etc.
    and return the results in either text or JSON format.

    Args:
        method (str): HTTP method request; either GET or POST.
        url (str): URL for HTTP request.
        cookies (dict, optional): Cookies for HTTP request. Defaults to None.
        data (dict, optional): Data for HTTP request. Defaults to None.
        headers (dict, optional): Headers for HTTP request. Defaults to None.
        resp_type (str, optional): Type of response format (text/json/xml). Defaults to 'text'.
        name (str, optional): Name of the request. Defaults to ''.

    Returns:
        list: A list containing results with this order:
              [content, status_code, history, http_headers, version]
    """
    # some variables to store results
    content = []
    history = []
    http_headers = []
    version = ''
    status_code = 0

    # print the subtitle based on the the variable "name"
    if config['verbosity'] >= 2 and name:
        printer(f'      │        └□ {Fore.GREEN}{name} is calling{Style.RESET_ALL}')

    # form the header and add a random User-Agent
    if not headers:
        headers = {'User-Agent': random.choice(config['user_agents'])}
    else:
        headers['User-Agent'] = random.choice(config['user_agents'])

    # send the HTTP request based on the given method
    try:
        # run the GET request
        if method == 'GET':
            request = requests.get(
                url,
                headers=headers,
                timeout=config['delay']['requests_timeout']
            )
        # run the POST request
        elif method == 'POST':
            request = requests.post(
                url,
                cookies=cookies,
                data=json.dumps(data),
                headers=headers,
                timeout=config['delay']['requests_timeout']
            )

        # get the status code
        status_code = int(request.status_code)

        # get the history
        history = request.history

        # get the headers
        http_headers = request.headers

        # get the HTTP version
        version = request.raw.version

        # get the results if there is the type is either 'text', 'xml', or 'json'
        if resp_type == 'json':
            content = json.loads(request.text)
        elif resp_type == 'text' or resp_type == 'xml':
            content = request.text
        else:
            content = request

    # exceptions
    except requests.exceptions.SSLError:
        texts = [
            f'The URL {url} cannot be opened due to an SSL error.',
            '',
            f'Status Code: {status_code}  -  API call URL: {url}'
        ]
        error_printer('exception', texts)
    except requests.exceptions.TooManyRedirects:
        texts = [
            f'The provided {name} URL does not seem correct.',
            '',
            f'Status Code: {status_code}  -  API call URL: {url}'
        ]
        error_printer('exception', texts)
    except requests.exceptions.HTTPError:
        texts = [
            f'Error in loading the {name} URL page.',
            '',
            f'Status Code: {status_code}  -  API call URL: {url}'
        ]
        error_printer('exception', texts)
    except requests.exceptions.ConnectionError:
        texts = [
            f'Error in establishing the connection to the {name} URL.',
            '',
            f'Status Code: {status_code}  -  API call URL: {url}'
        ]
        error_printer('exception', texts)
    except requests.exceptions.Timeout:
        texts = [
            f'Timeout error while opening {name} URL.',
            '',
            f'Status Code: {status_code}  -  API call URL: {url}'
        ]
        error_printer('exception', texts)
    except requests.exceptions.RequestException:
        texts = [
            f'Error in reading the data from the {name} URL.',
            '',
            f'Status Code: {status_code}  -  API call URL: {url}'
        ]
        error_printer('exception', texts)
    except json.decoder.JSONDecodeError:
        texts = [
            f'Error in reading the JSON data retrieved from the {name} call.',
            '',
            f'Status Code: {status_code}  -  API call URL: {url}'
        ]
        error_printer('exception', texts)
    except ValueError:
        texts = [
            f'No Result is found or there was an error for {name}.',
            '',
            f'Status Code: {status_code}  -  API call URL: {url}'
        ]
        error_printer('exception', texts)
    except Exception:
        texts = [
            f'An unknown error is ocurred while running {name}.',
            '',
            f'Status Code: {status_code}  -  API call URL: {url}'
        ]
        error_printer('exception', texts)

    # return results
    return [
        content,
        status_code,
        history,
        http_headers,
        version
    ]
