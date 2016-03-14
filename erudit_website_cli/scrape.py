from collections import namedtuple

import requests

from .util import getsoup, extract_post_args

Document = namedtuple('Document', 'id type author title')
Result = namedtuple('Result', 'documents total_count startat')

ERUDIT_URL = 'https://erudit.org'

def get_simple_search_postargs():
    r = requests.get(ERUDIT_URL)
    # We have to force encoding, or else we default to latin-1, which isn't the right one.
    r.encoding = 'utf-8'
    soup = getsoup(r.text)
    form = soup.find('form', id='rechAccueilForm')
    return extract_post_args(form)

def simple_search(searchfor, startat=1, pagesize=20):
    SIMPLE_SEARCH_DATA = get_simple_search_postargs()
    data = dict(
        SIMPLE_SEARCH_DATA,
        rechercheSimple=searchfor,
        pageDebut= startat,
        taille=pagesize,
    )
    r = requests.post(ERUDIT_URL + '/recherche/', data=data)
    r.encoding = 'utf-8'

    soup = getsoup(r.text)
    table = soup.find('table', id='tableResultats')
    rows = table('tr')[2:] # first 2 rows are not results.
    documents = []
    for row in rows:
        cb = row.find('input', type='checkbox')
        docid = cb.attrs['value']
        [doctype] = row.attrs['class']
        docauthor = row.find('p', class_='auteur').text
        doctitle = row.find('p', class_='titre').text[:100]
        documents.append(Document(docid, doctype, docauthor, doctitle))

    [total_div] = soup.select('div.ongletCorpus.Tous')
    total_in_brackets = total_div.find('span', class_='nbr').get_text().strip()
    total_result_count = total_in_brackets[1:-1]
    return Result(documents, total_result_count, startat)

