import argparse
import glob
import os

from solutions import solve
from solutions.utils import status


def main(problem_filter, strategy, seed, debug):
    status.DEBUG = debug

    for in_file in sorted(glob.glob(os.path.join('data', problem_filter) + '*')):
        solve(in_file, strategy, seed, debug)


def parse_args():
    """Arg parsing"""
    parser = argparse.ArgumentParser(description='Hashcode Solution')
    parser.add_argument('--strategy', type=str, nargs='?', default='default',
                        help='the strategy module name')
    parser.add_argument('--problem', type=str, nargs='?', default='',
                        help='a filter for the problem / data to run on')
    parser.add_argument('--seed', type=int, nargs='?', default=0,
                        help='seed for random functions')
    parser.add_argument('--debug', action='store_true',
                        help='show messages / progressbars')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    main(args.problem, args.strategy, args.seed, args.debug)
