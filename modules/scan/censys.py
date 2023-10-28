#!/usr/bin/env python


"""
    ### Vulnerability Scanner: Censys API

    This function gets the IP address of the host and returns the list of
    services on the host (open ports) and banner grabbing.

    Read more: - https://search.censys.io/api#/hosts/viewHost

    # Input:  - a single domain name or IP address
              - the type of the asset that needs to be assessed
    # Output: - either a set contains detailed related-IPs to the given domain name
              - or a set contains details about a single IP
"""


from config import config
from modules.utils import url_opener, error_printer, json_key_checker


def Censys(bacon, type):
    # variables to store results
    ip_details = dict()
    related_ips = set()

    # for the HTTP headers to send to Censys
    headers = {
        'Authorization': f'Basic {config["api"]["censys"]["api_key"]}',
        'accept': 'application/json'
    }

    # get the results in JSON from Censys based on the type
    if type == 'domain':
        url = config['api']['censys']['url_domain'].format(bacon)
        results = url_opener('GET', url, '', '', headers, 'json', 'Censys API')[0]

        # if the API call returns data
        if results['code'] == 200:
            # get the list of IP addresses and open ports
            for details in results['result']['hits']:
                ports = set()
                technologies = set()

                # iterate over the details of each IP
                for service in details['services']:
                    ports.add(
                        {
                            'port': json_key_checker(service, ['port']),
                            'status': 'open',
                            'protocol': json_key_checker(
                                service, ['transport_protocol']
                            ),
                            'service': json_key_checker(service, ['service_name']),
                        }
                    )
                # get the list of technologies
                technologies.add(
                    {
                        'name': json_key_checker(
                            ip_details, ['operating_system', 'product']
                        ),
                        'version': '',
                    }
                )

                # form the related_ips
                related_ips.add(
                    {
                        'ip': details['ip'],
                        'ports': ports,
                        'technologies': technologies,
                        'reverse_dns': json_key_checker(
                            details, ['dns', 'reverse_dns', 'names']
                        ),
                    }
                )
        else:
            errors = [
                'There is an error in getting the data from Censys',
                '',
                f'{results["status"]} ({results["code"]}): {results["error"]}',
                '',
                ''
            ]
            error_printer(True, errors)

        # return gathered data
        return related_ips

    elif type == 'ip':
        url = config['api']['Censys']['url_ip'].format(bacon)
        results = url_opener('GET', url, '', '', headers, 'json', 'Censys API')[0]

        # if the API call returns data
        if results['code'] == 200:
            ports = set()
            technologies = set()

            # iterate over the details of the IP
            for service in details['result']['services']:
                ports.add(
                    {
                        'port': json_key_checker(service, ['port']),
                        'status': 'open',
                        'protocol': json_key_checker(service, ['transport_protocol']),
                        'service': json_key_checker(service, ['service_name']),
                    }
                )
                # get the list of technologies
                for tech in service['software']:
                    technologies.add(
                        {
                            'name': json_key_checker(tech, ['product']),
                            'version': '',
                        }
                    )

            # form the related_ips
            ip_details.add(
                {
                    'ip': details['ip'],
                    'ports': ports,
                    'technologies': technologies,
                    'reverse_dns': json_key_checker(
                        details, ['dns', 'reverse_dns', 'names']
                    ),
                    'tags': []
                }
            )
        else:
            errors = [
                'There is an error in getting the data from Censys',
                '',
                f'{results["status"]} ({results["code"]}): {results["error"]}',
                '',
                ''
            ]
            error_printer(True, errors)

        # return gathered data
        return ip_details
