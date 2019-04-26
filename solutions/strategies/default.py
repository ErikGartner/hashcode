import sortedcontainers
import collections
import algorithms

from ..utils import parse_in, write_ans, dprint, progressbar, timethis
from .utils import *


TILE_MAX_H = 100
TILE_MAX_W = 100


def solve(data, seed, debug):
    H, W, D, B, projects = data

    max_h = max(projects, key=lambda p: p.h).h
    max_w = max(projects, key=lambda p: p.w).w

    tile, score, plans = create_tile(
        H, W, D, max_h, max_w, projects, TILE_MAX_H, TILE_MAX_W
    )

    print(tile)
