#!/usr/bin/env python

from colorama import Fore, Style
from datetime import datetime
import dns.resolver
import random
import re
import json
import sys, os
import requests
from config import config


# get the raw date and its format, then covert it to a date object and print it in defined format
def date_formatter(raw_date, raw_date_format):
    return datetime.strptime(raw_date, raw_date_format).strftime(config['date_format'])


# get the json and check if the key exist
# it just checks up to 2nd level
def json_key_checker(json_name, json_key1, json_key2):
    if json_key1 in json_name:
        if json_key2 != '' and json_key2 in json_name[json_key1]:
            return json_name[json_key1][json_key2]
        else:
            return json_name[json_key1]
    else:
        return ''


# make the json flat
# i.e. {'a': {'b': 1, 'c': {'d': 2}}, 'e': 3}
# ===> {'a_b': 1, 'a_c_d': 2, 'e': 3}
def flat_json(a_key, json, results):
    joiner = config['output']['csv']['header_joiner']
    # iterate over keys & values recursively
    for key, value in json.items():
        # check if the json contains another jason (is nested)
        if isinstance(value, dict):
            a_key += key + joiner
            # run the function recursively
            flat_json(a_key, value, results)
            # sanitize the aggregated key
            a_key = a_key[:-len(key + joiner)]
        else:
            a_key += key
            results[a_key] = value
            # sanitize the aggregated key
            a_key = a_key[:-len(key)]
    # return results
    return results


# it will get the json, make it flat, and return keys and values in separate lists
# it also checks if it is asked (in the config file) to be in the CSV file or not
# if not, it will be ignored from the output lists
def csv_maker(json, config_json):
    keys = list()
    values = list()

    # make the json flat
    json = flat_json('', json, {})
    if config_json:
        config_json = flat_json('', config_json, {})

    # iterate over keys & values
    for key, value in json.items():
        # check if it is True in config file to be written in CSV or not
        if (key in config_json) and config_json[key]:
            keys.append(key)
            values.append(value)
    
    # return results
    return [
        keys,
        values
    ]


# print on the terminal (STDOUT) and the file
all_prints = ''
def printer(term):
    # load the global variable
    global all_prints
    
    # print the term on the terminal (STDOUT)
    print(term)
    
    # sanitize the term to be able to save it into a file
    term = term.replace('[0m', '').replace('[30m', '')
    term = term.replace('[31m', '').replace('[32m', '').replace('[33m', '').replace('[34m', '').replace('[35m', '')
    term = term.replace('[36m', '').replace('[37m', '').replace('[38m', '').replace('[39m', '').replace('[40m', '')
    term = term.replace('[41m', '').replace('[42m', '').replace('[43m', '').replace('[44m', '').replace('[45m', '')
    term = term.replace('[46m', '').replace('[47m', '').replace('[48m', '').replace('[49m', '').replace('[50m', '')
    
    # save the term in a global variable to save in a file later
    all_prints += term + '\n'


# a sub-function to parse the result of the regex find_all function
def re_position(term, pos):
    return term[pos] if (len(term) > pos) else ''


# sanitize the domain name and strip schema from it
def domain_sanitizer(domain):
    # a regex to parse URL
    try:
        regex = r'(?i)(?P<all>(?P<sub_domain>[^\s~`!@#$%^&*()_+=,.?:;\'"{}\|\[\]\/\\]+\.)*(?P<domain>[^\s~`!@#$%^&*()_+=,.?:;\'"{}\|\[\]\/\\]+)(?P<tld>\.[^\s~`!@#$%^&*()\-_+=,.?:;\'"{}\|\[\]\/\\0-9]{2,}))'
        domain = re.search(regex, domain).group('all')
        
        # convert it to lowercase
        domain = domain.lower()
    except:
        domain = ''
    
    # return sanitized domain
    return domain


# get the details of the exception
def exception_report():
    exception_type, exception_obj, exception_tb = sys.exc_info()
    file_name = os.path.split(exception_tb.tb_frame.f_code.co_filename)[1]
    return [
        str(exception_type),
        str(exception_obj),
        str(exception_tb),
        str(exception_tb.tb_lineno),
        str(file_name)
    ]


