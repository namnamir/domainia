#!/usr/bin/env python

from time import sleep
from colorama import Fore, Style

from config import config
from modules.utils import json_value
from modules.utilities.url_opener import url_opener
from modules.utilities.printer import printer


def ssl_labs(domain):
    """
    ### SSL Certificates: SSL Labs

    This function uses the SSL Labs API to get the certificate's details.
    It, first, checks if there is any existing details. If there is any, loads
    it, if not, schedules the analysis. It also gets vulnerability assessments
    done by SSL Labs.
    # Read more: https://github.com/ssllabs/ssllabs-scan/blob/master/ssllabs-api-docs-v3.md

    # Input:  - a single domain name
    # Output: - a dictionary contains SSL certificate details
    """
    # a variable to store cert info
    cert_info = dict()
    # set the print arguments for the function "except_error_print"
    print_args = [True, '      │        ├──■ ', '      │        ├──■■ ']

    url = config['api']['ssl_labs']['url_status'].format(domain)

    # get the certificate from SSL Labs
    printer('      │        ├□ ' + Fore.GREEN + f'SSL Labs API is calling ({url})' + Style.RESET_ALL)

    # check if the certificate is in SSL Labs database
    # if not, run the scan and wait
    while True:
        # get the status
        json_data = url_opener('GET', url, '', '', '', 'json', 'Initial SSL Labs API')[0]
        status = json_data['status']

        # check the status
        if status in ('DNS', 'IN_PROGRESS'):
            printer('      │        ├──■ ' + Fore.YELLOW + f'Parsing SSL Certificate is not ready ({status})' + Style.RESET_ALL)
            printer('      │        └──■■ ' + Fore.YELLOW + json_data['statusMessage'] + Style.RESET_ALL)
            # wait for a certain time
            sleep(config['delay']['ssl_labs'])
            continue
        elif status == 'READY':
            break
        elif status == 'ERROR':
            printer('      │        ├──■ ' + Fore.RED + f'Error in parsing SSL Certificate ({status})' + Style.RESET_ALL)
            printer('      │        └──■■ Error: ' + Fore.RED + json_data['statusMessage'] + Style.RESET_ALL)
            return cert_info

    url = config['api']['ssl_labs']['url_detail'].format(domain, status['endpoints'][0]['ipAddress'])
    results = url_opener('GET', url, '', '', '', 'json', 'SSL Labs API')[0]['details']

    # continue only if there is any result
    if results:
        #initiate the result
        cert_info['control'] = dict()
        cert_info['vulnerability'] = dict()
        cert_info['control']['protocol'] = list()
        cert_info['control']['suite'] = list()

        cert_info['server_signature'] = json_value(results, 'serverSignature')

        cert_info['control']['grade'] = status['grade']

        # iterate over the suites and store them in a list
        for suites in results['suites']:
            cert_info['control']['protocol'].append(suites['protocol'])
            cert_info['control']['suite'][suites['protocol']] = list()
            for suite in suites['list']:
                # get the suite security flag
                flag = config['api']['ssl_labs']['suite_flag'][suite['q']] if suite['q'] else ''
                cert_info['control']['suite'][results['protocol']].append(flag + suite['name'])

        # get security controls out of certificate
        cert_info['control']['www_reachable'] = json_value(results, 'prefixDelegation')
        cert_info['control']['non_www_reachable'] = json_value(results, 'nonPrefixDelegation')
        cert_info['control']['compression'] = json_value(results, 'compressionMethods')
        cert_info['control']['npn'] = json_value(results, 'npnProtocols') if json_value(results, 'supportsNpn') else False
        cert_info['control']['alpn'] = json_value(results, 'alpnProtocols') if json_value(results, 'supportsAlpn') else False
        cert_info['control']['session_ticket'] = config['api']['ssl_labs']['session_resumption'][json_value(results, 'sessionTickets')]
        cert_info['control']['ocsp_stapling'] = json_value(results, 'ocspStapling')
        cert_info['control']['sni_required'] = json_value(results, 'sniRequired')
        cert_info['control']['rc4'] = json_value(results, 'supportsRc4')
        cert_info['control']['logjam'] = json_value(results, 'logjam')
        cert_info['control']['dhYsReuse'] = json_value(results, 'dhYsReuse')

        # get any vulnerabilities out of certificate
        cert_info['vulnerability']['beast'] = json_value(results, 'vulnBeast')
        cert_info['vulnerability']['heart_bleed'] = json_value(results, 'heartbleed')
        cert_info['vulnerability']['heartbeat'] = json_value(results, 'heartbeat')
        cert_info['vulnerability']['poodle'] = json_value(results, 'poodle')
        cert_info['vulnerability']['freak'] = json_value(results, 'freak')
        cert_info['vulnerability']['drown'] = json_value(results, 'drownVulnerable')
        cert_info['vulnerability']['drown_host'] = json_value(results, 'drownHosts')
        cert_info['vulnerability']['ecdh_parameter_reuse'] = json_value(results, 'ecdhParameterReuse')
        cert_info['vulnerability']['renegotiation'] = config['api']['ssl_labs']['renegotiation'][json_value(results, 'renegSupport')]
        cert_info['vulnerability']['session_resumption'] = config['api']['ssl_labs']['session_resumption'][json_value(results, 'sessionResumption')]
        cert_info['vulnerability']['openssl_ccs'] = config['api']['ssl_labs']['openssl_ccs'][json_value(results, 'openSslCcs')]
        cert_info['vulnerability']['openssl_lucky_m20'] = config['api']['ssl_labs']['openssl_lucky_m20'][json_value(results, 'openSSLLuckyMinus20')]
        cert_info['vulnerability']['ticket_bleed'] = config['api']['ssl_labs']['ticket_bleed'][json_value(results, 'ticketbleed')]
        cert_info['vulnerability']['bleichenbacher'] = config['api']['ssl_labs']['bleichenbacher'][json_value(results, 'bleichenbacher')]
        cert_info['vulnerability']['zombie_poodle'] = config['api']['ssl_labs']['zombie_poodle'][json_value(results, 'zombiePoodle')]
        cert_info['vulnerability']['golden_doodle'] = config['api']['ssl_labs']['golden_doodle'][json_value(results, 'goldenDoodle')]
        cert_info['vulnerability']['zero_length_padding_oracle'] = config['api']['ssl_labs']['zero_length_padding_oracle'][json_value(results, 'zeroLengthPaddingOracle')]
        cert_info['vulnerability']['sleeping_poodle'] = config['api']['ssl_labs']['sleeping_poodle'][json_value(results, 'sleepingPoodle')]
        cert_info['vulnerability']['poodle_tls'] = config['api']['ssl_labs']['poodle_tls'][json_value(results, 'poodleTls')]

    return cert_info
