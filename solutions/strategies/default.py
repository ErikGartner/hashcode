from sortedcontainers import SortedList, SortedSet
import collections
import algorithms

from ..utils import parse_in, write_ans, dprint, progressbar, timethis
from .utils import *


def solve(data, seed, debug):
    R, C, F, B, T, requests, cars = data

    map = Map()
    [map.add_car(c) for c in cars]
    orderbook = Orderbook(requests)

    for t in progressbar(range(T)):
        # Update map time
        map.t = t
        orderbook.t = t

        orderbook.purge_old()

        free_cars = map.free_cars()
        SEARCH_DIST = 20

        upcoming_requests = set()
        for r in orderbook.start_requests.islice(None, 100, True):
            if r.s > t + SEARCH_DIST:
                break

            if r.f >= t + SEARCH_DIST:
                upcoming_requests.add(r)
        upcoming_requests = SortedSet(upcoming_requests, key=lambda x: x.score)

        for r in upcoming_requests.islice(-5, None, True):
            if len(free_cars) == 0:
                break

            cs = map.nearby_cars(r.a, r.b, SEARCH_DIST)
            if len(cs) == 0:
                continue

            cs = sorted(cs, key=(lambda c: dist(*map.car_pos[c], r.a, r.b)))
            assign_car(cs[0], r, t, map, orderbook, free_cars)

        # Assign unused cars
        for r in orderbook.start_requests:
            if len(free_cars) == 0:
                break

            cs = sorted(free_cars, key=(lambda c: dist(*map.car_pos[c], r.a, r.b)))
            assign_car(cs[0], r, t, map, orderbook, free_cars)

    return orderbook.get_ans(cars)
