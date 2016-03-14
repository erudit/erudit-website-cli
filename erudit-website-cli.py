#!/usr/bin/env python

import argparse

import requests
from bs4 import BeautifulSoup
import tabulate

ERUDIT_URL = 'https://erudit.org'

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'searchfor',
        help="The string to search for in Erudit's simple search box"
    )
    return parser.parse_args()

def getsoup(content):
    return BeautifulSoup(content, 'html.parser')

def extract_post_args(soup):
    """Returns a ``post()``-ready dict of all input/select values in ``soup``.

    If you have multiple forms in your response, be sure to supply a sub-soup if you don't want
    all inputs in the page to be included.
    """
    result = {}
    for input in soup('input'):
        if 'name' not in input.attrs:
            continue
        if input.attrs['type'] == 'checkbox':
            value = 'on' if input.attrs.get('checked') else ''
        else:
            value = input.attrs.get('value', '')
        result[input.attrs['name']] = value
    for select in soup('select'):
        if 'multiple' in select.attrs:
            value = [elem.attrs['value'] for elem in select('option', attrs={'selected': 'selected'})]
        else:
            try:
                value = select('option', attrs={'selected': 'selected'})[0].attrs['value']
            except IndexError:
                value = ''
        result[select.attrs['name']] = value
    return result

def main():
    args = parse_args()
    r = requests.get(ERUDIT_URL)
    # We have to force encoding, or else we default to latin-1, which isn't the right one.
    r.encoding = 'utf-8'
    soup = getsoup(r.text)
    form = soup.find('form', id='rechAccueilForm')

    SIMPLE_SEARCH_DATA = extract_post_args(form)

    data = dict(SIMPLE_SEARCH_DATA, rechercheSimple=args.searchfor)
    r = requests.post('http://erudit.org/recherche/', data=data)
    r.encoding = 'utf-8'

    soup = getsoup(r.text)
    table = soup.find('table', id='tableResultats')
    rows = table('tr')[2:] # first 2 rows are not results.
    results = []
    for row in rows:
        cb = row.find('input', type='checkbox')
        docid = cb.attrs['value']
        [doctype] = row.attrs['class']
        docauthor = row.find('p', class_='auteur').text
        doctitle = row.find('p', class_='titre').text[:100]
        results.append((docid, doctype, docauthor, doctitle))

    headers = ["ID", "Type", "Author", "Title"]
    print(tabulate.tabulate(results, headers))

if __name__ == '__main__':
    main()

