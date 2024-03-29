#!/usr/bin/env python


"""
    The config file contains all settings and configurations of the tool.
    If you would like to change any value of the config dictionary, be 
    careful not to change the key. Moreover, remember that values are 
    case-sensitive.
"""


import random
from datetime import datetime
from api_keys import *

config = {
    # format of the data/time in the output file and stdout
    # for date/time formats, check out 
    # https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
    'date_format': '%Y-%m-%d %H:%M:%S',
    # set the config verbosity
    # it would be a number between 1 and 5
    # 1 represents the least verbosity and 5 the most one
    'verbosity': 5,
    # the text to be shown when subdomain takeover vulnerability is found
    'subdomain_takeover': '(Vuln_Subdomain_Takeover) ',
    # define the delay
    'delay': {
        # delay between each domains
        'domain': random.randint(5, 20),
        # delay between DNS queries
        'dns': random.randint(0, 1),
        # delay between loading SSL certificates
        'ssl': random.randint(3, 10),
    },
    'scan_type': {
        # find alternative domains and subdomains by going into each single
        # certificate or just by skimming the ssl overview
        # possible options: "quick" and "deep"
        # if it is defined by stdin (argument -t),
        # the setting from the config file will be ignored
        'alt_domain_finder': 'quick',
    },
    'output': {
        # the default name of the output file
        'filename': 'output_{0}'.format(datetime.now().strftime('%Y-%m-%d')),
        # the output file format
        # possible options are as follows
        # 'csv' for a CSV file
        # 'json' for a JSON file
        # 'txt' for a text file of the STDOUT
        # 'all' for all aforementioned formats
        'format': 'all',
        # define which items should be included in the CSV file
        # "True" means be included
        # "False" means be excluded
        'include': {
            # define which Whois data should be parsed and be written in the CSV output file
            'whois': {
                'create_date': True,
                'update_date': True,
                'expiration_date': True,
                'domain_age_days': True,
                'registrar': {
                    'name': False,
                    'iana_id': False,
                    'website': False,
                    'whois_server': False,
                    'email': False,
                    'phone': False,
                },
                'registrant': {
                    'name': True,
                    'country': True,
                    'email': True,
                    'phone': True,
                },
                'administrative': {
                    'name': False,
                    'country': False,
                    'email': False,
                    'phone': False,
                },
                'technical': {
                    'name': False,
                    'country': False,
                    'email': False,
                    'phone': False,
                },
                'name_servers': False,
            },
            # define which SSL data should be parsed and be written in the CSV output file
            'ssl': {
                'issue_date': True,
                'expiration_date': True,
                'signature': True,
                'serial_number': True,
                'issuer': {
                    'common_name': True,
                    'organization_name': True,
                    'country': True,
                    'organization_unit_name': True,
                },
                'subject': {
                    'common_name': True,
                    'organization_name': True,
                    'country': True,
                    'locality_name': True,
                }
            },
            # define which HTTP data should be parsed an written in the CSV output file
            'http': {
                'title': True,
                'status_code': True,
                'redirect': True,
                'blocked_domain': True,
                'blocked_ip': True,
                'meta': {
                    'description': True,
                    'keywords': False,
                    'robots': True,
                    'twitter_site': False,
                    'twitter_author': False,
                    'facebook_site': False,
                    'facebook_author': False,
                    'canonical': False,
                },
                'analytics': {
                    'google_ua': True,
                    'matomo': False,
                },
                'headers': {
                    'accept-ranges': False,
                    'access-control-allow-credentials': False,
                    'access-control-allow-headers': False,
                    'access-control-allow-methods': False,
                    'access-control-allow-origin': False,
                    'access-control-max-age': False,
                    'age': False,
                    'alt-svc': False,
                    'cache-control': False,
                    'cf-cache-status': False,
                    'cf-ray': False,
                    'connection': False,
                    'content-encoding': False,
                    'content-language': False,
                    'content-length': False,
                    'content-security-policy-report-only': False,
                    'content-security-policy': False,
                    'content-type': False,
                    'date': False,
                    'etag': False,
                    'expect-ct': False,
                    'expires': False,
                    'last-modified': False,
                    'link': False,
                    'nel': False,
                    'p3p': False,
                    'permissions-policy': False,
                    'pragma': False,
                    'property-id': False,
                    'referrer-policy': False,
                    'report-to': False,
                    'server-timing': False,
                    'set-cookie': False,
                    'strict-transport-security': False,
                    'transfer-encoding': False,
                    'twc-ak-req-id': False,
                    'twc-connection-speed': False,
                    'twc-device-class': False,
                    'twc-geoip-city': False,
                    'twc-geoip-country': False,
                    'twc-geoip-dma': False,
                    'twc-geoip-latlong': False,
                    'twc-geoip-region': False,
                    'twc-locale-group': False,
                    'twc-path-locale': False,
                    'twc-privacy': False,
                    'twc-subs': False,
                    'twc-unit': False,
                    'user-agent': False,
                    'vary': False,
                    'x-acquia-host': False,
                    'x-acquia-path': False,
                    'x-acquia-purge-tags': False,
                    'x-acquia-site': False,
                    'x-age': False,
                    'x-akamai-transformed': False,
                    'x-amz-cf-pop': False,
                    'x-arc': False,
                    'x-bucket-id': False,
                    'x-cache-hits': False,
                    'x-cache': False,
                    'x-content-security-policy-report-only': False,
                    'x-content-type-options': False,
                    'x-dns-prefetch-control': False,
                    'x-download-options': False,
                    'x-drupal-cache': False,
                    'x-drupal-dynamic-cache': False,
                    'x-envoy-upstream-service-time': False,
                    'x-frame-options': False,
                    'x-generator': False,
                    'x-origin-response-time': False,
                    'x-origin-tag': False,
                    'x-query-param': False,
                    'x-tt-logid': False,
                    'x-tt-trace-host': False,
                    'x-tt-trace-tag': False,
                    'x-ua-compatible': False,
                    'x-url-scheme': False,
                    'x-varnish': False,
                    'x-webkit-csp-report-only': False,
                    'x-xss-protection': False,
                    'x-zm-zoneid': False,
                },
            },
        },
        # settings of the JSON output file
        'json': {
            # define the indent size for the JSON file
            'indent': 4,
        },
        # settings of the CSV output file
        'csv': {
            # define the header joiner
            # i.e. json['a']['b']['c'] ==> 'a_b_c'
            'header_joiner': '_',
            # define the delimiter of your choice
            'delimiter': {
                # delimiter for the subdomains column in the CSV file
                'subdomain': ' ',
                # delimiter for the related domains column in the CSV file
                'related_domain': ' ',
                # delimiter for the DNS records column in the CSV file
                'dns_records': ' ',
                # delimiter for the name servers (NS) column in the CSV file
                'nameserver': ' ',
                # delimiter for the keywords column in the CSV file
                # keywords would contain space, then space is not a good delimiter
                'keyword': ' ',
                # delimiter for the blocklist column in the CSV file
                'blocklist': ' ',
                # delimiter for the CSV columns
                'column': ',',
            },
        },
    },
    # the user agent will be randomly selected among the list
    # you can use this website to generate the random User Agents: https://useragents.io/explore
    'user_agents' : [
        # Windows / Desktop
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; rv:102.0) Gecko/20100101 Firefox/102.0',
        'Mozilla/5.0 (Windows NT 10.0; rv:100.0) Gecko/20100101 Firefox/100.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0 IceDragon/65.0.2',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; TheWorld)',
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36 ASW/1.46.1990.139',
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36 LBBROWSER',
        # MacOS / Desktop
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15',
        'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_1) AppleWebKit/5331 (KHTML, like Gecko) Chrome/39.0.862.0 Mobile Safari/5331',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.2 Safari/605.1.15',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36 Edg/98.0.1108.51',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 DuckDuckGo/7 Safari/605.1.15',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:106.0) Gecko/20100101 Firefox/106.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Teams/1.3.00.9271 Chrome/69.0.3497.128 Electron/4.2.12 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 YaBrowser/21.9.0.1488 Yowser/2.5 Safari/537.36',
        # Linux / Desktop
        'Mozilla/5.0 (X11; Linux i686) AppleWebKit/5332 (KHTML, like Gecko) Chrome/36.0.801.0 Mobile Safari/5332',
        'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Debian Chrome/52.0.2743.116 Safari/537.36',
        'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.7.8) Gecko/20050927 Debian/1.7.8-1sarge3',
        'Mozilla/5.0 (Macintosh; ARM Mac OS X) AppleWebKit/538.15 (KHTML, like Gecko) Safari/538.15 Version/6.0 Raspbian/8.0 (1:3.8.2.0-0rpi27rpi1g) Epiphany/3.8.2',
        'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.7.6) Gecko/20050328 Fedora/1.7.6-1.2.5',
        'Mozilla/5.0 (compatible; Konqueror/4.5; FreeBSD) KHTML/4.5.4 (like Gecko)',
        'Opera/9.01 (X11; FreeBSD 6 i386; U; en)',
        'Mozilla/4.76 [en] (X11; U; FreeBSD 4.4-STABLE i386)',
        'Midori/0.2 (X11; FreeBSD; U; en-us) WebKit/531.2+',
        'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/540.0 (KHTML, like Gecko) Ubuntu/10.10 Chrome/9.1.0.0 Safari/540.0',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/80.0.3987.87 Chrome/80.0.3987.87 Safari/537.36',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:105.0) Gecko/20100101 Firefox/105.0',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Cypress/6.9.1 Chrome/87.0.4280.141 Electron/11.3.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.114 YaBrowser/22.9.1.1110 (beta) Yowser/2.5 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64; rv:106.0) Gecko/20100101 Firefox/106.0',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.34 (KHTML, like Gecko) kioclient/5.20.5 Safari/534.34',
        # Mobile phones
        'Mozilla/5.0 (Linux; arm_64; Android 11; SM-A225F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.166 YaBrowser/21.8.5.54.00 SA/3 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 10; FRL-L22; HMSCore 6.7.0.321) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.105 HuaweiBrowser/12.1.2.312 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 12; SAMSUNG SM-F721N/KSU1AVJ5) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/18.0 Chrome/99.0.4844.88 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 4.1.2; Nokia_XL Build/JZO54K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.82 Mobile Safari/537.36 NokiaBrowser/1.2.0.12',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 8_2_1 like Mac OS X; sl-SI) AppleWebKit/533.9.5 (KHTML, like Gecko) Version/4.0.5 Mobile/8B111 Safari/6533.9.5',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 16_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/106.0 Mobile/15E148 Safari/605.1.15',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1 (compatible; Baiduspider-render/2.0; +http://www.baidu.com/search/spider.html)',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15G77 Twitter for iPhone/7.28',
        'Mozilla/5.0 (Windows Phone 10.0; Android 6.0.1; Xbox; Xbox One) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Mobile Safari/537.36 Edge/16.16299',
        # Tablets
        'Mozilla/5.0 (iPad; CPU OS 15_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6,2 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (iPad; CPU OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/107.0.5304.66 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (iPad; CPU OS 13_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 [FBAN/FBIOS;FBDV/iPad5,1;FBMD/iPad;FBSN/iOS;FBSV/13.1;FBSS/2;FBID/tablet;FBLC/en_US;FBOP/5]',
        'Mozilla/5.0 (iPad; CPU OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Version/13.2.3 Safari/604.1 AlohaBrowser/2.15.2b3',
        'Mozilla/5.0 (iPad; CPU OS 16_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Mobile/15E148 Safari/604.1',
    ],
    # dns related settings
    'dns': {
        # list of the records
        # divide name by '/', e.g. TXT/_dmarc means _dmarc in TXT records
        # some famous DKIM selectors are listed below. Use them if you would like to brute-force selectors
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
            'DNSKEY',
            'RRSIG',
            'TXT',
            'SRV',
            'PTR',
            ## default DMARC subdomain
            'TXT/_dmarc',
            ## default DKIM
            ## Maropost default DKIM
            'TXT/default._domainkey',
            ## Google default DKIM
            #'TXT/google._domainkey',
            ## Microsoft default DKIM
            #'TXT/selector1._domainkey',
            ## Microsoft default DKIM
            #'TXT/selector2._domainkey',
            ## Sendgrid / SharpSpring default DKIM
            #'TXT/s1._domainkey',
            ## Sendgrid / SharpSpring default DKIM
            #'TXT/s2._domainkey',
            ## Hetzner default DKIM
            #'TXT/dkim._domainkey',
            ## MailChimp default DKIM
            #'TXT/mandrill._domainkey',
            ## MailChimp / Mandrill / MailGun default DKIM
            #'TXT/k1._domainkey',
            ## MailChimp / Mandrill default DKIM
            #'TXT/k2._domainkey',
            ## Everlytic default DKIM
            #'TXT/everlytickey1._domainkey',
            ## Everlytic default DKIM
            #'TXT/everlytickey2._domainkey',
            ## Everlytic default DKIM
            #'TXT/eversrv._domainkey',
            ## Acoustic / SilverPop / IBM Watson default DKIM
            #'TXT/spop1024._domainkey',
            ## ActiveCampaign default DKIM
            #'TXT/dk._domainkey',
            ## Aruba.it default DKIM
            #'TXT/a1._domainkey',
            ## AWeber default DKIM
            #'TXT/aweber_key_a._domainkey',
            ## AWeber default DKIM
            #'TXT/aweber_key_b._domainkey',
            ## AWeber default DKIM
            #'TXT/aweber_key_c._domainkey',
            ## Campaign Monitor default DKIM
            #'TXT/cm._domainkey',
            ## ContactLab default DKIM
            #'TXT/clab1._domainkey',
            ## DotDigital default DKIM
            #'TXT/dkim1024._domainkey',
            ## Emarsys / Listrak default DKIM
            #'TXT/key1._domainkey',
            ## Emarsys default DKIM
            #'TXT/key2._domainkey',
            ## Emma default DKIM
            #'TXT/e2ma-k1._domainkey',
            ## Emma default DKIM
            #'TXT/e2ma-k2._domainkey',
            ## Emma default DKIM
            #'TXT/e2ma-k3._domainkey',
            ## GoDaddy / Mad Mimi default DKIM
            #'TXT/sable._domainkey',
            ## HubSpot default DKIM
            #'TXT/hs1._domainkey',
            ## HubSpot default DKIM
            #'TXT/hs2._domainkey',
            ## Klaviyo default DKIM
            #'TXT/kl._domainkey',
            ## Klaviyo default DKIM
            #'TXT/kl1._domainkey',
            ## MailJet default DKIM
            #'TXT/mailjet._domainkey',
            ## MailPoet default DKIM
            #'TXT/mailpoet1._domainkey',
            ## MailPoet default DKIM
            #'TXT/mailpoet2._domainkey',
            ## Mapp Digital default DKIM
            #'TXT/ecm1._domainkey',
            ## Omnisend default DKIM
            #'TXT/smtp._domainkey',
            ## Sendinblue default DKIM
            #'TXT/mail._domainkey',
        ],
        # ignore any TXT records does not contain following terms
        'include_txt_records': [
            'SPF',
            'DMARC',
            'DKIM'
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
        # translation of DNS RCODEs
        # read more: http://www.iana.org/assignments/dns-parameters/dns-parameters.xhtml
        #            https://dnspython.readthedocs.io/en/latest/_modules/dns/rcode.html
        'dns_rcode': {
            0: 'NOERROR: DNS query completed successfully',
            1: 'FORMERR: DNS Query Format Error',
            2: 'SERVFAIL: Server failed to complete the DNS request',
            3: 'NXDOMAIN: Domain name does not exist',
            4: 'NOTIMP: Function not implemented',
            5: 'REFUSED: The server refused to answer for the query',
            6: 'YXDOMAIN: Name that should not exist, does exist',
            7: 'YXRRSET: RRset that should not exist, does exist',
            8: 'NXRRSet: RR Set that should exist, does not exist',
            9: 'NOTAUTH: Server not authoritative for the zone or not authorized',
            10: 'NOTZONE: Name not contained in zone',
            11: 'DSOTYPENI: DSO-TYPE Not Implemented',
            16: 'BADSIG/BADSIG: Bad OPT Version or TSIG signature failure',
            17: 'BADKEY: Key not recognized',
            18: 'BADTIME: Signature out of time window',
            19: 'BADMODE: Bad TKEY Mode',
            20: 'BADNAME: Duplicate key name',
            21: 'BADALG: Algorithm not supported',
            22: 'BADTRUNC: Bad truncation',
            23: 'BADCOOKIE: Bad or missing server cookie',
        }
    },
    'cnames': {
        # Githb
        'github.io': {
            'service': 'Github',
            'fingerprint': 'There isn\'t a GitHub Pages site here.',
            'f_type': 'content',
        },
        'gitbooks.io': {
            'service': 'Github',
            'fingerprint': '400',
            'f_type': 'http_status',
        },
        # Google
        'ghs.googlehosted.com': {
            'service': 'Google',
            'fingerprint': '',
            'f_type': 'NXDOMAIN',
        },
        'ghs.google.com': {
            'service': 'Google',
            'fingerprint': '',
            'f_type': 'NXDOMAIN',
        },
        'ghs-ssl.googlehosted.com': {
            'service': 'Google',
            'fingerprint': '',
            'f_type': 'NXDOMAIN',
        },
        # Amazon
        'cloudfront.net': {
            'service': 'Amazon CloudFront',
            'fingerprint': '',
            'f_type': 'NXDOMAIN',
        },
        'elasticbeanstalk.com': {
            'service': 'Amazon Elastic Beanstalk',
            'fingerprint': '',
            'f_type': 'NXDOMAIN',
        },
        # for the S3 legacy, it would be s3.amazonaws.com
        # for the regional S3, it would be s3-region-code.amazonaws.com
        'amazonaws.com': {
            'service': 'S3 Amazon',
            'fingerprint': '404',
            'f_type': 'http_status',
        },
        # Azure
        'azurewebsites.net': {
            'service': 'Microsoft Azure',
            'fingerprint': '',
            'f_type': 'NXDOMAIN',
        },
        'cloudapp.net': {
            'service': 'Microsoft Azure',
            'fingerprint': '',
            'f_type': 'NXDOMAIN',
        },
        'cloudapp.azure.com': {
            'service': 'Microsoft Azure',
            'fingerprint': '',
            'f_type': 'NXDOMAIN',
        },
        'trafficmanager.net': {
            'service': 'Microsoft Azure',
            'fingerprint': '',
            'f_type': 'NXDOMAIN',
        },
        'blob.core.windows.net': {
            'service': 'Microsoft Azure',
            'fingerprint': '',
            'f_type': 'NXDOMAIN',
        },
        'azure-api.net': {
            'service': 'Microsoft Azure',
            'fingerprint': '',
            'f_type': 'NXDOMAIN',
        },
        'azurehdinsight.net': {
            'service': 'Microsoft Azure',
            'fingerprint': '',
            'f_type': 'NXDOMAIN',
        },
        'azureedge.net': {
            'service': 'Microsoft Azure',
            'fingerprint': '',
            'f_type': 'NXDOMAIN',
        },
        # Heroku
        'herokuapp.com': {
            'service': 'Heroku',
            'fingerprint': 'There\'s nothing here, yet.',
            'f_type': 'content',
        },
        'herokudns.com': {
            'service': 'Heroku',
            'fingerprint': '',
            'f_type': 'NXDOMAIN',
        },
        # Zendesk
        'zendesk.com': {
            'service': 'Zendesk',
            'fingerprint': 'Oops, this help center no longer exists',
            'f_type': 'content',
        },
        'cloudflare.net': {
            'service': 'Cloudflare',
            'fingerprint': '',
            'f_type': 'NXDOMAIN',
        },
        'fastly.net': {
            'service': 'Fastly',
            'fingerprint': 'Fastly error: unknown domain',
            'f_type': 'content',
        },
        'pantheonsite.io': {
            'service': 'Pantheon',
            'fingerprint': 'Unknown site',
            'f_type': 'content',
        },
        'worksites.net': {
            'service': 'WorkSites',
            'fingerprint': 'Company Not Found',
            'f_type': 'content',
        },
        # Read Me
        'readme.io': {
            'service': 'Read Me',
            'fingerprint': 'Project doesnt exist... yet!',
            'f_type': 'content',
        },
        'readmessl.com': {
            'service': 'Read Me',
            'fingerprint': '',
            'f_type': 'NXDOMAIN',
        },
        'myjetbrains.com': {
            'service': 'Your Track',
            'fingerprint': 'has not been registered as a YouTrack InCloud instance.',
            'f_type': 'content',
        },
        'youtrack.cloud': {
            'service': 'Your Track',
            'fingerprint': 'has not been registered as a YouTrack InCloud instance.',
            'f_type': 'content',
        },
        'vendecommerce.com': {
            'service': 'Vend',
            'fingerprint': 'Oops. This webstore is no longer available',
            'f_type': 'content',
        },
        'gr8.com': {
            'service': 'Get Response',
            'fingerprint': 'This landing page is no longer available',
            'f_type': 'content',
        },
        'createsend.com': {
            'service': 'Create Send',
            'fingerprint': 'Double check the URL or',
            'f_type': 'content',
        },
        'bigcartel.com': {
            'service': 'Big Cartel',
            'fingerprint': 'Oops! We couldn’t find that page.',
            'f_type': 'content',
        },
        'bcvp0rtal.com': {
            'service': 'Bright Cove',
            'fingerprint': 'Page Not Found',
            'f_type': 'content',
        },
        'brightcovegallery.com': {
            'service': 'Bright Cove',
            'fingerprint': 'Page Not Found',
            'f_type': 'content',
        },
        'gallery.video': {
            'service': 'Bright Cove',
            'fingerprint': 'Page Not Found',
            'f_type': 'content',
        },
        'ideas.aha.io': {
            'service': 'Aha!',
            'fingerprint': 'Unable to load ideas portal',
            'f_type': 'content',
        },
        'wishpond.com': {
            'service': 'Wishpond',
            'fingerprint': 'Oops! There isn’t a Wishpond Campaign published to this page.',
            'f_type': 'content',
        },
        'tumblr.com': {
            'service': 'Tumblr',
            'fingerprint': '404',
            'f_type': 'http_status',
        },
        'wordpress.com': {
            'service': 'Wordpress',
            'fingerprint': '.wordpress.com doesn\'t exist',
            'f_type': 'content',
        },
        'teamwork.com': {
            'service': 'Teamwork',
            'fingerprint': 'Oops - We didn\'t find your site',
            'f_type': 'content',
        },
        'helpjuice.com': {
            'service': 'Help Juice',
            'fingerprint': '404',
            'f_type': 'http_status',
        },
        'helpscoutdocs.com': {
            'service': 'Helps Count',
            'fingerprint': '404',
            'f_type': 'http_status',
        },
        'ghost.io': {
            'service': 'Ghost',
            'fingerprint': 'Domain error',
            'f_type': 'content',
        },
        'myshopify.com': {
            'service': 'Shopify',
            'fingerprint': 'Sorry, this shop is currently unavailable.',
            'f_type': 'content',
        },
        'uservoice.com': {
            'service': 'User Voice',
            'fingerprint': '404',
            'f_type': 'http_status',
        },
        'surge.sh': {
            'service': 'Surge',
            'fingerprint': '404',
            'f_type': 'http_status',
        },
        'bitbucket.io': {
            'service': 'Bitbucket',
            'fingerprint': '404',
            'f_type': 'http_status',
        },
        'sendgrid.net': {
            'service': 'Sendgrid',
            'fingerprint': '',
            'f_type': 'NXDOMAIN',
        },
        'feedpress.me': {
            'service': 'Feedpress',
            'fingerprint': '',
            'f_type': 'NXDOMAIN',
        },
        'webflow.io': {
            'service': 'Web Flow',
            'fingerprint': '404',
            'f_type': 'http_status',
        },
        'freshpo.com': {
            'service': 'Freshdesk',
            'fingerprint': '404',
            'f_type': 'http_status',
        },
        # Akami
        'edgekey.net': {
            'service': 'Akami',
            'fingerprint': '',
            'f_type': 'NXDOMAIN',
        },
        'edgesuite.net': {
            'service': 'Akami',
            'fingerprint': '',
            'f_type': 'NXDOMAIN',
        },
        '': {
            'service': '',
            'fingerprint': '',
            'f_type': 'content',
        },
        '': {
            'service': '',
            'fingerprint': '',
            'f_type': 'content',
        },
        '': {
            'service': '',
            'fingerprint': '',
            'f_type': 'content',
        },
    },
    # List of DNS blocklist
    # translation of numbers
    #   0: blocklist
    #   1: informational
    #   2: graylist, e.g. proxies, TOR exit/entry nodes
    #   3: redlist, e.g. misconfiguration
    #   10: allowlist
    #   40: error
    'dnsbl': {
        # usage: https://barracudacentral.org/rbl/how-to-use
        'b.barracudacentral.org': {
            'type': ['ipv4'],
            '127.0.0.2': [0, 'Spam'],
        },
        # usage: http://www.sorbs.net/general/using.shtml
        'dnsbl.sorbs.net': {
            'type': ['ipv4'],
            '127.0.0.2': [2, 'Proxy: Open HTTP Proxy Servers'],
            '127.0.0.3': [2, 'Proxy: Open SOCKS Proxy Servers'],
            '127.0.0.4': [2, 'Proxy: Other Open Proxy Servers'],
            '127.0.0.5': [1, 'SMTP: Open SMTP relay servers'],
            '127.0.0.6': [0, 'Spam: hosts that have been noted as sending spam/UCE/UBE to the admins of SORBS'],
            '127.0.0.7': [0, 'Spam: web servers which have spammer abusable vulnerabilities'],
            '127.0.0.8': [1, 'Unkown: hosts demanding that they never be tested by SORBS'],
            '127.0.0.9': [0, 'Zombie: networks hijacked from their original owners'],
            '127.0.0.10': [1, 'Unkown: Dynamic IP Address ranges'],
            '127.0.0.11': [3, 'Misconfig: domain names where the A or MX records point to bad address space'],
            '127.0.0.12': [1, 'Unkown: domain names where the owners have indicated no email should ever originate from these domains'],
            '127.0.0.14': [1, 'Unkown: IP addresses and Netblocks of where system administrators and ISPs owning the network have indicated that servers should not be present'],
        },
        # usage: https://www.uceprotect.net/en/index.php?m=3&s=0
        'dnsbl-1.uceprotect.net': {
            'type': ['ipv4'],
            '127.0.0.2': [0, 'Spam: Conservative List'],
        },
        # usage: https://www.uceprotect.net/en/index.php?m=3&s=0
        'dnsbl-2.uceprotect.net': {
            'type': ['ipv4'],
            '127.0.0.2': [0, 'Spam: Strict List'],
        },
        # usage: https://www.uceprotect.net/en/index.php?m=3&s=0
        'dnsbl-3.uceprotect.net': {
            'type': ['ipv4'],
            '127.0.0.2': [0, 'Spam: Hardliner List'],
        },
        # usage: https://www.spamhaus.org/faq/section/Spamhaus%20DBL
        'zen.spamhaus.org': {
            'type': ['ipv4'],
            '127.0.0.2': [0, 'Spam: Spamhaus Block List (SBL)'],
            '127.0.0.3': [0, 'Spam: Spamhaus SBL CSS; list is an automatically produced dataset of IP addresses that are involved in sending low-reputation email'],
            '127.0.0.4': [0, 'Spam: Spamhaus Exploits Block List (XBL); a realtime database of IP addresses of hijacked PCs infected by illegal 3rd party exploits, including open proxies (HTTP, socks, AnalogX, wingate, etc), worms/viruses with built-in spam engines, and other types of trojan-horse exploits.'],
            '127.0.0.9': [0, 'Spam: Spamhaus DROP/EDROP Data'],
            '127.0.0.10': [0, 'Spam: ISP Maintained'],
            '127.0.0.11': [0, 'Spam: Spamhaus Maintained'],
            '127.255.255.252': [40, 'Error: Typing error in DNSBL name'],
            '127.255.255.254': [40, 'Error: Query via public/open resolver'],
            '127.255.255.255': [40, 'Error: Excessive number of queries'],
        },
        # usage: https://www.spamhaus.org/faq/section/DNSBL%20Usage
        'dbl.spamhaus.org': {
            'type': ['domain'],
            '127.0.0.2': [0, 'Spam'],
            '127.0.0.4': [0, 'Phishing'],
            '127.0.0.5': [0, 'Malware'],
            '127.0.0.6': [0, 'C2'],
            '127.0.0.102': [0, 'Spam: abused legit spam'],
            '127.0.0.103': [0, 'Spam: abused spammed redirector domain'],
            '127.0.0.104': [0, 'Phishing: abused legit phish'],
            '127.0.0.105': [0, 'Malware: abused legit malware'],
            '127.0.0.106': [0, 'C2: abused legit botnet C&C'],
            '127.0.1.255': [40, 'Error: IP queries prohibited!'],
            '127.255.255.252': [40, 'Error: Typing error in DNSBL name'],
            '127.255.255.254': [40, 'Error: Query via public/open resolver'],
            '127.255.255.255': [40, 'Error: Excessive number of queries'],
        },
        'psbl.surriel.com': {
            'type': ['ipv4'],
            '127.0.0.2': [0, 'Spam: Hardliner List'],
        },
        # usage: https://www.surbl.org/lists
        'multi.surbl.org': {
            'type': ['domain'],
            '127.0.0.2': [0, 'Spam'],
            '127.0.0.4': [0, 'Spam'],
            '127.0.0.8': [0, 'Phishing'],
            '127.0.0.16': [0, 'Malware'],
            '127.0.0.32': [0, 'Sapm'],
            '127.0.0.64': [0, 'Abused'],
            '127.0.0.128': [0, 'Hacked'],
        },
        # usage: https://www.dan.me.uk/dnsbl
        'tor.dan.me.uk': {
            'type': ['ipv4', 'ipv6'],
            '127.0.0.100': [2, 'Proxy: TOR Node'],
        },
        # usage: https://www.spamcop.net/fom-serve/cache/351.html
        'bl.spamcop.net': {
            'type': ['ipv4'],
            '127.0.0.2': [0, 'Spam'],
        },
        # usage: https://www.team-cymru.com/bogon-reference-dns
        'v4.fullbogons.cymru.com': {
            'type': ['ipv4'],
            '127.0.0.2': [0, 'Bogon: Fake IPs'],
        },
        # usage: https://www.team-cymru.com/bogon-reference-dns
        'v6.fullbogons.cymru.com': {
            'type': ['ipv6'],
            '127.0.0.2': [0, 'Bogon: Fake IPs'],
        },
        # usage: http://www.wpbl.info/
        'db.wpbl.info': {
            'type': ['ipv4'],
            '127.0.0.2': [0, 'Spam'],
        },
        # usage: https://dronebl.org/docs/howtouse
        'dnsbl.dronebl.org': {
            'type': ['ipv4'],
            '127.0.0.2': [1, 'Unkown: Sample'],
            '127.0.0.3': [1, 'IRC'],
            '127.0.0.4': [2, 'Proxy: TOR'],
            '127.0.0.5': [0, 'Spam: Bottler'],
            '127.0.0.6': [0, 'Spam: Unknown spambot or drone'],
            '127.0.0.7': [0, 'Zombie: DDoS Drone'],
            '127.0.0.8': [2, 'Proxy: SOCKS Proxy'],
            '127.0.0.9': [2, 'Proxy: HTTP Proxy'],
            '127.0.0.10': [2, 'Proxy: Proxy Chain'],
            '127.0.0.11': [2, 'Proxy: Web Page Proxy'],
            '127.0.0.12': [2, 'Proxy: Open DNS Resolver'],
            '127.0.0.13': [2, 'Hacker: Brute force attackers'],
            '127.0.0.14': [2, 'Proxy: Open Wingate Proxy'],
            '127.0.0.15': [0, 'Zombie: Compromised router or gateway'],
            '127.0.0.16': [0, 'Malware: Autorooting worms'],
            '127.0.0.17': [0, 'C2: Automatically determined botnet IPs'],
            '127.0.0.18': [0, 'IRC: DNS/MX type hostname detected on IRC'],
            '127.0.0.255': [1, 'Unknown'],
        },
        # usage: https://uribl.com/about.shtml
        'multi.uribl.com': {
            'type': ['domain'],
            '127.0.0.2': [0, 'Spam'],
            '127.0.0.4': [2, 'Sapm: domains found in UBE/UCE'],
            '127.0.0.8': [3, 'Spam: domains that actively show up in mail flow, are not listed on URIBL black, and are either: being monitored, very young (domain age via whois), or use whois privacy features to protect their identity'],
        },
    },
    # details of APIs
    # for date/time formats, check out 
    # https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
    'api': {
        # whois lookup APIs
        'whoisxml': {
            'url_whois': 'https://www.whoisxmlapi.com/whoisserver/WhoisService?apiKey={0}&outputFormat=JSON&domainName={1}',
            'url_dns': 'https://www.whoisxmlapi.com/whoisserver/DNSService?apiKey={0}&outputFormat=JSON&domainName={1}&type=_all',
            'url_ip_geo': 'https://ip-geolocation.whoisxmlapi.com/api/v1?apiKey={0}&outputFormat=JSON&ipAddress={1}',
            'url_reverse_ip': 'https://dns-history.whoisxmlapi.com/api/v1?apiKey={0}&outputFormat=JSON&ipAddress={1}',
            'url_balance': 'https://user.whoisxmlapi.com/service/account-balance?apiKey={0}',
            'date_format': '%Y-%m-%dT%H:%M:%SZ',
            'api_key': random.choice(api_key_whoisxml),
        },
        'whoxy': {
            'url_whois': 'https://api.whoxy.com/?key={0}&whois={1}&format=json',
            'url_balance': 'https://api.whoxy.com/?key={0}&account=balance',
            'date_format': '%Y-%m-%d',
            'api_key': random.choice(api_key_whoxy),
        },
        # SSL certificate API
        'crt_sh': {
            'url_all': 'https://crt.sh/?q={0}&output=json',
            'url_single': 'https://crt.sh/?id={0}',
            'date_format': '%b %d %H:%M:%S %Y GMT',
        },
        # IP whois lookup API
        'ipapi': {
            'url_lookup': 'http://ip-api.com/json/{0}?fields={1}',
            # define fields you would like to get from the API
            'fields': 'status,message,continent,continentCode,country,countryCode,region,regionName,city,district,zip,lat,lon,timezone,offset,currency,isp,org,as,asname,reverse,mobile,proxy,hosting,query',
        },
        # Hacker Target API
        'hacker_target': {
            'url_hosts': 'https://api.hackertarget.com/hostsearch/?q={0}',
        },
        # Security Trails API
        'security_trails': {
            'url_subdomain': 'https://api.securitytrails.com/v1/domain/{0}/subdomains',
            'url_whois': 'https://api.securitytrails.com/v1/domain/{0}/whois',
            'url_whois_history': 'https://api.securitytrails.com/v1/history/{0}/whois',
            'api_key': random.choice(api_key_securitytrails),
        },
        # SSL Mate API
        'ssl_mate': {
            'url_all': 'https://api.certspotter.com/v1/issuances?domain={0}&include_subdomains=true&expand=dns_names&expand=issuer&expand=cert'
        },
        # DNS Spy
        'dns_spy': {
            'url': 'https://dnsspy.io/scan/{0}',
        },
        # DNS History
        'dns_history': {
            'url_subdomain': 'https://dnshistory.org/subdomains/1/{0}',
            'url_dns_history': 'https://dnshistory.org/historical-dns-records/{0}/{1}',
            'date_format': '%Y-%m-%d',
        },
        # Shodan
        'shodan': {
            'url_internet_db': 'https://internetdb.shodan.io/',
            'url_ip': 'https://api.shodan.io/shodan/host/{0}?key={1}',
            'url_dns': 'https://api.shodan.io/dns/domain/{0}?key={1}',
            'api_key': random.choice(api_key_shodan),
        },
    },
}
