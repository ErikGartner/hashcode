from sortedcontainers import SortedList
import collections
import algorithms

from ..utils import parse_in, write_ans, dprint, progressbar
from .utils import *


def solve(data, seed, debug):
    R, C, F, B, T, requests, cars = data

    map = Map()
    [map.add_car(c) for c in cars]


    # sort request by score
    score_requests = SortedList(requests, key=lambda x: x.score)

    for t in progressbar(range(T)):
        # Only keep valid requests
        requests = filter_requests(requests, t)


        for request in reversed(requests):
            pass



    return []
