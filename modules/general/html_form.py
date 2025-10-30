#!/usr/bin/env python

from typing import List, Dict
from bs4 import BeautifulSoup


def form_finder(soup: BeautifulSoup) -> List[Dict[str, any]]:
    """
    This function looks for any forms within the HTML page including all fields.

    Args:
        soup (BeautifulSoup): The BeautifulSoup format of the HTML page

    Returns:
        List[Dict[str, any]]: A list containing all forms with their fields
    """
    forms = []

    # find 'form' elements within the HTML content
    all_forms = soup.find_all('form')

    # iterate over forms in the HTML page
    for form in all_forms:
        # a variable to store inputs of the form
        fields = []

        # get the inputs
        inputs = form.find_all('input')

        # iterate over fields ('input' elements) in the form
        if inputs:
            for input in inputs:
                fields.append({
                    'type': input.get('type', ''),
                    'name': input.get('name', ''),
                    'id': input.get('id', ''),
                    'value': input.get('value', ''),
                    'placeholder': input.get('placeholder', '')
                })

        # write findings in the list
        forms.append({
            'method': form.get('method', ''),
            'action': form.get('action', ''),
            'name': form.get('name', ''),
            'id': form.get('id', ''),
            'fields': fields
        })

    # return results
    return forms
