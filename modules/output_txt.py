#!/usr/bin/env python

from colorama import Back, Fore, Style
from config import config
from modules.utils import exception_report

# write into a JSON file
def txt_writer(file_name):
    # write the result in the output file
    try:
        # print the name of the domain
        print('\n [' + Fore.GREEN + '+' + Fore.WHITE + ']──┬──' + 
                Fore.RED + Back.WHITE + ' Write into {0} '.format(file_name) + Style.RESET_ALL +
                Fore.GREEN + Style.RESET_ALL + '\n      │')
        
        # open the file and start writing in it
        with open(file_name, mode='w', encoding='UTF8', newline='') as output_file:
            # write the line into the CSV file
            from modules.utils import all_prints
            output_file.write(all_prints)

        # close the file
        output_file.close()

    except IOError:
        ex = exception_report()
        print('      │ ■ ' + Fore.RED + 'Error in in I/O (input/output).' + Style.RESET_ALL)
        if config['verbosity'] >= 4:
            print('      │ ■■ ' + 'ERROR: ' + Fore.MAGENTA + ex[0] + ' → ' + ex[4] + ':' + ex[3] (ex[3].errno, ex[3].strerror)+ Fore.RED + '  ' + ex[1] + Style.RESET_ALL)
    except TypeError:
        ex = exception_report()
        print('      │ ■ ' + Fore.RED + 'Error in the in serializing the TXT variable.' + Style.RESET_ALL)
        if config['verbosity'] >= 4:
            print('      │ ■■ ' + 'ERROR: ' + Fore.MAGENTA + ex[0] + ' → ' + ex[4] + ':' + ex[3] + Fore.RED + '  ' + ex[1] + Style.RESET_ALL)
    except ValueError:
        ex = exception_report()
        print('      │ ■ ' + Fore.RED + 'Error in values are going to be written in the TXT file.' + Style.RESET_ALL)
        if config['verbosity'] >= 4:
            print('      │ ■■ ' + 'ERROR: ' + Fore.MAGENTA + ex[0] + ' → ' + ex[4] + ':' + ex[3] + Fore.RED + '  ' + ex[1] + Style.RESET_ALL)
    except Exception:
        ex = exception_report()
        print('      │ ■ ' + Fore.RED + 'Error in writing into the TXT file.' + Style.RESET_ALL)
        if config['verbosity'] >= 4:
            print('      │ ■■ ' + 'ERROR: ' + Fore.MAGENTA + ex[0] + ' → ' + ex[4] + ':' + ex[3] + Fore.RED + '  ' + ex[1] + Style.RESET_ALL)
    finally:
        # print a message shows the scan for the domain is finished
        print('      │\n      └───' + Fore.RED + Back.WHITE + ' Finish Writing in "{0}" '.format(file_name) + Style.RESET_ALL + '\n')