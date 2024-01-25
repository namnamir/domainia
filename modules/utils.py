#!/usr/bin/env python

from datetime import datetime
from usp.tree import sitemap_tree_for_homepage

from config import config


# get the raw date and its format, then covert it to a date object and print it
# in defined format
def date_formatter(date, date_format):
    # if the input 'date' is a string date not a date object
    if date_format:
        return datetime.strptime(date, date_format).strftime(config['date_format'])
    # if the input 'date' is a date object
    else:
        return date.strftime(config['date_format'])


# a function to return the value of a JSON key if it exists
def json_value(json, key):
    value = ''
    if key in json:
        if json[key] == 'false':
            value = False
        elif json[key] == 'true':
            value = True
        elif json[key] in ('null', 'none', None):
            value = ''
        else:
            value = json[key]

    # return value
    return value


# get the json and check if the key exist
# it is a recursive function that can check any values given in the list of
# keys in keys
def json_key_checker(json, keys):
    if keys[0] in json:
        if len(json) > 1 and keys[1] != '' and keys[1] in json[keys[0]]:
            keys.pop(0)
            json_key_checker(json[keys[0]], keys)
        else:
            return json[keys[0]]
    else:
        return ''


# a sub-function to parse the result of the regex find_all function
def re_position(term, pos):
    return term[pos] if (len(term) > pos) else ''


# print on the terminal (STDOUT) and the file
# all_prints = ''
# def printer(term):
#     # load the global variable
#     global all_prints

#     # print the term on the terminal (STDOUT)
#     print(term)

#     # strip styles from the term to be able to save it into a file
#     term = term.replace('\x1B[0m', '').replace('\x1B[30m', '').replace('\x1B[31m', '')
#     term = term.replace('\x1B[32m', '').replace('\x1B[33m', '').replace('\x1B[34m', '')
#     term = term.replace('\x1B[35m', '').replace('\x1B[36m', '').replace('\x1B[37m', '')
#     term = term.replace('\x1B[38m', '').replace('\x1B[39m', '').replace('\x1B[40m', '')
#     term = term.replace('\x1B[41m', '').replace('\x1B[42m', '').replace('\x1B[43m', '')
#     term = term.replace('\x1B[44m', '').replace('\x1B[45m', '').replace('\x1B[46m', '')
#     term = term.replace('\x1B[47m', '').replace('\x1B[48m', '').replace('\x1B[49m', '')
#     term = term.replace('\x1B[50m', '')

#     # save the term in a global variable to save in a file later
#     all_prints += term + '\n'

# sanitize the domain name and strip schema from it
# def domain_sanitizer(domain):
#     try:
#         # use urlparse() to split the URL into its component parts
#         parsed_url = urlparse(domain)

#         # check if netloc is empty (i.e., domain does not contain schema)
#         if not parsed_url.netloc:
#             domain = 'http://' + domain
#             parsed_url = urlparse(domain)

#         # form the components of the URL
#         url_components = [
#             parsed_url.netloc.lower(),
#             parsed_url.path,
#             parsed_url.params,
#             parsed_url.query,
#             parsed_url.fragment
#         ]

#     except Exception as error:
#         # handle any exceptions that may be raised
#         texts = [
#             f'Error in parsing the domain "{domain}".',
#             error
#         ]
#         print_error('exception', texts)
#         url_components = ['', '', '', '', '']

#     # return sanitized domain
#     return url_components


# get the details of the exception
# def exception_report():
#     # get error details
#     exception_type, exception_value, exception_trace = sys.exc_info()
#     # get the file location
#     file_name = os.path.split(exception_trace.tb_frame.f_code.co_filename)[1]
#     # get the line number
#     line_no = exception_trace.tb_lineno
#     # get the trace back to the source
#     exception_trace = ''.join(traceback.format_tb(exception_trace))
#     # return results
#     return [
#         str(exception_type),
#         str(exception_value),
#         str(exception_trace),
#         str(line_no),
#         str(file_name)
#     ]


# print the errors related to the exceptions, based on verbosity
# flag  = "exception" or True to print based on verbosity, and
#         False to print nothing as the error
# texts = ["text for verbosity 1", ..., "text for verbosity 5"]
# def print_error(flag, texts):
#     verbosity_1 = '      │        ├──🛑 '
#     verbosity_2 = '      │        │     '
#     verbosity_3 = '      │        │     '
#     verbosity_4 = '      │        │     '
#     verbosity_5 = '      │        │     '

#     # if flag is True/exception and verbosity is not 0 (or False)
#     if flag and config['verbosity']:
#         # print error messages for verbosity 1 (-v)
#         if config['verbosity'] >= 1 and len(texts) >= 1 and texts[0]:
#             printer(verbosity_1 + Fore.RED + texts[0] + Style.RESET_ALL)
#         # print error messages for verbosity 2 (-vv)
#         if config['verbosity'] >= 2 and len(texts) >= 2 and texts[1]:
#             printer(verbosity_2 + Fore.RED + texts[1] + Style.RESET_ALL)
#         # print error messages for verbosity 3 (-vvv)
#         if config['verbosity'] >= 3 and len(texts) >= 3 and texts[2]:
#             printer(verbosity_3 + Fore.RED + texts[2] + Style.RESET_ALL)
#         # print error messages for verbosity 4 (-vvvv)
#         if config['verbosity'] >= 4 and len(texts) >= 4 and texts[3]:
#             printer(verbosity_4 + Fore.RED + texts[3] + Style.RESET_ALL)
#         # print error messages for verbosity 5 (-vvvvv)
#         if config['verbosity'] >= 5:
#             if len(texts) >= 5 and texts[4]:
#                 printer(verbosity_5 + Fore.RED + texts[4] + Style.RESET_ALL)
#             # in case, it is an exception error message
#             if flag == 'exception':
#                 ex = exception_report()
#                 printer(
#                     verbosity_5 + 'Exception Message: ' + Fore.MAGENTA +
#                     ex[0] + ' ➜ ' + ex[4] + ':' + ex[3] + Fore.RED + ' == ' +
#                     ex[2] + ' ⚊ ' + ex[1] + Style.RESET_ALL
#                 )


