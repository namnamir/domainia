#!/usr/bin/env python


"""
    ### Output: Utilities

    Here is the list of general functions used for generating output files
"""


from config import config


# make the json flat
# i.e. {'a': {'b': 1, 'c': {'d': 2}}, 'e': 3}
# ===> {'a_b': 1, 'a_c_d': 2, 'e': 3}
def flat_json(init_key, json, results):
    joiner = config['output']['csv']['header_joiner']
    # iterate over keys & values recursively
    for key, value in json.items():
        # check if the json contains another jason (is nested)
        if isinstance(value, dict):
            init_key += key + joiner
            # run the function recursively
            flat_json(init_key, value, results)
            # sanitize the aggregated key
            init_key = init_key[:-len(key + joiner)]
        else:
            init_key += key
            results[init_key] = value
            # sanitize the aggregated key
            init_key = init_key[:-len(key)]
    # return results
    return results


# it will get the json, make it flat, and return keys and values in separate lists
# it also checks if it is asked (in the config file) to be in the CSV file or not
# if not, it will be ignored from the output lists
def csv_maker(json, config_json):
    keys = set()
    values = list()
    both = dict()

    #
    delimiter = config['output']['csv']['delimiter']['other']

    # make the json flat
    json = flat_json('', json, {})
    if config_json:
        config_json = flat_json('', config_json, {})

    # iterate over keys & values
    if isinstance(json, dict):
        # iterate over the flatted JSON
        for key, value in json.items():
            # check if it is True in config file to be written in CSV or not
            # if (key in config_json) and config_json[key]:
                if isinstance(value, list):
                    value = delimiter.join(value)

                keys.add(key)
                values.append(str(value))
                both[key] = str(value)
    else:
        values = json
    
    # return results
    return [
        keys,
        values,
        both
    ]