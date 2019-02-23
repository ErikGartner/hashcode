from collections import defaultdict
from sortedcontainers import SortedSet


def dist(a, b, x, y):
    return abs(a - x) + abs(b - y)


def filter_requests(finished_request, t, *request_sets):
    to_remove = set()
    for r in finished_request:
        if t + r.score <= r.f:
            break
        to_remove.add(r)
    for r in to_remove:
        finished_request.remove(r)
        [rs.remove(r) for rs in request_sets]


def time_finished(car_x, car_y, a, b, x, y, t, s):
    T = t
    T += dist(car_x, car_y, a, b)
    on_time = T <= s
    T += max(0, T - s)
    T += dist(a, b, x, y)
    return T, on_time


class Map():

    def __init__(self):
        self.cars = defaultdict(lambda: set())
        self.car_pos = {}
        self.t = 0
        self.car_ready_times = {}

    def add_car(self, car):
        self.cars[(0, 0)].add(car)
        self.car_pos[car] = (0, 0)
        self.car_ready_times[car] = 0

    def cars(self, x, y):
        return [c for c in self.cars[(x, y)] if self.car_ready_times[c] <= self.t]

    def move(self, car, x1, y1, x2, y2, T):
        """Move a car from x1, y1 to x2, y2, it will be ready at time T"""
        assert(car in self.cars[(x1, y1)])
        self.cars[(x1, y1)].remove(car)
        self.cars[(x2, y2)].add(car)
        self.car_pos[car] = (x2, y2)
        self.car_ready_times[car] = T

    def nearby_cars(self, x, y, radius):
        cars = set()
        for xr in range(x - radius, x + radius + 1):
            for yr in range(y - radius, y + radius + 1):
                cars.update(self.cars[(xr, yr)])
        return cars

    def free_cars(self):
        return set([c for c, t in self.car_ready_times.items() if t <= self.t])


class Orderbook():

    def __init__(self, requests):
        # sort request by score
        self.scored_requests = SortedSet(requests, key=lambda x: x.score)
        self.start_requests = SortedSet(requests, key=lambda x: x.s)
        self.finish_requests = SortedSet(requests, key=lambda x: x.f)
        self.requests = requests
        self.done = defaultdict(lambda: list())
        self.t = 0

    def purge_old(self):
        filter_requests(self.finish_requests,
                        self.t,
                        self.requests,
                        self.scored_requests,
                        self.start_requests)

    def order_done(self, c, r):
        self.requests.remove(r)
        self.scored_requests.remove(r)
        self.start_requests.remove(r)
        self.finish_requests.remove(r)
        self.done[c].append(r.n)

    def get_ans(self, cars):
        ans = ''
        for c in cars:
            ans += '{} {}\n'.format(c.id, ' '.join([str(x) for x in self.done[c]]))
        return ans
