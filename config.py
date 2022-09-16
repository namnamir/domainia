from api_keys import *

config = {
    # format of the data/time in the output file and stdout
    # for date/time formats, check out 
    # https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
    'date_format': '%Y-%m-%d %H:%M:%S',
    'scan_type': {
        # find alternative domains and subdomains by going into each single
        # certificate or just by skimming the ssl overview
        # possible options: "quick" and "deep"
        # if it is defined by stdin (argument -t),
        # the setting from the config file will be ignored
        'alt_domain_finder': 'quick',
    },
    # list of the records
    # possible records:
    ### NONE, A, NS, MD, MF, CNAME, SOA, MB, MG, MR, NULL, WKS, PTR, HINFO, MINFO, MX, TXT, RP,
    ### AFSDB, X25, ISDN, RT, NSAP, NSAP-PTR, SIG, KEY, PX, GPOS, AAAA, LOC, NXT, SRV, NAPTR, KX,
    ### CERT, A6, DNAME, OPT, APL, DS, SSHFP, IPSECKEY, RRSIG, NSEC, DNSKEY, DHCID, NSEC3,
    ### NSEC3PARAM, TLSA, HIP, CDS, CDNSKEY, CSYNC, SPF, UNSPEC, EUI48, EUI64, TKEY, TSIG,
    ### IXFR, AXFR, MAILB, MAILA, ANY, URI, CAA, TA, DLV,
    'dns_records': [
        'A',
        'AAAA',
        'NS',
        'CNAME',
        'MX',
        'TXT',
    ],
    # ignore any TXT records does not contain following terms
    'include_txt_records': [
        'spf',
        'dmarc',
        'domainkey'
    ],
    # to perform the DNS recon, it uses the random list of DNS server,
    # if you prefer just one specific DNS server, remove the list and
    # add your preference.
    'dns_servers': [
        '8.8.8.8', '8.8.4.4',               # Google
        '9.9.9.9', '149.112.112.112',       # Quad9
        '208.67.222.222', '208.67.220.220', # OpenDNS
        '1.1.1.1', '1.0.0.1',               # Cloudflare
        '185.228.168.9', '185.228.169.9',   # CleanBrowsing
        '76.76.19.19', '76.223.122.150',    # Alternate DNS
        '94.140.14.14', '94.140.15.15',     # AdGuard DNS
    ],
    # for the CSV output file, you can define the delimiter of your choice
    'delimiter': {
        # delimiter for the CSV columns
        'csv':            ',',
        # delimiter for the subdomains column in the CSV file
        'subdomain':      ' ',
        # delimiter for the related domains column in the CSV file
        'related_domain': ' ',
        # delimiter for the DNS records column in the CSV file
        'dns_records':    ' ',
        # delimiter for the name servers (NS) column in the CSV file
        'nameserver':     ' ',
        # delimiter for the keywords column in the CSV file
        # keywords would contain space, then space is not a good delimiter
        'keyword':        '_',
    },
    # define which Whois data should be parsed and be written in the output file
    # "True" means be included
    # "False" means be excluded
    'whois': {
        'create_date':      True,
        'update_date':      True,
        'expiration_date':  True,
        'domain_age_days':  True,
        'registrar': {
            'name':         False,
            'iana_id':      False,
            'website':      False,
            'whois_server': False,
            'email':        False,
            'phone':        False,
        },
        'registrant': {
            'name':         True,
            'country':      True,
            'email':        True,
            'phone':        True,
        },
        'administrative': {
            'name':         False,
            'country':      False,
            'email':        False,
            'phone':        False,
        },
        'technical': {
            'name':         False,
            'country':      False,
            'email':        False,
            'phone':        False,
        },
        'name_servers':     False,
    },
    # define which SSL data should be parsed and be written in the output file
    # "True" means be included
    # "False" means be excluded
    'ssl': {
        'issue_date':                 True,
        'expiration_date':            True,
        'signature':                  True,
        'serial_number':              True,
        'issuer': {
            'common_name':            True,
            'organization_name':      True,
            'country':                True,
            'organization_unit_name': True,
        },
        'subject': {
            'common_name':            True,
            'organization_name':      True,
            'country':                True,
            'locality_name':          True,
        }
    },
    # details of APIs
    # for date/time formats, check out 
    # https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
    'api': {
        # whois lookup apis
        'whoisxml': {
            'url_whois':   'https://www.whoisxmlapi.com/whoisserver/WhoisService?apiKey={0}&outputFormat=JSON&domainName={1}',
            'url_dns':     'https://www.whoisxmlapi.com/whoisserver/DNSService?apiKey={0}&outputFormat=JSON&domainName={1}&type=_all',
            'url_balance': 'https://user.whoisxmlapi.com/service/account-balance?apiKey={0}',
            'date_format': '%Y-%m-%dT%H:%M:%SZ',
            'api_key':     api_key_whoisxml,
        },
        'whoxy': {
            'url_whois':   'https://api.whoxy.com/?key={0}&whois={1}&format=json',
            'url_balance': 'https://api.whoxy.com/?key={0}&account=balance',
            'date_format': '%Y-%m-%d',
            'api_key':     api_key_whoxy,
        },
        # SSL certificate api
        'crt': {
            'url1':        'https://crt.sh/?q={0}&output=json',
            'url2':        'https://crt.sh/?id={0}',
            'date_format': '%b %d %H:%M:%S %Y GMT',
        },
    },
}
