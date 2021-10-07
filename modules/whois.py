import requests
import json
from config import config
from colorama import Fore, Back, Style


# get the wohis of the domain form different sources
def whois(domain):
    whois = {
        'registrar': '',
        'registrationDate': '',
        'expirationDate': '',
        'registrant': '',
        'administrativeContact': '',
        'technicalContact': '',
    }

    # print findings
    print('      ├───' + Fore.BLACK + Back.WHITE + ' Whois ' + Style.RESET_ALL)

    try:
        r = requests.get(config['api']['whoisxml']['url_whois'].format(config['api']['whoisxml']['key'], domain))
        json_data = json.loads(r.text)['WhoisRecord']

        whois['registrar'] = json_data['registrarName'] if 'registrarName' in json_data else ''
        whois['registrationDate'] = json_data['registryData']['createdDate'] if ('registryData' in json_data and 'createdDate' in json_data['registryData']) else ''
        whois['expirationDate'] = json_data['registryData']['expiresDate'] if ('registryData' in json_data and 'expiresDate' in json_data['registryData']) else ''

        # get the registrant contact
        if ('registrant' in json_data) and ('organization' in json_data['registrant']):
                whois['registrant'] = json_data['registrant']['organization']
        elif ('registryData' in json_data) and ('registrant' in json_data['registryData']):
            registrant = json_data['registryData']['registrant']
            if 'name' in registrant:
                whois['administrativeContact'] = registrant['name']
            elif 'organization' in registrant:
                whois['administrativeContact'] = registrant['organization']

        # get the administrative contact
        if ('administrativeContact' in json_data) and ('organization' in json_data['administrativeContact']):
                whois['administrativeContact'] = json_data['administrativeContact']['organization']
        elif ('registryData' in json_data) and ('administrativeContact' in json_data['registryData']):
            administrativeContact = json_data['registryData']['administrativeContact']
            if 'name' in administrativeContact:
                whois['administrativeContact'] = administrativeContact['name']
            elif 'organization' in administrativeContact:
                whois['administrativeContact'] = administrativeContact['organization']

        # get the technical contact
        if ('technicalContact' in json_data) and ('organization' in json_data['technicalContact']):
                whois['technicalContact'] = json_data['technicalContact']['organization']
        elif ('registryData' in json_data) and ('technicalContact' in json_data['registryData']):
            technicalContact = json_data['registryData']['technicalContact']
            if 'name' in technicalContact:
                whois['technicalContact'] = technicalContact['name']
            elif 'organization' in technicalContact:
                whois['technicalContact'] = technicalContact['organization']

        print(whois)

        print(Fore.WHITE + '      │      ■ Registrar:              ' + Fore.YELLOW + whois['registrar'] + Style.RESET_ALL)
        print(Fore.WHITE + '      │      ■ Registrant:             ' + Fore.YELLOW + whois['registrant'] + Style.RESET_ALL)
        print(Fore.WHITE + '      │      ■ Administrative Contact: ' + Fore.YELLOW + whois['administrativeContact'] + Style.RESET_ALL)
        print(Fore.WHITE + '      │      ■ Technical Contact:      ' + Fore.YELLOW + whois['technicalContact'] + Style.RESET_ALL)
        print(Fore.WHITE + '      │      ■ Registration Date:      ' + Fore.YELLOW + whois['registrationDate'] + Style.RESET_ALL)
        print(Fore.WHITE + '      │      ■ Expiration Date:        ' + Fore.YELLOW + whois['expirationDate'] + Style.RESET_ALL)
    except requests.exceptions.HTTPError as e:
        print(Fore.WHITE + '      │      ■ ' + Fore.RED + 'Error in loading the HTTP page.' + Style.RESET_ALL)
        print(Fore.WHITE + '      │      ■■ ERROR: ' + Fore.RED + str(e) + Style.RESET_ALL)        
    except requests.exceptions.ConnectionError as e:
        print(Fore.WHITE + '      │      ■ ' + Fore.RED + 'Error in establishing the connection.' + Style.RESET_ALL)
        print(Fore.WHITE + '      │      ■■ ERROR: ' + Fore.RED + str(e) + Style.RESET_ALL)  
    except requests.exceptions.Timeout as e:
        print(Fore.WHITE + '      │      ■ ' + Fore.RED + 'Timeout error.' + Style.RESET_ALL)
        print(Fore.WHITE + '      │      ■■ ERROR: ' + Fore.RED + str(e) + Style.RESET_ALL)  
    except requests.exceptions.RequestException as e:
        print(Fore.WHITE + '      │      ■ ' + Fore.RED + 'Error in reading the data from the website.' + Style.RESET_ALL)
        print(Fore.WHITE + '      │      ■■ ERROR: ' + Fore.RED + str(e) + Style.RESET_ALL) 
    except ValueError as e:
        print(Fore.WHITE + '      │      ■ ' + Fore.RED + 'No Result is found or there was an error.' + Style.RESET_ALL)
        print(Fore.WHITE + '      │      ■■ ERROR: ' + Fore.RED + str(e) + '\r\n' + Style.RESET_ALL)

    # return list instead of set
    return whois    
