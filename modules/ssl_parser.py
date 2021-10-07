import requests
import json
import re
from config import config
from colorama import Fore, Back, Style


# parse the SSL and find the domains and subdomains with the same
# ssl certificat. It also goes historically
def ssl_parser(domain):
    # a sub-function to pars the result of the regex find_all function
    def ssl_json(term, pos):
        return term[pos] if (len(term) > pos) else ''

    # some variables
    subdomains = set()
    related_domains = set()
    alt_names = set()
    ssl_info = {
        'issue_date': '',
        'expriration_date': '',
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
        },
    }
    flag = True

    # print out found SSL info
    print('      ├───' + Fore.BLACK + Back.WHITE + ' SSL Certificate Data ' + Style.RESET_ALL)
    
    # find subdomains by parsing historical SSL certificates
    try:
        r = requests.get(config['api']['crt']['url1'].format(domain))
        json_data = json.loads(r.text)

        # continue only if there is any data for it
        if json_data:
            json_data = sorted(json_data, key=lambda k: k['id'], reverse=True)
            
            # iterate over each issued certificate (cert history)
            for i in range(0, len(json_data)):
                # if it is a quick search, ignore loading each certificate
                if (config['flags']['Alt-Domain Finder'] == "quick") and (i > 0):
                    break
                cert = requests.get(config['api']['crt']['url2'].format(json_data[i]['id']))
                # fix the HTML format of the space
                cert = (cert.text).replace('&nbsp;',' ')

                # print the progress
                # print((i+1))
                # print(len(json_data))
                # print(round((i+1)/len(json_data)))
                print(Fore.WHITE + '      │      ■■■■  ' + Fore.GREEN + \
                      '{0} certificate out of {1} is loaded '.format(i, len(json_data)) + Fore.WHITE + \
                      '■■■■ ({0}%)'.format(str(round((i+1)/len(json_data) * 100))) + Style.RESET_ALL, end="\r")

                # agregate all alternative names
                alt_names.update(re.findall(r"DNS:(.*?)<BR>", cert))

                # get the latest info of the certificate; ignore older details
                if i == 0:
                    ssl_info = {
                        'issue_date':       ssl_json(re.findall(r"Not Before[ =:]*(.*?)<BR>", cert), 0),
                        'expriration_date': ssl_json(re.findall(r"Not After[ =:]*(.*?)<BR>", cert), 0),
                        'signature':        ssl_json(re.findall(r"Signature Algorithm[ :]*(.*?)<BR>", cert), 0),
                        'serial_number':    ssl_json(re.findall(r"Serial Number[ :]<\/A><BR>[ =]*(.*?)<BR>", cert), 0),
                        'issuer': {
                            'common_name':            ssl_json(re.findall(r"commonName[ =]*(.*?)<BR>", cert), 0),
                            'organization_name':      ssl_json(re.findall(r"organizationName[ =]*(.*?)<BR>", cert), 0),
                            'country':                ssl_json(re.findall(r"countryName[ =]*(.*?)<BR>", cert), 0),
                            'organization_unit_name': ssl_json(re.findall(r"organizationalUnitName[ =]*(.*?)<BR>", cert), 0),
                        },
                        'subject': {
                            'common_name':       ssl_json(re.findall(r"commonName[ =]*(.*?)<BR>", cert), 1),
                            'organization_name': ssl_json(re.findall(r"organizationName[ =]*(.*?)<BR>", cert), 1),
                            'country':           ssl_json(re.findall(r"countryName[ =]*(.*?)<BR>", cert), 1),
                            'locality_name':     ssl_json(re.findall(r"localityName[ =]*(.*?)<BR>", cert), 0),
                        },
                    }

            # if it is a quick search
            if config['flags']['Alt-Domain Finder'] == "quick":
                # iterate over the found results
                for (key, value) in enumerate(json_data):
                    # agregate all alternative names
                    alt_names.update(value['name_value'].split("\n"))

        # if there is no SSL data            
        else:
            flag = False
            
    except requests.exceptions.HTTPError as e:
        print(Fore.WHITE + '      │      ■ ' + Fore.RED + 'Error in loading the HTTP page.')
        print(Fore.WHITE + '      │      ■■ ERROR: ' + Fore.RED + str(e) + Style.RESET_ALL)        
        pass
    except requests.exceptions.ConnectionError as e:
        print(Fore.WHITE + '      │      ■ ' + Fore.RED + 'Error in establishing the connection.' + Style.RESET_ALL)
        print(Fore.WHITE + '      │      ■■ ERROR: ' + Fore.RED + str(e) + Style.RESET_ALL)  
        pass
    except requests.exceptions.Timeout as e:
        print(Fore.WHITE + '      │      ■ ' + Fore.RED + 'Timeout error.' + Style.RESET_ALL)
        print(Fore.WHITE + '      │      ■■ ERROR: ' + Fore.RED + str(e) + Style.RESET_ALL)  
        pass
    except requests.exceptions.RequestException as e:
        print(Fore.WHITE + '      │      ■ ' + Fore.RED + 'Error in reading the data from the API.' + Style.RESET_ALL)
        print(Fore.WHITE + '      │      ■■ ERROR: ' + Fore.RED + str(e) + Style.RESET_ALL)
        pass
    except ValueError as e:
        print(Fore.WHITE + '             ■ ' + Fore.RED + 'Error in handling the JSON.' + Style.RESET_ALL)
        print(Fore.WHITE + '             ■■ ERROR: ' + Fore.RED + str(e) + '\r\n' + Style.RESET_ALL)
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
        print(Fore.WHITE + '      │      ■ SSL Issue Date:      ' + Fore.YELLOW + ssl_info['issue_date'] + Style.RESET_ALL)
        print(Fore.WHITE + '      │      ■ SSL Expiration Date: ' + Fore.YELLOW + ssl_info['expriration_date'] + Style.RESET_ALL)
        print(Fore.WHITE + '      │      ■ SSL Signature:       ' + Fore.YELLOW + ssl_info['signature'] + Style.RESET_ALL)
        print(Fore.WHITE + '      │      ■ SSL Serial Number:   ' + Fore.YELLOW + ssl_info['serial_number'] + Style.RESET_ALL)
        print(Fore.WHITE + '      │      ■ SSL Issure Name:     ' + Fore.YELLOW + ssl_info['issuer']['organization_name'] + Style.RESET_ALL)
        print(Fore.WHITE + '      │      ■ SSL Subject Name:    ' + Fore.YELLOW + ssl_info['subject']['organization_name'] + Style.RESET_ALL)
    elif flag:
        print(Fore.WHITE + '             ■■ ' + Fore.RED + 'Nothing found as SSL certificate info.' + Style.RESET_ALL)
    else:
        print(Fore.WHITE + '             ■ ' + Fore.RED + 'There is no SSL certificate to extract subdomains from.' + Style.RESET_ALL)

    # print out found subdomains
    print('      ├───' + Fore.BLACK + Back.WHITE + ' Subdomains ' + Style.RESET_ALL)
    if subdomains:
        for sd in subdomains:
            print(Fore.WHITE + '      │      ■ ' + Fore.YELLOW + sd + Style.RESET_ALL)
    elif flag:
        print(Fore.WHITE + '             ■■ ' + Fore.RED + 'Nothing as subdomain is found.' + Style.RESET_ALL)
    else:
        print(Fore.WHITE + '             ■ ' + Fore.RED + 'There is no SSL certificate to extract subdomains from.' + Style.RESET_ALL)
    
    # print out found related domains
    print('      └───' + Fore.BLACK + Back.WHITE + ' Related (Sub)domains ' + Style.RESET_ALL)
    if related_domains:
        for rd in related_domains:
            print(Fore.WHITE + '             ■ ' + Fore.YELLOW + rd + Style.RESET_ALL)
    elif flag:
        print(Fore.WHITE + '             ■■ ' + Fore.RED + 'Nothing as related domain is found.' + Style.RESET_ALL)
    else:
        print(Fore.WHITE + '             ■ ' + Fore.RED + 'There is no SSL certificate to extract related (sub)domains from.' + Style.RESET_ALL)
    print('\r\n')

    # return list instead of set
    return [ssl_info, sorted(subdomains), sorted(related_domains)]