# get the internal links based on the sitemap
# import logging
# def load_sitemap(domain):
    # a variable to store internal pages
    links = list()

    # disable logging of USP
    logging.getLogger('usp').disabled = True
    logging.getLogger('usp.helpers').disabled = True
    logging.getLogger('usp.fetch_parse').disabled = True
    logging.getLogger('usp.tree').disabled = True

    # get the sitemap
    sitemap = sitemap_tree_for_homepage(f'http://{domain}')

    # generate the internal page links
    for page in sitemap.all_pages():
        links.append(page.url)

    # return the results
    return links


# send the HTTP request based on the method and get the results
# in text or JSON format
# def run_requests(method, url, cookies, data, headers, type, name):
#     # some variables to store results
#     results = list()
#     history = list()
#     http_headers = list()
#     version = ''
#     status_code = 0

#     # print the subtitle based on the the variable "name"
#     if config['verbosity'] >= 2 and name:
#         printer(
#             '      │        ├□ ' + Fore.GREEN +
#             f'{name} is calling' + Style.RESET_ALL
#         )

#     # form the header and add a random User-Agent
#     if not headers:
#         headers = {'User-Agent': random.choice(config['user_agents'])}
#     else:
#         headers['User-Agent'] = random.choice(config['user_agents'])

#     # send the HTTP request based on the given method
#     try:
#         # run the GET request
#         if method == 'GET':
#             request = requests.get(
#                 url,
#                 headers=headers,
#                 timeout=config['delay']['requests_timeout']
#             )
#         # run the POST request
#         elif method == 'POST':
#             request = requests.post(
#                 url,
#                 cookies=cookies,
#                 data=json.dumps(data),
#                 headers=headers,
#                 timeout=config['delay']['requests_timeout']
#             )

#         # get the status code
#         status_code = int(request.status_code)

#         # get the history
#         history = request.history

#         # get the headers
#         http_headers = request.headers

#         # get the HTTP version
#         version = request.raw.version

#         # get the results if there is the type is either 'text', 'xml', or 'json'
#         if type == 'json':
#             results = json.loads(request.text)
#         elif type == 'text' or type == 'xml':
#             results = request.text
#         else:
#             results = request

#     # exceptions
#     except requests.exceptions.SSLError:
#         texts = [
#             f'The URL {url} cannot be opened due to an SSL error.',
#             '',
#             f'Status Code: {status_code}  -  API call URL: {url}'
#         ]
#         print_error('exception', texts)
#     except requests.exceptions.TooManyRedirects:
#         texts = [
#             f'The provided {name} URL does not seem correct.',
#             '',
#             f'Status Code: {status_code}  -  API call URL: {url}'
#         ]
#         print_error('exception', texts)
#     except requests.exceptions.HTTPError:
#         texts = [
#             f'Error in loading the {name} URL page.',
#             '',
#             f'Status Code: {status_code}  -  API call URL: {url}'
#         ]
#         print_error('exception', texts)
#     except requests.exceptions.ConnectionError:
#         texts = [
#             f'Error in establishing the connection to the {name} URL.',
#             '',
#             f'Status Code: {status_code}  -  API call URL: {url}'
#         ]
#         print_error('exception', texts)
#     except requests.exceptions.Timeout:
#         texts = [
#             f'Timeout error while opening {name} URL.',
#             '',
#             f'Status Code: {status_code}  -  API call URL: {url}'
#         ]
#         print_error('exception', texts)
#     except requests.exceptions.RequestException:
#         texts = [
#             f'Error in reading the data from the {name} URL.',
#             '',
#             f'Status Code: {status_code}  -  API call URL: {url}'
#         ]
#         print_error('exception', texts)
#     except json.decoder.JSONDecodeError:
#         texts = [
#             f'Error in reading the JSON data retrieved from the {name} call.',
#             '',
#             f'Status Code: {status_code}  -  API call URL: {url}'
#         ]
#         print_error('exception', texts)
#     except ValueError:
#         texts = [
#             f'No Result is found or there was an error for {name}.',
#             '',
#             f'Status Code: {status_code}  -  API call URL: {url}'
#         ]
#         print_error('exception', texts)
#     except Exception:
#         texts = [
#             f'An unknown error is ocurred while running {name}.',
#             '',
#             f'Status Code: {status_code}  -  API call URL: {url}'
#         ]
#         print_error('exception', texts)

#     # return results
#     finally:
#         return [
#             results,
#             status_code,
#             history,
#             http_headers,
#             version
#         ]
