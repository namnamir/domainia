#!/usr/bin/env python


"""
    ### Subdomain: Utilities

    Here is the list of general functions used for finding subdomains
"""


from modules.utilities.error_printer import error_printer


# this function checks if the given alternative name is a subdomain or a related
# domain.
#
# domain should be a dictionary in this format
# domain_info = {'name':string, 'reason':string, 'date':string}
#
# result would be a list. The first items represent the type, and the second item
# represents the value.
# possible output
#    0: alt name and domain are the same
#    1: alt name is a subdomain
#    2: alt name is a related domain
def sub_related_domain(alt_name, domain):
    # strip the illegal chars from the alternative name
    alt_name = str(alt_name['name']).lower().strip()
    alt_name = alt_name.replace('https://', '').replace('http://', '').replace('/', '')

    if alt_name != domain.lower():
        # sanitize (subject) alternative names
        alt_name = alt_name.replace('*.', '')
        # for OpenSSL "subjectAltName"
        alt_name = alt_name.replace('DNS:', '')

        # check if it is an alt name or a related domain
        # then add it to the corresponding set
        if alt_name.endswith(domain):
            return [
                1,
                {
                    'name': alt_name.split('.' + domain)[0],
                    'reason': alt_name['reason'],
                    'date': alt_name['date']
                }
            ]
        # if it is a related domain
        else:
            return [
                2,
                {
                    'name': alt_name,
                    'reason': alt_name['reason'],
                    'date': alt_name['date']
                }
            ]
    # if the domain name and the alternative name are the same
    else:
        return [0, False]


# get the list of alternative domains and return the 2 sets
# one for subdomains and one for related domains
# domain_info should be a list in this format
# domain_info = [domain, reason, date, date_format]
def sub_related_domains(alt_names, domain_info):
    # variables to store subdomains and related domains
    subdomains = set()
    related_domains = set()

    # continue only if there is any data for it
    if alt_names:
        for alt_name in alt_names:
            # iterate over the found alternative names
            # call the function to define if the alt name is a subdomain or not
            alt_name_result = sub_related_domain(alt_name, domain_info)
            # if there is no results
            if alt_name_result[0] == 0:
                continue
            # if it is a subdomain
            elif alt_name_result[0] == 1:
                subdomains.add(alt_name_result[1])
            # if it is a related-domain
            elif alt_name_result[0] == 2:
                related_domains.add(alt_name_result[1])
            # if there was an error with getting info
            else:
                texts = [
                    f'There was an error in analyzing the alternative name',
                    '',
                    f'Code: {alt_name_result[0]} ➜ {alt_name_result[1]}'
                ]
                error_printer(True, texts)

    # return subdomain and related domain
    return [
        subdomains,
        related_domains
    ]
