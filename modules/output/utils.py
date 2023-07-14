#!/usr/bin/env python


"""
    ### Output: Utilities

    Here is the list of general functions used for generating output files
"""

from typing import Dict

from config import config


def flatten_json(y):
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out


def flatten_json(init_key: str, input: Dict, output: Dict) -> Dict:
    """
    Flatten a nested JSON object into a flat dictionary.
    i.e. {'a': {'b': 1, 'c': {'d': 2}}, 'e': 3} ===> {'a_b': 1, 'a_c_d': 2, 'e': 3}

    Args:
        init_key (str): The initial key to use when flattening the JSON object.
        input (Dict): The JSON object to flatten.
        output (Dict): The dictionary to store the flattened JSON.

    Returns:
        A dictionary containing the flattened JSON object.
    """
    joiner = config['output']['csv']['header_joiner']

    # iterate over keys & values recursively
    for key, value in input.items():
        # check if the json contains another jason (is nested)
        if isinstance(value, dict):
            # run the function recursively
            flatten_json(init_key + key + joiner, value, output)
        else:
            output[init_key + key] = value
    return output

# make the json flat
# i.e. {'a': {'b': 1, 'c': {'d': 2}}, 'e': 3}
# ===> {'a_b': 1, 'a_c_d': 2, 'e': 3}
def flatten_json_old(init_key, json, results):
    joiner = config['output']['csv']['header_joiner']
    # iterate over keys & values recursively
    for key, value in json.items():
        # check if the json contains another jason (is nested)
        if isinstance(value, dict):
            init_key += key + joiner
            # run the function recursively
            flatten_json_old(init_key, value, results)
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

    # print(json.keys(), '\n\n')
    # print(config_json.keys(), '\n\n')
    # iterate over keys & values
    if isinstance(json, dict):
        # iterate over the flatted JSON
        for key, value in json.items():
            # check if it is True in config file to be written in CSV or not
            # additionally ignore the ones that are not in the config
            if key in config_json and config_json[key]:
                print('---------6---------', key)

            if key not in config_json:
                print('---------1---------', key)

            if isinstance(value, list):
                if isinstance(value[0], dict):
                    continue
                value = delimiter.join(value)

            keys.add(key)
            values.append(str(value))
            both[key] = str(value)
    else:
        values = json

    print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
    # return results
    return [
        keys,
        values,
        both
    ]
