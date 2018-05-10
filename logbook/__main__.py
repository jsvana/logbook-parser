import argparse
from datetime import timedelta
from pathlib import Path
import sys


from tabulate import tabulate


from .parser import Logbook


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'logbook_file',
        type=Path,
        help='Path to ForeFlight logbook export CSV',
    )
    return parser.parse_args()


def main():
    args = parse_args()

    logbook = Logbook(args.logbook_file)

    rows = [
        ['All', logbook.total_time],
        ['Last seven days', logbook.hours_in_last(timedelta(days=7))],
        ['Last 30 days', logbook.hours_in_last(timedelta(days=30))],
        ['Last 90 days', logbook.hours_in_last(timedelta(days=90))],
        ['Last six months', logbook.hours_in_last(timedelta(days=180))],
        ['Last year', logbook.hours_in_last(timedelta(days=365))],
    ]
    print('Summary')
    print(tabulate(rows, tablefmt='plain'))


    rows = [
        [
            'General (ASEL)',
            *logbook.general_currency_expiration('airplane_single_engine_land'),
        ],
        [
            'Night (ASEL)',
            *logbook.night_currency_expiration('airplane_single_engine_land'),
        ],
        [
            'Tailwheel (ASEL)',
            *logbook.tailwheel_currency_expiration('airplane_single_engine_land'),
        ],
        [
            'Flight Review',
            *logbook.bfr_currency_expiration(),
        ],
    ]
    print()
    print('Currency')
    print(tabulate(rows, headers=['type', 'expiry', 'days_remaining']))


sys.exit(main())
