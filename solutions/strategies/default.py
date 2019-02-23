from sortedcontainers import SortedList, SortedSet
import collections
import algorithms

from ..utils import parse_in, write_ans, dprint, progressbar
from .utils import *



def solve(data, seed, debug):
    R, C, F, B, T, requests, cars = data

    map = Map()
    [map.add_car(c) for c in cars]
    orderbook = Orderbook(requests)

    for t in progressbar(range(T)):
        # Update map time
        dprint(t)
        map.t = t
        orderbook.t = t

        orderbook.purge_old()

        free_cars = map.free_cars()
        dprint('Free cars:', len(free_cars))

        SEARCH_DIST = 5

        upcoming_requests = SortedSet([], key=lambda x: x.score)
        for r in orderbook.start_requests:
            if r.s > t + SEARCH_DIST:
                break
            upcoming_requests.add(r)

        for r in reversed(upcoming_requests):
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
