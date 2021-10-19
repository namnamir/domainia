from api_keys import *

config = {
    'flags': {
        # find alternative domains and subdomains by going into each single
        # certificate or just by skimming the ssl overview
        # possible options: [quick, deep]
        'alt_domain_finder': 'quick',
    },
    # list of the recoreds
    # possible records:
    ### NONE, A, NS, MD, MF, CNAME, SOA, MB, MG, MR, NULL, WKS, PTR, HINFO, MINFO, MX, TXT, RP,
    ### AFSDB, X25, ISDN, RT, NSAP, NSAP-PTR, SIG, KEY, PX, GPOS, AAAA, LOC, NXT, SRV, NAPTR, KX,
    ### CERT, A6, DNAME, OPT, APL, DS, SSHFP, IPSECKEY, RRSIG, NSEC, DNSKEY, DHCID, NSEC3,
    ### NSEC3PARAM, TLSA, HIP, CDS, CDNSKEY, CSYNC, SPF, UNSPEC, EUI48, EUI64, TKEY, TSIG,
    ### IXFR, AXFR, MAILB, MAILA, ANY, URI, CAA, TA, DLV,
    'records': [
        'A',
        'AAAA',
        'NS',
        'CNAME',
        'MX',
        'TXT',
    ],
    'whois': [
        'registrar',
        'registrant',
        'registrationDate',
        'expirationDate',
        'administrativeContact',
        'technicalContact',
    ],
    # for doing the DNS recon, it uses the random list of DNS server,
    # if you prefer just one specific DNS server, remove the list and
    # add the ones you prefer.
    'dns_servers': [
        '8.8.8.8', '8.8.4.4', # Google
        '9.9.9.9', '149.112.112.112', # Quad9
        '208.67.222.222', '208.67.220.220', # OpenDNS
        '1.1.1.1', '1.0.0.1', # Cloudflare
        '185.228.168.9', '185.228.169.9', # CleanBrowsing
        '76.76.19.19', '76.223.122.150', # Alternate DNS
        '94.140.14.14', '94.140.15.15', # AdGuard DNS
    ],
    # for the CSV output file, you can define the delimiter of your choice
    # for each column of it.
    'delimiter': {
        'csv': ',',
        'subdomain': ' ',
        'related_domain': ' ',
        'dns_records': ' ',
    },
    'api': {
        # for whois and DNS records
        'whoisxml': {
            'url_whois': 'https://www.whoisxmlapi.com/whoisserver/WhoisService?apiKey={0}&outputFormat=JSON&domainName={1}',
            'url_dns': 'https://www.whoisxmlapi.com/whoisserver/DNSService?apiKey={0}&outputFormat=JSON&domainName={1}&type=_all',
            'url_balance': 'https://user.whoisxmlapi.com/service/account-balance?apiKey={0}',
            'key': api_key_whoisxml,
        },
        'nameauditor': {
            'url_whois': 'https://nameauditor-whois-check.p.rapidapi.com/whois/{0}',
            'key': api_key_nameauditor,
        },
        # for SSL certificates
        'crt': {
            'url1': 'https://crt.sh/?q=%.{0}&output=json',
            'url2': 'https://crt.sh/?id={0}',
        },
    },
}
