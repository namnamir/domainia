#!/usr/bin/env python

from colorama import Fore, Style
import random
import json
import requests
from typing import List, Union

from config import config
from modules.utilities.printer import printer
from modules.utilities.error_printer import error_printer


def url_opener(method: str, url: str, cookies: dict = None, data: dict = None, headers: dict = None,
               resp_type: str = 'text', name: str = '') -> List[Union[List, int, List, List, str, str]]:
    """
    This function calls sends the HTTP request based on the given method, cookies, data, headers, etc.
    and return the results in either text or JSON format. If the 'HTTP status code' is not within 200
    or 300, it tries to run it in HTTPs by replacing the scheme.

    Args:
        method (str): HTTP method request; either GET or POST.
        url (str): URL for HTTP request.
        cookies (dict, optional): Cookies for HTTP request; defaults is None.
        data (dict, optional): Data for HTTP request; defaults is None.
        headers (dict, optional): Headers for HTTP request; defaults is None.
        resp_type (str, optional): Type of response format (text/json/xml); defaults is 'text'.
        name (str, optional): Name of the request; defaults is ''.

    Returns:
        list: A list containing results with this order:
              [content, status_code, history, http_headers, version, url]
    """
    # Call the main function
    content, status_code, history, http_headers, version = requests_runner(
            method, url, cookies, data, headers, resp_type, name
        )

    # If there is any error in getting the HTTP request, try the HTTPs
    if status_code < 200 or status_code >= 400:
        url = url.replace('http://', 'https://')
        content, status_code, history, http_headers, version = requests_runner(
            method, url, cookies, data, headers, resp_type, name
        )

    # Return results
    return [
        content,
        status_code,
        history,
        http_headers,
        version,
        url  # In case the URL's scheme is changed
    ]


def requests_runner(method: str, url: str, cookies: dict = None, data: dict = None, headers: dict = None,
                    resp_type: str = 'text', name: str = '') -> List[Union[List, int, List, List, str, str]]:
    """
    This function sends the HTTP request based on the given method, cookies, data, headers, etc.
    and return the results in either text or JSON format.

    Args:
        method (str): HTTP method request; either GET or POST.
        url (str): URL for HTTP request.
        cookies (dict, optional): Cookies for HTTP request; defaults is None.
        data (dict, optional): Data for HTTP request; defaults is None.
        headers (dict, optional): Headers for HTTP request; defaults is None.
        resp_type (str, optional): Type of response format (text/json/xml); defaults is 'text'.
        name (str, optional): Name of the request; defaults is ''.

    Returns:
        list: A list containing results with this order:
              [content, status_code, history, http_headers, version, url]
    """
    # Some variables to store results
    content = []
    status_code = 0
    history = []
    http_headers = []
    version = ''

    # Print the subtitle based on the the variable "name"
    if config['verbosity'] >= 2 and name:
        printer(f'      │          ∘ {Fore.GREEN}{name} is calling{Style.RESET_ALL}')

    # Form the header and add a random User-Agent
    if not headers:
        headers = {'User-Agent': random.choice(config['user_agents'])}
    else:
        headers['User-Agent'] = random.choice(config['user_agents'])

    # Send the HTTP request based on the given method
    try:
        # Run the GET request
        if method == 'GET':
            request = requests.get(
                url,
                headers=headers,
                timeout=config['delay']['requests_timeout']
            )
        # Run the POST request
        elif method == 'POST':
            request = requests.post(
                url,
                cookies=cookies,
                data=json.dumps(data),
                headers=headers,
                timeout=config['delay']['requests_timeout']
            )

        # Get the status code
        status_code = int(request.status_code)

        # Get the history
        history = request.history

        # Get the headers
        http_headers = request.headers

        # Get the HTTP version
        version = request.raw.version

        # Get the results if there is the type is either 'text', 'xml', or 'json'
        if resp_type == 'json':
            content = json.loads(request.text)
        elif resp_type == 'text' or resp_type == 'xml':
            content = request.text
        else:
            content = request

    # region: Exceptions
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
    # endregion: Exceptions

    # Return results
    return [
        content,
        status_code,
        history,
        http_headers,
        version
    ]
