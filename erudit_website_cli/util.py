from bs4 import BeautifulSoup

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


