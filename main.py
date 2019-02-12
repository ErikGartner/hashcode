import argparse
import glob

from solutions import solve


def main(problem_filter):
    for in_file in sorted(glob.glob(os.path.join('data', problem_filter))):
        solve(in_file)


def parse_args():
    """Arg parsing"""
    parser = argparse.ArgumentParser(description='Hashcode Solution')
    parser.add_argument('problem', type=String, nargs='?',
                        help='a filter for the problem / data to run on')
    args = parser.parse_args()


if __name__ == '__main__':
    parse_args()
    main()
