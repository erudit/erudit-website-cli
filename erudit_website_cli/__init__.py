#!/usr/bin/env python

import argparse

import tabulate

from .scrape import simple_search

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'searchfor',
        help="The string to search for in Erudit's simple search box"
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
    results = simple_search(args.searchfor, int(args.startat), int(args.pagesize))
    headers = ["ID", "Type", "Author", "Title"]
    print(tabulate.tabulate(results.documents, headers, tablefmt='grid'))

    stopat = results.startat + len(results.documents) - 1
    print("Results {} to {} out of {}".format(results.startat, stopat, results.total_count))

if __name__ == '__main__':
    main()

