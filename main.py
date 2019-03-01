import argparse
import glob
import os
import profile
import pstats
import zipfile
import datetime

from solutions import solve, score_answers
from solutions.utils import status


def main(problem_filter, start_time, strategy, seed, debug):
    status.DEBUG = debug

    for in_file in sorted(glob.glob(os.path.join('data', problem_filter) + '*')):
        try:
            solve(in_file, start_time, strategy, seed, debug)
        except KeyboardInterrupt as e:
            pass


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
    parser.add_argument('--profile', action='store_true',
                        help='profile the code')
    parser.add_argument('--score', action='store_true',
                        help='score answers')
    parser.add_argument('--nozip', action='store_true',
                        help='disable creating zip of the current code state')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    if args.score:
        score_answers()
        exit(0)

    start_time = datetime.datetime.now().strftime("%H-%M-%S-%f")

    if not args.nozip:
        excluded_dirs = set(['data', 'out', 'tests', 'venv', '__pycache__'])
        zip_path = './out/%s_code.zip' % start_time
        ziphandle = zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED)
        for root, dirs, files in os.walk('.', topdown=True):
            dirs[:] = [d for d in dirs if d not in excluded_dirs]
            for file in files:
                ziphandle.write(os.path.join(root, file))
        ziphandle.close()

    if args.profile:
        print('Profiling...')
        profile.runctx('m(p, st, s, d)',
                       {'m': main,
                        'p': args.problem,
                        'st': args.strategy,
                        's': args.seed,
                        'd': args.debug}, {}, filename='profile_log')
        p = pstats.Stats('profile_log')
        p.strip_dirs().sort_stats('cumulative').print_stats()
    else:
        main(args.problem, start_time, args.strategy, args.seed, args.debug)
