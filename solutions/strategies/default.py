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

        for r in orderbook.start_requests:
            if r.s > t + 5:
                break

            cs = map.nearby_cars(r.a, r.b, int(R))
            dprint('Nearby cars', len(cs))
            if len(cs) == 0:
                continue

            cs = sorted(cs, key=(lambda c: dist(*map.car_pos[c], r.a, r.b)))
            car_x, car_y = map.car_pos[cs[0]]
            T_fin, on_time = time_finished(car_x, car_y, r.a, r.b, r.x, r.y, t, r.s)
            map.move(cs[0], car_x, car_y, r.x, r.y, T_fin)
            orderbook.order_done(cs[0], r)

    return orderbook.get_ans(cars)
