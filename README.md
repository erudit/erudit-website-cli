# erudit-website-cli

A CLI (and, also, a library) to access search results from [erudit.org](https://erudit.org).

This is a very early version of the library, so documentation is sparse.

## Installation

    $ python3 -m venv env
    $ . env/bin/activate
    $ python setup.py install
    $ erudit-website-cli arendt

## Usage

For command line usage, use the `-h` flag to see all options.

You can also use the package as a library:

    >>> from erudit_website_cli.scrape import simple_search
    >>> results = simple_search('arendt', startat=42, pagesize=12)
    >>> results
    >>> results.total_count
    '1112'
    >>> results.startat
    42
    >>> len(results.documents)
    12
    >>> results.documents[0]
    Document(id='009512ar', type='Article', author='Ritha Cossette', title="Compte renduHannah Arendt, l'amour de la liberté de Francis Moreault, Québec, Les Presses de l'Unive")

