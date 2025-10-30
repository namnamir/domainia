#!/usr/bin/env python

import dns.resolver
import requests
import random
from config import config
from modules.utilities.url_sanitizer import url_sanitizer


# check if the subdomain is vulnerable to the takeover by misconfiguration in CNAME
# results schema:
#       0: no subdomain takeover vulnerability
#       1: subdomain takeover vulnerability
#       2: there was an error
def subdomain_takeover(rdata):
    # sanitize the rdata
    rdata = url_sanitizer(rdata)[1]

    # iterate over the CNAMEs defined in the config file
    for cname in config['cnames']:
        flag = True
        headers = {'User-Agent': random.choice(config['user_agents'])}
        f_type = config['cnames'][cname]['f_type'].lower()

        # if the found CNAME target is in our list
        if cname in rdata:
            try:
                # act based on the type of the fingerprint
                if f_type == 'content':
                    try:
                        req = requests.get('https://' + rdata, headers=headers).text
                    # in case the scheme is not HTTPS
                    except requests.exceptions.InvalidSchema:
                        req = requests.get('http://' + rdata, headers=headers).text
                        # return error ocurred
                        return 2
                    except Exception:
                        flag = False

                    # if the page is loaded and the fingerprint is found
                    if not flag:
                        fingerprint = config['cnames']['cname']['fingerprint'].lower()
                        if fingerprint in req:
                            # return potential subdomain takeover
                            return 1
                        else:
                            # return no subdomain takeover vulnerability
                            return 0
                # if the error is: the domain doesn't exist
                elif f_type == 'nxdomain':
                    try:
                        dns.resolver.resolve(rdata, 'A')
                        # return no subdomain takeover vulnerability
                        return 0
                    except dns.resolver.NXDOMAIN:
                        # return potential subdomain takeover
                        return 1
                    except Exception:
                        # return error ocurred
                        return 2
                # if it shows 404 HTTP error
                elif f_type == 'http_status':
                    try:
                        req = requests.get('https://' + rdata, headers=headers).text
                    # in case the scheme is not HTTPS
                    except requests.exceptions.InvalidSchema:
                        req = requests.get('http://' + rdata, headers=headers).text
                        # return error ocurred
                        return 2
                    except Exception:
                        # return error ocurred
                        return 2

                    # if the fingerprint is what is defined in the config file
                    fingerprint = config['cnames']['cname']['fingerprint']
                    if fingerprint == str(req.status_code):
                        # return potential subdomain takeover
                        return 1
                    else:
                        # return no subdomain takeover vulnerability
                        return 0
            # exceptions
            except Exception:
                # return error ocurred
                return 2
