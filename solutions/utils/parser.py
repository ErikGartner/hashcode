import datetime
import sortedcontainers
import collections

from solutions.strategies.utils import *

Request = collections.namedtuple('Request', 'n a b x y s f score')
Car = collections.namedtuple('Car', 'id')


def parse_in(in_file):
    with open(in_file, 'r') as file:
        R, C, F, N, B, T = [int(x) for x in file.readline().split()]
        requests = []
        for n in range(N):
            a, b, x, y, s, f = [int(x) for x in file.readline().split()]
            requests.append(Request(n, a, b, x, y, s, f, dist(a, b, x, y)))
    cars = [Car(f) for f in range(F)]
    return R, C, F, B, T, set(requests), cars


def parse_ans(ans_file):
    with open(ans_file, 'r') as f:
        pass


def write_ans(in_file, strategy, answer):
    """
    Takes an in_file and generates an appropriate outfile.
    Return the path to outfile.
    """
    problem_name = in_file.split('/')[-1].replace('.in', '')
    t = datetime.datetime.now().strftime("%H-%M-%S-%f")
    outfile = 'out/{}_{}_{}.ans'.format(problem_name, strategy, t)

    print('Writing {} -> {}'.format(in_file, outfile))
    with open(outfile, 'w') as f:
        f.write(answer)