# run functions use "requests" and "json" modules
def run_requests(url, headers, type, name, print_args):
    results = list()
    status_code = 0
    history = list()

    # form the header
    if not headers:
        headers = {'User-Agent': random.choice(config['user_agents'])}
    try:
        # run the request
        request = requests.get(url, headers=headers)

        # get the status code
        status_code = request.status_code

        # get the history
        history = request.history

        # get the headers
        headers = request.headers

        # get the results if there is the type is either 'text' or 'json'
        if type == 'json':
            results = json.loads(request.text)
        elif type == 'text':
            results = request.text
        else:
            results = request

    # exceptions
    except requests.exceptions.HTTPError:
        if print_args[0]:
            ex = exception_report()
            printer(print_args[1] + Fore.RED + 'Error in loading the {0} URL page.'.format(name) + Style.RESET_ALL)
            if config['verbosity'] >= 4:
                printer(print_args[2] + 'ERROR: ' + Fore.MAGENTA + ex[0] + ' → ' + ex[4] + ':' + ex[3] + Fore.RED + '  ' + ex[1] + Style.RESET_ALL)
    except requests.exceptions.ConnectionError:
        if print_args[0]:
            ex = exception_report()
            printer(print_args[1] + Fore.RED + 'Error in establishing the connection to the {0} URL.'.format(name) + Style.RESET_ALL)
            if config['verbosity'] >= 4:
                printer(print_args[2] + 'ERROR: ' + Fore.MAGENTA + ex[0] + ' → ' + ex[4] + ':' + ex[3] + Fore.RED + '  ' + ex[1] + Style.RESET_ALL)
    except requests.exceptions.Timeout:
        if print_args[0]:
            ex = exception_report()
            printer(print_args[1] + Fore.RED + 'Timeout error while opening {0} URL.'.format(name) + Style.RESET_ALL)
            if config['verbosity'] >= 4:
                printer(print_args[2] + 'ERROR: ' + Fore.MAGENTA + ex[0] + ' → ' + ex[4] + ':' + ex[3] + Fore.RED + '  ' + ex[1] + Style.RESET_ALL)
    except requests.exceptions.RequestException:
        if print_args[0]:
            ex = exception_report()
            printer(print_args[1] + Fore.RED + 'Error in reading the data from the {0} URL.'.format(name) + Style.RESET_ALL)
            if config['verbosity'] >= 4:
                printer(print_args[2] + 'ERROR: ' + Fore.MAGENTA + ex[0] + ' → ' + ex[4] + ':' + ex[3] + Fore.RED + '  ' + ex[1] + Style.RESET_ALL)
    except requests.exceptions.TooManyRedirects:
        if print_args[0]:
            ex = exception_report()
            printer(print_args[1] + Fore.RED + 'The provided {0} URL does not seem correct.'.format(name) + Style.RESET_ALL)
            if config['verbosity'] >= 4:
                printer(print_args[2] + 'ERROR: ' + Fore.MAGENTA + ex[0] + ' → ' + ex[4] + ':' + ex[3] + Fore.RED + '  ' + ex[1] + Style.RESET_ALL)
    except json.decoder.JSONDecodeError:
        if print_args[0]:
            ex = exception_report()
            printer(print_args[1] + Fore.RED + 'Error in reading the JSON data retrieved from the {0} call.'.format(name) + Style.RESET_ALL)
            if config['verbosity'] >= 4:
                printer(print_args[2] + 'ERROR: ' + Fore.MAGENTA + ex[0] + ' → ' + ex[4] + ':' + ex[3] + Fore.RED + '  ' + ex[1] + Style.RESET_ALL)
    except ValueError:
        if print_args[0]:
            ex = exception_report()
            printer(print_args[1] + Fore.RED + 'No Result is found or there was an error for {0}.'.format(name) + Style.RESET_ALL)
            if config['verbosity'] >= 4:
                printer(print_args[2] + 'ERROR: ' + Fore.MAGENTA + ex[0] + ' → ' + ex[4] + ':' + ex[3] + Fore.RED + '  ' + ex[1] + Style.RESET_ALL)
    except Exception:
        if print_args[0]:
            ex = exception_report()
            printer(print_args[1] + Fore.RED + 'An unknown error is ocurred while running {0}.'.format(name) + Style.RESET_ALL)
            if config['verbosity'] >= 4:
                printer(print_args[2] + 'ERROR: ' + Fore.MAGENTA + ex[0] + ' → ' + ex[4] + ':' + ex[3] + Fore.RED + '  ' + ex[1] + Style.RESET_ALL)

    # return results
    return [
        results,
        status_code,
        history,
        headers
    ]


# resolve the DNS
def dns_resolver(domain, record, print_args):
    results = list()
        
    # set the DNS server
    dns.resolver.Resolver().nameservers = config['dns']['dns_servers']

    try:
        answers = dns.resolver.resolve(domain, record)
        for answer in answers: 
            results.append(str(answer))

    except dns.resolver.NoAnswer:
        if print_args[0]:
            ex = exception_report()
            printer(print_args[1] + Fore.RED + 'The DNS query "{0}" for "{1}" returned no answer.'.format(record, domain) + Style.RESET_ALL)
            if config['verbosity'] >= 4:
                printer(print_args[2] + 'ERROR: ' + Fore.MAGENTA + ex[0] + ' → ' + ex[4] + ':' + ex[3] + Fore.RED + '  ' + ex[1] + Style.RESET_ALL)
    except dns.resolver.NXDOMAIN:
        if print_args[0]:
            ex = exception_report()
            printer(print_args[1] + Fore.RED + 'QUERY "{0}": The domain "{1}" does not exist.'.format(record, domain) + Style.RESET_ALL)
            if config['verbosity'] >= 4:
                printer(print_args[2] + 'ERROR: ' + Fore.MAGENTA + ex[0] + ' → ' + ex[4] + ':' + ex[3] + Fore.RED + '  ' + ex[1] + Style.RESET_ALL)
    except dns.resolver.NoNameservers:
        if print_args[0]:
            ex = exception_report()
            printer(print_args[1] + Fore.RED + 'All nameservers failed to answer the DNS query "{0}" for "{1}".'.format(record, domain) + Style.RESET_ALL)
            if config['verbosity'] >= 4:
                printer(print_args[2] + 'ERROR: ' + Fore.MAGENTA + ex[0] + ' → ' + ex[4] + ':' + ex[3] + Fore.RED + '  ' + ex[1] + Style.RESET_ALL)
    except Exception:
        if print_args[0]:
            ex = exception_report()
            printer(print_args[1] + Fore.RED + 'QUERY "{0}": No result is found for "{1}" or there was an error.'.format(record, domain) + Style.RESET_ALL)
            if config['verbosity'] >= 4:
                printer(print_args[2] + 'ERROR: ' + Fore.MAGENTA + ex[0] + ' → ' + ex[4] + ':' + ex[3] + Fore.RED + '  ' + ex[1] + Style.RESET_ALL)

    # return the list of the DNS results
    return list(set(results))
