from sortedcontainers import SortedList, SortedSet
import collections
import algorithms

from ..utils import parse_in, write_ans, dprint, progressbar
from .utils import *


def solve(data, seed, debug):
    R, C, F, B, T, requests, cars = data

    map = Map()
    [map.add_car(c) for c in cars]

    # sort request by score
    scored_requests = SortedSet(requests, key=lambda x: x.score)
    start_requests = SortedSet(requests, key=lambda x: x.s)
    finish_requests = SortedSet(requests, key=lambda x: x.f)

    for t in progressbar(range(T)):
        # Update map time
        map.t = t

        # Only keep valid requests
        filter_requests(requests, t, scored_requests, start_requests,
                        finish_requests)

        free_cars = map.free_cars()

    return []
