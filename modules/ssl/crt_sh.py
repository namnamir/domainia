#!/usr/bin/env python

import re
from colorama import Fore, Style

from config import config
from modules.utils import re_position
from modules.utils import date_formatter
from modules.utilities.printer import printer
from modules.utilities.url_opener import url_opener


def crt_sh(domain):
    """
    ### SSL Certificates: crt.sh API

    This function get the latest certificate details from crt.sh.
    It first gets the list of all certificates, sort them by ID, and load the
    latest certificate (based on ID). Afterwards, parse the page using RE.

    # Input:  - a single domain name
    # Output: - a dictionary contains SSL certificate details
    """
    # a variable to store cert info
    cert_info = dict()
    # get the date format of the crt.sh from the config file
    date_format = config['api']['crt_sh']['date_format']

    # download the certificate page on CRT
    url = config['api']['crt_sh']['url_all'].format(domain)
    printer('      │        ├□ ' + Fore.GREEN + f'CRT.sh API is calling ({url})' + Style.RESET_ALL)
    results = url_opener('GET', url, '', '', '', 'json', 'Crt.sh API')[0]

    # continue only if there is any result
    if results:
        # sort certificates by ID to get the details of the latest one
        results = sorted(results, key=lambda k: k['id'], reverse=True)

        url = config['api']['crt_sh']['url_single'].format(results[0]['id'])
        cert = url_opener('GET', url, '', '', '', 'text', 'Crt.sh API')[0]

        # fix the HTML format of the space
        cert = cert.replace('&nbsp;', ' ')

        # get the info of the latest certificate
        cert_info['signature'] = re_position(re.findall(r"Signature Algorithm[ :]*(.*?)<BR>", cert), 0)
        cert_info['serial_number'] = re_position(re.findall(r"Serial Number[ :]<\/A><BR>[ =]*(.*?)<BR>", cert), 0)
        cert_info['validity']['issue_date'] = date_formatter(re_position(re.findall(r"Not Before[ =:]*(.*?)<BR>", cert), 0), date_format)
        cert_info['validity']['expiration_date'] = date_formatter(re_position(re.findall(r"Not After[ =:]*(.*?)<BR>", cert), 0), date_format)
        cert_info['fingerprint']['sha256'] = re_position(re.findall(r"search.censys.io/certificates/(.*?)\">", cert), 0)
        cert_info['issuer']['common_name'] = re_position(re.findall(r"commonName[ =]*(.*?)<BR>", cert), 0)
        cert_info['issuer']['organization_name'] = re_position(re.findall(r"organizationName[ =]*(.*?)<BR>", cert), 0)
        cert_info['issuer']['organization_unit_name'] = re_position(re.findall(r"organizationalUnitName[ =]*(.*?)<BR>", cert), 0)
        cert_info['issuer']['country'] = re_position(re.findall(r"countryName[ =]*(.*?)<BR>", cert), 0)
        cert_info['issuer']['state'] = re_position(re.findall(r"stateOrProvinceName[ =]*(.*?)<BR>", cert), 0)
        cert_info['issuer']['city'] = re_position(re.findall(r"localityName[ =]*(.*?)<BR>", cert), 0)
        cert_info['subject']['common_name'] = re_position(re.findall(r"commonName[ =]*(.*?)<BR>", cert), 1)
        cert_info['subject']['organization_name'] = re_position(re.findall(r"organizationName[ =]*(.*?)<BR>", cert), 1)
        cert_info['subject']['organization_unit_name'] = re_position(re.findall(r"organizationalUnitName[ =]*(.*?)<BR>", cert), 1)
        cert_info['subject']['country'] = re_position(re.findall(r"countryName[ =]*(.*?)<BR>", cert), 1)
        cert_info['subject']['state'] = re_position(re.findall(r"stateOrProvinceName[ =]*(.*?)<BR>", cert), 1)
        cert_info['subject']['city'] = re_position(re.findall(r"localityName[ =]*(.*?)<BR>", cert), 1)
        cert_info['control']['lint'] = re.findall(r"<SPAN[\sclass=\"notice|warning|fatal|error\"]*>\s*(.*?)\s*</SPAN>", cert)

    return cert_info
