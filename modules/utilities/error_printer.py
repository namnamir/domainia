#!/usr/bin/env python

from colorama import Fore, Style
from config import config

from modules.utilities.printer import printer
from modules.utilities.exception_handling import exception_details


def error_printer(flag, texts):
    """
    This function prints errors related to the exceptions, based on verbosity

    Args:
        flag (str | boolean): "exception" or True to print based on verbosity, and
                              False to print nothing as the error
        texts (list): a list contains text for each verbosity in the following format
                      ["text for verbosity 1", ..., "text for verbosity 5"]
    """
    verbosity_1 = '      │        ├─1─■ '
    verbosity_2 = '      │        ├─2─■ '
    verbosity_3 = '      │        ├─3─■ '
    verbosity_4 = '      │        ├─4─■ '
    verbosity_5 = '      │        ├─5─■ '

    # if flag is True/exception and verbosity is not 0 (or False)
    if flag and config['verbosity']:
        # print error messages for verbosity 1 (-v)
        if (
            config['verbosity'] >= 1
            and len(texts) >= 1
            and texts[0]
        ):
            printer(f'{verbosity_1}{Fore.RED}{texts[0]}{Style.RESET_ALL}')

        # print error messages for verbosity 2 (-vv)
        if (
            config['verbosity'] >= 2
            and len(texts) >= 2
            and texts[1]
        ):
            printer(f'{verbosity_2}{Fore.RED}{texts[1]}{Style.RESET_ALL}')

        # print error messages for verbosity 3 (-vvv)
        if (
            config['verbosity'] >= 3
            and len(texts) >= 3
            and texts[2]
        ):
            printer(f'{verbosity_3}{Fore.RED}{texts[2]}{Style.RESET_ALL}')

        # print error messages for verbosity 4 (-vvvv)
        if (
            config['verbosity'] >= 4
            and len(texts) >= 4
            and texts[3]
        ):
            printer(f'{verbosity_4}{Fore.RED}{texts[3]}{Style.RESET_ALL}')

        # print error messages for verbosity 5 (-vvvvv)
        if config['verbosity'] >= 5:
            if (
                len(texts) >= 5
                and texts[4]
            ):
                printer(f'{verbosity_5}{Fore.RED}{texts[4]}{Style.RESET_ALL}')

            # in case, it is an exception error message
            if flag == 'exception':
                ex = exception_details()
                printer(f'{verbosity_5}Exception Message: {Fore.MAGENTA}{ex[0]} ➜ '
                        f'{ex[4]}:{ex[3]}{Fore.RED} == {ex[2]} ⚊ {ex[1]}{Style.RESET_ALL}')
