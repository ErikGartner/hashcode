from collections import defaultdict


def dist(a, b, x, y):
    return abs(a - x) + abs(b - y)


def filter_requests(requests, t):
    return [r for r in requests if t <= r.f]


class Map():

    def __init__(self):
        self.data = defaultdict(lambda: set())
        self.t = 0
        self.car_ready_times = {}

    def add_car(self, car):
        self.data[(0, 0)].add(car)
        self.car_ready_times[car] = 0

    def cars(self, x, y):
        return [c for c in self.data[(x, y)] if self.car_ready_times[c] <= self.t]

    def move(self, car, x1, y1, x2, y2, T):
        """Move a car from x1, y1 to x2, y2, it will be ready at time T"""
        assert(car.x == x1 and car.y == y1)
        self.data[(x1, y1)].remove(car)
        self.data[(x2, y2)].add(car)
        self.car_ready_times[car] = T

    def nearby_cars(self, x, y, radius):
        cars = set()
        for xr in range(x - radius, x + radius + 1):
            for yr in range(y - radius, y + radius + 1):
                cars.update(self.cars(xr, yr))
        return cars
