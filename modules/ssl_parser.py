import requests
import json
import re
from colorama import Fore, Back, Style
from config import config
from modules.utils import *


# parse the SSL and find the domains and subdomains with the same
# ssl certificate. It also goes historically
def ssl_parser(domain, scan_type):
    # some variables
    subdomains = set()
    related_domains = set()
    alt_names = set()
    flag = True
    ssl_info = {
        'issue_date': '',
        'expiration_date': '',
        'signature': '',
        'serial_number': '',
        'issuer': {
            'common_name': '',
            'organization_name': '',
            'country': '',
            'organization_unit_name': '',
        },
        'subject': {
            'common_name': '',
            'organization_name': '',
            'country': '',
            'locality_name': '',
        }
    }

    # get the type of the scan; quick or deep
    # if it is defined by stdin, the setting from the config file will be ignored
    if scan_type == '':
        scan_type = config['scan_type']['alt_domain_finder']

    # print out found SSL info
    print('      ├───' + Fore.BLACK + Back.WHITE + ' SSL Certificate Data ' + Style.RESET_ALL)
    
    # find subdomains by parsing historical SSL certificates
    try:
        # download the certificate page on CRT
        url = config['api']['crt_sh']['url1'].format(domain)
        date_format = config['api']['crt_sh']['date_format']
        r = requests.get(url)
        json_data = json.loads(r.text)

        # continue only if there is any data for it
        if json_data:
            json_data = sorted(json_data, key=lambda k: k['id'], reverse=True)
            
            # iterate over each issued certificate (cert history)
            for i in range(0, len(json_data)):
                # if it is a quick search, ignore loading each certificate
                if (scan_type == "quick") and (i > 0):
                    break
                url = config['api']['crt_sh']['url2'].format(json_data[i]['id'])
                cert = requests.get(url)
                # fix the HTML format of the space
                cert = (cert.text).replace('&nbsp;',' ')

                # print the progress
                print('      │      ■■■■  ' + Fore.GREEN + \
                      '{0} cert(s) out of {1} certificates is loaded '.format(i+1, len(json_data)) + Fore.CYAN + \
                      '({0}%)'.format(str(round((i+1)/len(json_data) * 100))) + Fore.WHITE + ' ■■■■' + Style.RESET_ALL)

                # aggregate all alternative names
                alt_names.update(re.findall(r"DNS:(.*?)<BR>", cert))

                # get the latest info of the certificate; ignore older details
                if i == 0:
                    ssl_info = {
                        'issue_date':      date_formatter(re_position(re.findall(r"Not Before[ =:]*(.*?)<BR>", cert), 0), date_format),
                        'expiration_date': date_formatter(re_position(re.findall(r"Not After[ =:]*(.*?)<BR>", cert), 0), date_format),
                        'signature':       re_position(re.findall(r"Signature Algorithm[ :]*(.*?)<BR>", cert), 0),
                        'serial_number':   re_position(re.findall(r"Serial Number[ :]<\/A><BR>[ =]*(.*?)<BR>", cert), 0),
                        'issuer': {
                            'common_name':            re_position(re.findall(r"commonName[ =]*(.*?)<BR>", cert), 0),
                            'organization_name':      re_position(re.findall(r"organizationName[ =]*(.*?)<BR>", cert), 0),
                            'country':                re_position(re.findall(r"countryName[ =]*(.*?)<BR>", cert), 0),
                            'organization_unit_name': re_position(re.findall(r"organizationalUnitName[ =]*(.*?)<BR>", cert), 0),
                        },
                        'subject': {
                            'common_name':       re_position(re.findall(r"commonName[ =]*(.*?)<BR>", cert), 1),
                            'organization_name': re_position(re.findall(r"organizationName[ =]*(.*?)<BR>", cert), 1),
                            'country':           re_position(re.findall(r"countryName[ =]*(.*?)<BR>", cert), 1),
                            'locality_name':     re_position(re.findall(r"localityName[ =]*(.*?)<BR>", cert), 0),
                        },
                    }

            # if it is a quick search
            if scan_type == "quick":
                # iterate over the found results
                for (key, value) in enumerate(json_data):
                    # aggregate all alternative names
                    alt_names.update(value['name_value'].split("\n"))

        # if there is no SSL data            
        else:
            flag = False
            
    except requests.exceptions.HTTPError as e:
        print('      │      ■ ' + Fore.RED + 'Error in loading the HTTP page.')
        print('      │      ■■ ERROR: ' + Fore.RED + str(e) + Style.RESET_ALL)        
        pass
    except requests.exceptions.ConnectionError as e:
        print('      │      ■ ' + Fore.RED + 'Error in establishing the connection.' + Style.RESET_ALL)
        print('      │      ■■ ERROR: ' + Fore.RED + str(e) + Style.RESET_ALL)  
        pass
    except requests.exceptions.Timeout as e:
        print('      │      ■ ' + Fore.RED + 'Timeout error.' + Style.RESET_ALL)
        print('      │      ■■ ERROR: ' + Fore.RED + str(e) + Style.RESET_ALL)  
        pass
    except requests.exceptions.RequestException as e:
        print('      │      ■ ' + Fore.RED + 'Error in reading the data from the API.' + Style.RESET_ALL)
        print('      │      ■■ ERROR: ' + Fore.RED + str(e) + Style.RESET_ALL)
        pass
    except ValueError as e:
        print('      │      ■ ' + Fore.RED + 'Error in handling the JSON.' + Style.RESET_ALL)
        print('      │      ■■ ERROR: ' + Fore.RED + str(e) + '\r\n' + Style.RESET_ALL)
        pass

    # iterate over the found alternative names
    for d in alt_names:
        # ignore the main domain
        if (d != domain):
            # find subdomains
            if d.endswith(domain):
                sd = d.split("."+domain)[0]
                if sd.startswith("*."):
                    sd = sd.split("*.")[1]
                elif sd.startswith("*"):
                    continue
                subdomains.add(sd)
            # find related domains (not subdomain)
            else:
                if d.startswith("*."):
                    rd = d.split("*.")[1]
                else:
                    rd = d
                related_domains.add(rd)

    # remove the domain from the set
    if domain in subdomains:
        subdomains.remove(domain)

    if ssl_info:
        print('      │      ■ Issue Date:        ' + Fore.YELLOW + ssl_info['issue_date'] + Style.RESET_ALL)
        print('      │      ■ Expiration Date:   ' + Fore.YELLOW + ssl_info['expiration_date'] + Style.RESET_ALL)
        print('      │      ■ Signature:         ' + Fore.YELLOW + ssl_info['signature'] + Style.RESET_ALL)
        print('      │      ■ Serial Number:     ' + Fore.YELLOW + ssl_info['serial_number'] + Style.RESET_ALL)
        print('      │      ' + Fore.CYAN + '■ Issuer' + Style.RESET_ALL)
        print('      └┐      ■■  Name:           ' + Fore.YELLOW + ssl_info['issuer']['common_name'] + Style.RESET_ALL)
        print('       │      ■■  Org. Name:      ' + Fore.YELLOW + ssl_info['issuer']['organization_name'] + Style.RESET_ALL)
        print('       │      ■■  Org. Unit Name: ' + Fore.YELLOW + ssl_info['issuer']['organization_unit_name'] + Style.RESET_ALL)
        print('      ┌┘      ■■  Country:        ' + Fore.YELLOW + ssl_info['issuer']['country'] + Style.RESET_ALL)
        print('      │      ' + Fore.CYAN + '■ Subject' + Style.RESET_ALL)
        print('      └┐      ■■  Name:           ' + Fore.YELLOW + ssl_info['subject']['common_name'] + Style.RESET_ALL)
        print('       │      ■■  Org. Name:      ' + Fore.YELLOW + ssl_info['subject']['organization_name'] + Style.RESET_ALL)
        print('       │      ■■  Local Name:     ' + Fore.YELLOW + ssl_info['subject']['locality_name'] + Style.RESET_ALL)
        print('      ┌┘      ■■  Country:        ' + Fore.YELLOW + ssl_info['subject']['country'] + Style.RESET_ALL)
    elif flag:
        print('      │      ■■ ' + Fore.RED + 'Nothing found as SSL certificate info.' + Style.RESET_ALL)
    else:
        print('      │      ■ ' + Fore.RED + 'There is no SSL certificate to extract subdomains from.' + Style.RESET_ALL)

    # print out found subdomains
    print('      ├───' + Fore.BLACK + Back.WHITE + ' Subdomains ' + Style.RESET_ALL)
    if subdomains:
        for sd in subdomains:
            print('      │      ■ ' + Fore.YELLOW + sd + Style.RESET_ALL)
    elif flag:
        print('      │      ■■ ' + Fore.RED + 'Nothing as subdomain is found.' + Style.RESET_ALL)
    else:
        print('      │      ■ ' + Fore.RED + 'There is no SSL certificate to extract subdomains from.' + Style.RESET_ALL)
    
    # print out found related domains
    print('      ├───' + Fore.BLACK + Back.WHITE + ' Related (Sub)domains ' + Style.RESET_ALL)
    if related_domains:
        for rd in related_domains:
            print('      │      ■ ' + Fore.YELLOW + rd + Style.RESET_ALL)
    elif flag:
        print('      │      ■■ ' + Fore.RED + 'Nothing as related domain is found.' + Style.RESET_ALL)
    else:
        print('      │      ■ ' + Fore.RED + 'There is no SSL certificate to extract related (sub)domains from.' + Style.RESET_ALL)
    print('      │\r\n      └───' + Fore.RED + Back.WHITE + ' THE END  ({0}) '.format(domain) + Style.RESET_ALL)
    print('\r\n')

    # return list instead of set
    return [
        ssl_info, 
        sorted(subdomains), 
        sorted(related_domains)
    ]
