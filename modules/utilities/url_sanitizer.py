from urllib.parse import urlparse
from typing import List, Union

from modules.utilities.error_printer import error_printer


def url_sanitizer(url: str) -> List[Union[str, str, str]]:
    """
    this function sanitizes the given url decomposes it into all possible components
    including scheme, path, parameters, queries, fragments, etc.

    An example of a full URL:
        'http://user:pass@NetLoc:80/path;parameters/path2;parameters2?query=argument#fragment'

    All components:
        parsed_url.scheme,
        parsed_url.hostname,        # (sub)domain; it is 'netloc' in lower case
        parsed_url.netloc.lower(),  # (sub)domain
        parsed_url.path,
        parsed_url.params,
        parsed_url.query,
        parsed_url.fragment,
        parsed_url.username,
        parsed_url.password,
        parsed_url.port

    Args:
        url (str): URL string.

    Returns:
        List[str, str, str]: List of the composed full URL, the hostname, and URN.

    Raises:
        Exception: Any exception that may be raised during URL parsing.
    """
    try:
        # Use urlparse() to split the URL into its component parts
        parsed_url = urlparse(url)

        # Check if scheme is empty
        if not parsed_url.scheme:
            url = "http://" + url
            parsed_url = urlparse(url)

    except Exception as error:
        # Handle any exceptions that may be raised
        texts = [
            f'Error in parsing the domain "{url}".',
            error
        ]
        error_printer("exception", texts)
        return ["", ""]

    # Return the sanitized decomposed url
    return [
        parsed_url.geturl(),
        parsed_url.hostname,
        parsed_url.geturl().replace(parsed_url.scheme + "://", "")
    ]
