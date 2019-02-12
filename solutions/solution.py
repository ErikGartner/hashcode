import random

import sortedcontainers
import collections
import algorithms

from .utils import parse_in, write_ans, dprint, progressbar


def solve(in_file, seed=0, debug=True):
    """
    Generates a solution, use seed to ensure that we can search over many different.
    """
    print('Running: {}'.format(in_file))
    random.seed(seed)

    # Use progressbar to display progress in the solution
    for x in progressbar(range(100000)):
        pass

    parse_in(in_file)
    write_ans(in_file, [])
