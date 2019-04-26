import sortedcontainers
import collections
import algorithms

from ..utils import parse_in, write_ans, dprint, progressbar, timethis
from .utils import *

from ..scoring.scorer import score as score_fn


TILE_MAX_H = 100
TILE_MAX_W = 100


def solve(data, seed, debug):
    H, W, D, B, projects = data

    max_h = max(projects, key=lambda p: p.h).h
    max_w = max(projects, key=lambda p: p.w).w

    tile, score, plans = create_tile(
        H, W, D, max_h, max_w, projects, TILE_MAX_H, TILE_MAX_W
    )
    print("Tile:")
    print(tile)

    tile_h, tile_w = tile.shape

    # Apply tile to city map
    city_plans = []
    city_map = np.full((H, W), -1)
    for x in range(0, H - tile_h + 1, tile_h):
        for y in range(0, W - tile_w + 1, tile_w):
            city_map[x : x + tile_h, y : y + tile_w] = tile

            for p in plans:
                city_plans.append(Plan(p.id, p.x + x, p.y + y))

    print("Map:")
    print(city_map)
    print("Score: {}".format(score_fn(city_plans, projects, (H, W, D))))
    return city_plans
