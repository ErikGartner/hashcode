from collections import defaultdict


def dist(a, b, x, y):
    return abs(a - x) + abs(b - y)


def filter_requests(requests, t, *request_sets):
    to_remove = set()
    for r in requests:
        if r.f <= t:
            break
        to_remove.add(r)
    for r in to_remove:
        requests.remove(r)
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
        self.t = 0
        self.car_ready_times = {}

    def add_car(self, car):
        self.cars[(0, 0)].add(car)
        self.car_ready_times[car] = 0

    def cars(self, x, y):
        return [c for c in self.cars[(x, y)] if self.car_ready_times[c] <= self.t]

    def move(self, car, x1, y1, x2, y2, T):
        """Move a car from x1, y1 to x2, y2, it will be ready at time T"""
        assert(car.x == x1 and car.y == y1)
        self.cars[(x1, y1)].remove(car)
        self.cars[(x2, y2)].add(car)
        self.car_ready_times[car] = T

    def nearby_cars(self, x, y, radius):
        cars = set()
        for xr in range(x - radius, x + radius + 1):
            for yr in range(y - radius, y + radius + 1):
                cars.update(self.cars(xr, yr))
        return cars

    def free_cars(self):
        return set([c for c, t in self.car_ready_times.items() if t <= self.t])
