#!/usr/bin/env python

import argparse

import tabulate

from .scrape import simple_search, complex_search

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'searchfor',
        nargs='+',
        help="The string to search for in Erudit's simple search box. Multiple args are AND-connected."
    )
    parser.add_argument(
        '--or',
        dest='searchfor_or',
        action='append',
        help="Add a search string to 'searchfor', but OR-connected."
    )
    parser.add_argument(
        '--pagesize',
        default='20',
        help="Maximum number of results that we get in our results"
    )
    parser.add_argument(
        '--startat',
        default='1',
        help="Index at which our results should start"
    )
    return parser.parse_args()

def main():
    args = parse_args()
    if len(args.searchfor) > 1:
        results = complex_search(
            args.searchfor,
            searchfor_or=args.searchfor_or,
            startat=int(args.startat),
            pagesize=int(args.pagesize)
        )
    else:
        results = simple_search(
            args.searchfor[0],
            startat=int(args.startat),
            pagesize=int(args.pagesize)
        )
    headers = ["ID", "Type", "Author", "Title"]
    print(tabulate.tabulate(results.documents, headers, tablefmt='grid'))

    stopat = results.startat + len(results.documents) - 1
    print("Results {} to {} out of {}".format(results.startat, stopat, results.total_count))

if __name__ == '__main__':
    main()

