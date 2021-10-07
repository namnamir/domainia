import requests
import re
from colorama import Fore, Back, Style


# get the basic site status
def site_status(domain):
    title = ''
    status = ''

    # print the record
    print('      ├───' +  Fore.BLACK + Back.WHITE + ' General Info ' + Style.RESET_ALL)

    # open the webiste
    try:
        r = requests.get('http://'+domain)
        title = ''.join(re.findall('<title>(.*?)</title>', r.text))
        status = r.status_code
        
        print(Fore.WHITE + '      │      ■ Site Title:  ' + Fore.YELLOW + title + Style.RESET_ALL)
        print(Fore.WHITE + '      │      ■ HTTP Status: ' + Fore.YELLOW + str(status) + Style.RESET_ALL)
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

    return {'site_title':title, 'HTTP_status':str(status)}
