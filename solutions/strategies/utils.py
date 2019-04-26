import collections
import numpy as np

Plan = collections.namedtuple("Plan", "id x y")


def create_tile(H, W, D, h, w, projects, max_h=100, max_w=100):
    """DFS to generate an optimal tile"""

    # Tile size
    h = min(H, h * 2, max_h)
    w = min(W, w * 2, max_w)

    tile = np.full((h, w), -1, np.int8)
    x_coords, y_coords = np.where(tile == -1)
    free = frozenset(list(zip(x_coords, y_coords)))
    plans = []

    return _create_tile(tile, free, plans, projects, D, H, W)


def _create_tile(tile, free, plans, projects, D, H, W):
    best_score = 0
    best_tile = tile
    best_plans = plans

    leaf_tile = True

    for p in projects:
        for f in free:
            # We can build project p at corner x, y
            if _can_build(f[0], f[1], tile, p, H, W):
                leaf_tile = True

                new_free = free - set(f)
                new_tile = np.array(tile, copy=True)
                new_tile[f[0] : f[0] + p.h, f[1] : f[1] + p.w] = p.plan
                new_plans = plans + [Plan(p.id, f[0], f[1])]
                new_tile, score, new_plans = _create_tile(
                    new_tile, new_free, new_plans, projects, D, H, W
                )

                if score > best_score:
                    best_tile = new_tile
                    best_plans = new_plans
                    best_score = score

    if leaf_tile:
        # Cant build more. Score the tile
        best_score = score_plans(plans, projects, D)

    return best_tile, best_score, best_plans


def _can_build(x, y, tile, project, H, W):
    if x + project.h >= H or y + project.w >= W:
        return False

    area = tile[x : x + project.h, y : y + project.w] == -1

    if type(area) is bool:
        return area

    return area.all()


def score_plans(plans, projects, D):
    return 1
