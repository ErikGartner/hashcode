import random
import importlib

from .utils import parse_in, write_ans


def solve(in_file, start_time, strategy='default', seed=0, debug=True):
    """
    Generates a solution, use seed to ensure that we can search over many different.
    """
    print('Running: {}'.format(in_file))
    random.seed(seed)

    full_path = 'solutions.strategies.%s' % strategy
    mod = importlib.import_module(full_path)
    solv_func = getattr(mod, 'solve')

    data = parse_in(in_file)
    ans = solv_func(data, seed, debug)
    write_ans(in_file, start_time, strategy, ans)
