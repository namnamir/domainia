#!/usr/bin/env python

import re

import global_variable


def printer(term: str) -> None:
    """
    This function writes the input term on STDOUT, then removes any ANSI escape
    sequences (sanitization) and keeps the result to be written in a text file.

    Args:
        term: The text that should be written on STDOUT and in the text file
    """
    global ALL_PRINTS

    # Print the term on the terminal (STDOUT)
    print(term)

    # Remove ANSI escape sequences from the term to be able to save it into a file
    term = re.sub(r'\x1B\[\d+m', '', term)

    # Save the term in a global variable to save in a file later
    global_variable.ALL_PRINTS += term + '\n'
