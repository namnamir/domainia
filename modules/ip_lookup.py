import ipaddress
import requests
import json
from colorama import Fore, Back, Style
from config import config


# validate the Ipv4 or IPv6
def validate_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False


# lookup the ip
def ip_lookup(ip):
    # call the IP-API and parse the data
    def ip_api(ip):
        # call the API
        api = config['api']['ipapi']['url_lookup'].format(ip, config['api']['ipapi']['fields'])
        r = requests.get(api)
        json_data = json.loads(r.text)

        # write the data
        ip_lookup = {
            'continent': json_data['continent'],
            'continent_code': json_data['continentCode'],
            'country': json_data['country'],
            'country_code': json_data['countryCode'],
            'region': json_data['regionName'],
            'city': json_data['city'],
            'zip_code': json_data['zip'],
            'latitude': json_data['lat'],
            'longitude': json_data['lon'],
            'timezone': json_data['timezone'],
            'time_offset': json_data['offset'],
            'isp': json_data['isp'],
            'organization': json_data['org'],
            'as_number': json_data['as'],
            'as_name': json_data['asname'],
            'reverse_dns': json_data['reverse'],
            'mobile': str(json_data['mobile']),
            'proxy': str(json_data['proxy']),
            'hosting': str(json_data['hosting']),
        }

        return ip_lookup
    
    
    try:
        # define some variables
        ip_lookup = {
            'continent': '',
            'continent_code': '',
            'country': '',
            'country_code': '',
            'region': '',
            'city': '',
            'zip_code': '',
            'latitude': '',
            'longitude': '',
            'time_offset': '',
            'offset': '',
            'isp': '',
            'organization': '',
            'as_number': '',
            'as_name': '',
            'reverse_dns': '',
            'mobile': '',
            'proxy': '',
            'hosting': ''
        }

        # check if the ip is a valid one
        if validate_ip(ip):
            ip_lookup = ip_api(ip)

    # exceptions
    except requests.exceptions.HTTPError as e:
        print('      │      ■ ' + Fore.RED + 'Error in loading the IP Lookup API URL page.' + Style.RESET_ALL)
        print('      │      ■■ ERROR: ' + Fore.RED + str(e) + Style.RESET_ALL)        
    except requests.exceptions.ConnectionError as e:
        print('      │      ■ ' + Fore.RED + 'Error in establishing the connection to the IP Lookup API URL.' + Style.RESET_ALL)
        print('      │      ■■ ERROR: ' + Fore.RED + str(e) + Style.RESET_ALL)  
    except requests.exceptions.Timeout as e:
        print('      │      ■ ' + Fore.RED + 'Timeout error.' + Style.RESET_ALL)
        print('      │      ■■ ERROR: ' + Fore.RED + str(e) + Style.RESET_ALL)  
    except requests.exceptions.RequestException as e:
        print('      │      ■ ' + Fore.RED + 'Error in reading the data from the IP Lookup API URL.' + Style.RESET_ALL)
        print('      │      ■■ ERROR: ' + Fore.RED + str(e) + Style.RESET_ALL) 
    except requests.exceptions.TooManyRedirects as e:
        print('      │      ■ ' + Fore.RED + 'The provided IP Lookup API URL does not seem correct.' + Style.RESET_ALL)
        print('      │      ■■ ERROR: ' + Fore.RED + str(e) + Style.RESET_ALL)
    except json.decoder.JSONDecodeError as e:
        print('      │      ■ ' + Fore.RED + 'Error in reading the JSON data retrieved from the IP Lookup API call.' + Style.RESET_ALL)
        print('      │      ■■ ERROR: ' + Fore.RED + str(e) + Style.RESET_ALL)
    except ValueError as e:
        print('      │      ■ ' + Fore.RED + 'No Result is found or there was an error.' + Style.RESET_ALL)
        print('      │      ■■ ERROR: ' + Fore.RED + str(e) + Style.RESET_ALL)
    except Exception as e:
        print('      │      ■ ' + Fore.RED + 'An unknown error is ocurred.' + Style.RESET_ALL)
        print('      │      ■■ ERROR: ' + Fore.RED + str(e) + Style.RESET_ALL)
    
    # return the results in the format of set
    return ip_lookup