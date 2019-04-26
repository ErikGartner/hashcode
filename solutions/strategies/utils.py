import collections
import sortedcontainers
import numpy as np

from ..scoring.scorer import score_plans

Plan = collections.namedtuple("Plan", "id x y")

def n_best_residentials(projects, n=None):
    residentials = [project for project in projects if project.t == 'R']
    residentials = sorted(residentials, key=lambda x: x.ur/len(x.used), reverse=True)
    if n:
        return residentials[:n]
    return residentials

def create_tile(H, W, D, h, w, projects, max_h=100, max_w=100):
    """DFS to generate an optimal tile"""

    # Tile size
    h = min(H, h * 2, max_h)
    w = min(W, w * 2, max_w)

    tile = np.full((h, w), -1, np.int8)
    x_coords, y_coords = np.where(tile == -1)
    free = frozenset(list(zip(x_coords, y_coords)))
    plans = []

    return _complete_tile(tile, free, plans, projects, D, *tile.shape)


def _complete_tile(tile, free, plans, projects, D, H, W):

    for f in free:
        best_score = -1
        best_tile = tile
        best_plans = plans

        for p in projects:
            # We can build project p at corner x, y
            if _can_build(f[0], f[1], tile, p, H, W):
                new_tile = np.array(tile, copy=True)
                new_tile[f[0] : f[0] + p.h, f[1] : f[1] + p.w] = p.plan
                new_plans = plans + [Plan(p.id, f[0], f[1])]
                score = score_plans(new_plans, projects, D)

                if score > best_score:
                    best_tile = new_tile
                    best_plans = new_plans
                    best_score = score

        tile = best_tile
        plans = best_plans

    return best_tile, best_score, best_plans


def _can_build(x, y, tile, project, H, W):
    if x + project.h > H or y + project.w > W:
        return False

    area = tile[x : x + project.h, y : y + project.w] == -1

    if type(area) is bool:
        return area

    return area.all()
