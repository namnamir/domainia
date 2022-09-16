from datetime import datetime
from config import config

# get the raw date and its format, then covert it to a date object and print it in defined format
def date_formatter(raw_date, raw_date_format):
    return datetime.strptime(raw_date, raw_date_format).strftime(config['date_format'])


# get the json and check if the key/value exist
def json_checker(json_name, json_key1, json_key2):
    if json_key1 in json_name:
        if json_key2 != '' and json_key2 in json_name[json_key1]:
            return json_name[json_key1][json_key2]
        else:
            return json_name[json_key1]
    else:
        return ''


# a sub-function to parse the result of the regex find_all function
def re_position(term, pos):
    return term[pos] if (len(term) > pos) else ''