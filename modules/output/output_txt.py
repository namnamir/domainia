#!/usr/bin/env python

from colorama import Back, Fore, Style

from config import config
from modules.utilities.exception_handling import exception_details
from modules.utilities.printer import printer
from modules.utilities.printer import ALL_PRINTS


def txt_writer(file_name: str) -> None:
    """
    This function gets all STDOUT terms from 'ALL_PRINTS' then write into a file.

    Args:
        file_name (str): The name of the file to write the JSON data to.
    """
    try:
        # print the name of the domain
        printer(f'\n [{Fore.GREEN}+{Fore.WHITE}]──┬──{Fore.RED}{Back.WHITE} Write into '
                f'{file_name}{Style.RESET_ALL}{Fore.GREEN}{Style.RESET_ALL}\n      │')

        # open the file and start writing in it
        with open(file_name, mode='w', encoding='UTF8', newline='') as output_file:
            # write the line into the CSV file
            output_file.write(ALL_PRINTS)

    except IOError:
        ex = exception_details()
        printer(f'      │ ■ {Fore.RED}Error in in I/O (input/output).{Style.RESET_ALL}')
        if config['verbosity'] >= 4:
            printer(f'      │ ■■ ERROR: {Fore.MAGENTA}{ex[0]} → {ex[4]}:{ex[3]} ({ex[3].errno}, {ex[3].strerror}) '
                    f'{Fore.RED}  {ex[1]}{Style.RESET_ALL}')
    except TypeError:
        ex = exception_details()
        printer(f'      │ ■ {Fore.RED}Error in the in serializing the TXT variable.{Style.RESET_ALL}')
        if config['verbosity'] >= 4:
            printer(f'      │ ■■ ERROR: {Fore.MAGENTA}{ex[0]} → {ex[4]}:{ex[3]}{Fore.RED}  {ex[1]}{Style.RESET_ALL}')
    except ValueError:
        ex = exception_details()
        printer(f'      │ ■ {Fore.RED}Error in values are going to be written in the TXT file.{Style.RESET_ALL}')
        if config['verbosity'] >= 4:
            printer(f'      │ ■■ ERROR: {Fore.MAGENTA}{ex[0]} → {ex[4]}:{ex[3]}{Fore.RED}  {ex[1]}{Style.RESET_ALL}')
    except Exception:
        ex = exception_details()
        printer(f'      │ ■ {Fore.RED}Error in writing into the TXT file.{Style.RESET_ALL}')
        if config['verbosity'] >= 4:
            printer(f'      │ ■■ ERROR: {Fore.MAGENTA}{ex[0]} → {ex[4]}:{ex[3]}{Fore.RED}  {ex[1]}{Style.RESET_ALL}')
    finally:
        # print a message shows the scan for the domain is finished
        printer(f'      │\n      └──{Fore.RED}{Back.WHITE} Finish Writing in "{file_name}" {Style.RESET_ALL}\n')
