import random

import tqdm
import sortedcontainers
import collections
import algorithms

from .utils.parser import parse_in, write_ans


def solve(in_file, seed=0):
    """
    Generates a solution, use seed to ensure that we can search over many different.
    """
    random.seed(seed)
