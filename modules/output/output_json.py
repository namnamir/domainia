#!/usr/bin/env python

import json
from colorama import Back, Fore, Style
from config import config
from modules.utils import exception_report, printer

# write into a JSON file
def json_writer(file_name, json_data):
    # write the result in the output file
    try:
        # print the name of the domain
        printer('\n [' + Fore.GREEN + '+' + Fore.WHITE + ']──┬──' + 
                Fore.RED + Back.WHITE + ' Write into {0} '.format(file_name) + Style.RESET_ALL +
                Fore.GREEN + Style.RESET_ALL + '\n      │')
        
        # open the file and start writing in it
        with open(file_name, mode='w', encoding='UTF8', newline='') as output_file:
            indent = config['output']['json']['indent']
            # write the line into the CSV file
            # json.dump(json_data, output_file)
            # s = json.dumps(json_data)
            # print(s)
            output_file.write(str(json_data))

    except IOError:
        ex = exception_report()
        printer('      │ ■ ' + Fore.RED + 'Error in in I/O (input/output).' + Style.RESET_ALL)
        if config['verbosity'] >= 4:
            printer('      │ ■■ ' + 'ERROR: ' + Fore.MAGENTA + ex[0] + ' → ' + ex[4] + ':' + ex[3] (ex[3].errno, ex[3].strerror)+ Fore.RED + '  ' + ex[1] + Style.RESET_ALL)
    except TypeError:
        ex = exception_report()
        printer('      │ ■ ' + Fore.RED + 'Error in the in serializing the JSON variable.' + Style.RESET_ALL)
        if config['verbosity'] >= 4:
            printer('      │ ■■ ' + 'ERROR: ' + Fore.MAGENTA + ex[0] + ' → ' + ex[4] + ':' + ex[3] + Fore.RED + '  ' + ex[1] + Style.RESET_ALL)
    except ValueError:
        ex = exception_report()
        printer('      │ ■ ' + Fore.RED + 'Error in values are going to be written in the JSON file.' + Style.RESET_ALL)
        if config['verbosity'] >= 4:
            printer('      │ ■■ ' + 'ERROR: ' + Fore.MAGENTA + ex[0] + ' → ' + ex[4] + ':' + ex[3] + Fore.RED + '  ' + ex[1] + Style.RESET_ALL)
    except Exception:
        ex = exception_report()
        printer('      │ ■ ' + Fore.RED + 'Error in writing into the JSON file.' + Style.RESET_ALL)
        if config['verbosity'] >= 4:
            printer('      │ ■■ ' + 'ERROR: ' + Fore.MAGENTA + ex[0] + ' → ' + ex[4] + ':' + ex[3] + Fore.RED + '  ' + ex[1] + Style.RESET_ALL)
    finally:
        # print a message shows the scan for the domain is finished
        printer('      │\n      └──' + Fore.RED + Back.WHITE + ' Finish Writing in "{0}" '.format(file_name) + Style.RESET_ALL + '\n')
