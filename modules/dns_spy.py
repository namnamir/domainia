
#!/usr/bin/env python

from bs4 import BeautifulSoup
from config import config
from modules.subdomain_takeover import subdomain_takeover
from modules.utils import run_requests

# get the DNS records by DNS Spy
def dns_spy(domain):
    # initial variables
    dns_records = {}
    subdomains = list()

    # form the URL and the header
    url = config['api']['dns_spy']['url'].format(domain)
    # set the print arguments for the function "run_requests"
    print_args = [True, '      │        ├──■ ', '      │        │  ■■ ']

    # open the URL
    try:
        data = run_requests(url, '', 'text', 'DNS Spy API', print_args)
        text_data, status_code = data[0], data[1]
        
        # if it returns Error 404 which means there is no data for the domain
        if str(status_code) == '404':
            return [
                dns_records,
                set(subdomains)
            ]
        
        # parse the page
        rows = BeautifulSoup(text_data, "html.parser").find('table', {'id': 'domain-table'}).find_all('tr')
        for row in rows:
            # temp variable
            temp = list()

            if 'Record' in str(row):
                continue
            row = row.find_all("td")
            # sanitize the data
            row[0] = row[0].get_text().replace(' ', '').replace('\n', '')
            row[1] = row[1].get_text().replace(' ', '').replace('\n', '')
            row[2] = row[2].get_text().replace(' ', '').replace('\n', '')
            row[3] = row[3].get_text().replace('"', '').replace('\\', '')
            row[3] = row[3].replace('                                                  ', '')
            row[3] = row[3].replace('                                               ', '')
            row[3] = row[3].replace('                                              ', '')
            
            if row[1] == domain and row[0] != 'TXT':
                value = row[3].split('\n')
                # add values to the results and remove duplicates
                temp += list(set(value))
            # find subdomains A\AAAA records
            elif row[0] in ('A', 'AAAA'):
                subdomains.append(row[1].split(domain)[0])
            else:
                sdt_answer = ''
                # ignore the followings
                if row[0] in 'TXT' and row[1].startswith('_dmarc'):
                    continue
                # find subdomains based on CNAME
                if row[0] in 'CNAME':
                    subdomains.append(row[1].split('.' + domain)[0])
                    # if the record is CNAME, check for the subdomain takeover
                    sdt = subdomain_takeover(row[3])
                    # if vulnerable to subdomain takeover
                    if sdt == 1:
                        sdt_answer = '(Vuln_Subdomain_Takeover) '
                row[3] = row[3].replace('\n', ' ')
                value = sdt_answer + row[1] + ' ' + row[2] + ' ' + row[3]
                # add values to the results
                temp.append(value)
                
            # add the data to results and remove duplicates
            if row[0] in dns_records:
                dns_records[row[0]] += list(set(temp))
            else:
                dns_records[row[0]] = list(set(temp))

            # remove empty items
            if '' in dns_records[row[0]]: dns_records[row[0]].remove('')

    # exceptions
    except:
        pass

    # return results
    return [
        dns_records,
        set(subdomains)
    ]