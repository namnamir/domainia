#!/usr/bin/env python

from colorama import Back, Fore, Style
# import csv
import json
import yaml
from typing import Dict

from config import config
import global_variable
from modules.utilities.printer import printer
from modules.utilities.error_printer import error_printer


def output_writer(file_name: str, formats: str, dict_data: Dict) -> None:
    """
    This function converts the given dictionary to different formats.
    If the format is TXT, it gets all STDOUT terms from 'ALL_PRINTS' then write into a file.
    If the format is JSON, it converts the dictionary of the data into a JSON data and then write into a file.
    If the format is YAML, it converts the dictionary of the data into a YAML data and then write into a file.
    If the format is CSV, it calls another function.

    Args:
        file_name (str): The name of the file to write the JSON data to.
        dict_data (dict): The dictionary containing the data to write to the file.
    """
    # Print the name of the domain
    printer(f'\n [{Fore.GREEN}☵{Fore.WHITE}]──{Fore.RED}{Back.WHITE} Writing into files.{Style.RESET_ALL}')

    # Iterate over formats
    i = 1
    for format in formats:
        # Form the extension of the file based on the selected "formant"
        if format in ('json_beautiful', 'json_b', 'b_json', 'beautiful_json'):
            extension = 'json'
        else:
            extension = format

        # Print the output location
        line = '└' if i == len(formats) else '├'
        printer(f'      {line}─── {Fore.CYAN}{file_name}.{extension}{Style.RESET_ALL}')

        # Write the result in the output file based on the selected format
        try:
            # Open the file and start writing in it
            with open(f"{file_name}.{extension}", mode='w', encoding='UTF8', newline='') as output_file:
                if format == "csv":
                    # output = csv.writer(output_file, quoting=csv.QUOTE_MINIMAL)
                    # start the recursive flattening process
                    # flatten_json(json_data)
                    continue

                # If the format is JSON (compact JSON)
                elif format == 'json':
                    output = json.dumps(dict_data, separators=(",", ":"), default=str, ensure_ascii=False)

                # If the format is JSON (Beautiful JSON)
                elif format in ['json_beautiful', 'json_b', 'b_json', 'beautiful_json']:
                    indent = config['output']['json']['indent']
                    output = json.dumps(dict_data, indent=indent, default=str, ensure_ascii=False)

                # If the format is YAML
                elif format == 'yaml':
                    indent = config['output']['yaml']['indent']
                    output = yaml.dump(dict_data, indent=indent, allow_unicode=True)

                # If the format is TXT (text)
                elif format == "txt":
                    output = global_variable.ALL_PRINTS

                # Print the output
                output_file.write(str(output))

        except IOError:
            texts = ['Error in in I/O (input/output).']
            error_printer('exception', texts)
        except TypeError:
            texts = [f'Error in the in serializing the "{format}" variable.']
            error_printer('exception', texts)
        except ValueError:
            texts = [f'Error in values are going to be written in the "{format}" file.']
            error_printer('exception', texts)
        except Exception:
            texts = [f'Error in writing into the "{format}" file.']
            error_printer('exception', texts)

        # Increment the counter of the formats
        i += 1

    # Print an empty line
    printer('\n')
