#!/usr/bin/env python


"""
    ### SSL Certificates: OpenSSL

    This function get the certificate details from Python OpenSSL module (pyOpenSSL).
    It first gets the list of all certificates, sort them by ID, and load the 
    latest certificate (based on ID). Afterwards, parse the page using RE.

    # Input:  - a single domain name
    # Output: - a dictionary contains SSL certificate details
"""


from datetime import datetime
import OpenSSL
import ssl
from config import config
from modules.utils import date_formatter, except_error_print, alt_name_sanitizer


def openssl(domain):
    # a variable to store cert info
    cert_info = dict()
    # set the print arguments for the function "except_error_print"
    print_args = [True, '      │        ├──■ ', '      │        ├──■■ ']

    try:
        # get the certificate
        cert = ssl.get_server_certificate((domain, 443))
        # parse the certificate
        x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)

        # iterate over the certificate extensions to get alternative names
        for i in range(0, x509.get_extension_count()):
            extension = x509.get_extension(i)
            if 'subjectAltName' in str(extension.get_short_name()):
                alt_names = str(extension).split(',')
                sub, alt = alt_name_sanitizer(alt_names, domain)
                cert_info['subdomains'].update(sub)
                cert_info['related_domains'].update(alt)

        # parse cert info and write into a dictionary
        cert_info['expired'] = x509.has_expired()
        cert_info['serial_number'] = str(x509.get_serial_number())
        cert_info['version'] = x509.get_version()
        cert_info['signature'] = x509.get_signature_algorithm()
        cert_info['validity']['issue_date'] = date_formatter(x509.get_notBefore().decode('ascii'), '%Y%m%d%H%M%SZ')
        cert_info['validity']['expiration_date'] = date_formatter(x509.get_notAfter().decode('ascii'), '%Y%m%d%H%M%SZ')
        cert_info['validity']['days'] = (cert_info['validity']['expiration_date'] - cert_info['validity']['issue_date']).days
        cert_info['validity']['past_days'] = (datetime.now() - datetime.strptime(cert_info['validity']['issue_date'], config['date_format'])).days
        cert_info['validity']['left_days'] = (datetime.strptime(cert_info['validity']['expiration_date'], config['date_format']) - datetime.now()).days
        cert_info['fingerprint']['md5'] = x509.digest('md5').decode()
        cert_info['fingerprint']['sha1'] = x509.digest('sha1').decode()
        cert_info['fingerprint']['sha256'] = x509.digest('sha256').decode()
        cert_info['fingerprint']['sha512'] = x509.digest('sha512').decode()
        cert_info['issuer']['common_name'] = x509.get_issuer().CN
        cert_info['issuer']['organization_name'] = x509.get_issuer().O
        cert_info['issuer']['organization_unit_name'] = x509.get_issuer().OU
        cert_info['issuer']['country'] = x509.get_issuer().C
        cert_info['issuer']['state'] = x509.get_issuer().ST
        cert_info['issuer']['city'] = x509.get_issuer().L
        cert_info['issuer']['email_address'] = x509.get_issuer().emailAddress
        cert_info['subject']['common_name'] = x509.get_subject().CN
        cert_info['subject']['organization_name'] = x509.get_subject().O
        cert_info['subject']['organization_unit_name'] = x509.get_subject().OU
        cert_info['subject']['country'] = x509.get_subject().C
        cert_info['subject']['state'] = x509.get_subject().ST
        cert_info['subject']['city'] = x509.get_subject().L
        cert_info['subject']['email_address'] = x509.get_subject().emailAddress

    except ssl.SSLError as err:
        args = [print_args, f'There is an error in certificate of the host "{domain}" is failed.', err, '']
        except_error_print(args)
    except Exception:
        args = [print_args, f'Error in getting or parsing certificate for the host "{domain}".', '', '']
        except_error_print(args)

    return cert_info
