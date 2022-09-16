import requests
import re
from colorama import Fore, Back, Style


# get the basic site status
def site_status(domain):
    title = ''
    status = ''

    # print the title of the section
    print('      ├───' +  Fore.BLACK + Back.WHITE + ' General Info ' + Style.RESET_ALL)

    # open the website
    try:
        r = requests.get('http://'+domain)
        title = ''.join(re.findall('<title>(.*?)</title>', r.text, re.IGNORECASE))
        description = ''.join(re.findall('<meta\s*name\s*=[\s"\']+description[\s"\']+content\s*=[\s"\']*(.*?)["|\'\s]*>', r.text, re.IGNORECASE))
        keywords = ''.join(re.findall('<meta\s*name\s*=[\s"\']+keywords[\s"\']+content\s*=[\s"\']*(.*?)["|\'\s]*>', r.text, re.IGNORECASE))
        status = r.status_code
        
        # print the result on STDOUT
        print('      │      ■ Site Title:       ' + Fore.YELLOW + title + Style.RESET_ALL)
        print('      │      ■ HTTP Status:      ' + Fore.YELLOW + str(status) + Style.RESET_ALL)
        print('      │      ■ Site Description: ' + Fore.YELLOW + description + Style.RESET_ALL)
        print('      │      ■ Site Keywords:    ' + Fore.YELLOW + keywords + Style.RESET_ALL)
    except requests.exceptions.HTTPError as e:
        print('      │      ■ ' + Fore.RED + 'Error in loading the HTTP page.' + Style.RESET_ALL)
        print('      │      ■■ ERROR: ' + Fore.RED + str(e) + Style.RESET_ALL)        
    except requests.exceptions.ConnectionError as e:
        print('      │      ■ ' + Fore.RED + 'Error in establishing the connection.' + Style.RESET_ALL)
        print('      │      ■■ ERROR: ' + Fore.RED + str(e) + Style.RESET_ALL)  
    except requests.exceptions.Timeout as e:
        print('      │      ■ ' + Fore.RED + 'Timeout error.' + Style.RESET_ALL)
        print('      │      ■■ ERROR: ' + Fore.RED + str(e) + Style.RESET_ALL)  
    except requests.exceptions.RequestException as e:
        print('      │      ■ ' + Fore.RED + 'Error in reading the data from the website.' + Style.RESET_ALL)
        print('      │      ■■ ERROR: ' + Fore.RED + str(e) + Style.RESET_ALL)

    return {'site_title':title, 
            'http_status':str(status), 
            'site_description':description,
            'site_keyword':keywords.split(',')
           }
