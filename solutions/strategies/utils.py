import collections
import sortedcontainers
import numpy as np

from ..utils.status import *
from ..utils.status import progressbar
from ..scoring.scorer import score_plans

Plan = collections.namedtuple("Plan", "id x y")


def n_best_residentials(projects, n=None):
    residentials = [project for project in projects if project.t == "R"]
    residentials = sorted(residentials, key=lambda x: x.ur, reverse=True)
    if n:
        return residentials[:n]
    return residentials


def create_tile(H, W, D, h, w, projects, max_h=100, max_w=100):
    """DFS to generate an optimal tile"""

    # Tile size
    h = min(H, h * 2, max_h)
    w = min(W, w * 2, max_w)

    # Generate starting tiles
    start_res = n_best_residentials(projects, n=1)

    best_score = -1
    best_tile = None
    best_plans = []
    for res in start_res:
        tile = np.full((h, w), -1, np.int8)
        x_coords, y_coords = np.where(tile == -1)
        free = frozenset(list(zip(x_coords, y_coords)))

        x = 0
        y = 0

        plans = [Plan(res.id, x, y)]

        tile, free, neighbours = build_project(tile, plans[-1], projects,
                                               set([]), free, D)

        tile, score, plans = _complete_tile(tile, free, neighbours, plans, projects, D, *tile.shape)

        if score > best_score:
            best_tile = tile
            best_plans = plans
            best_score = score

    total_score = best_score * (H // h) * (W // w)
    print('Total score: %d' % total_score)
    return best_tile, best_score, best_plans



def _complete_tile(tile, free, neighbours, plans, projects, D, H, W, max_tries=1000):
    # fyll första neighbour innan andra osv
    print("_complete_tile")
    sorted_utils = sorted([p for p in projects if p.t == 'U'], key=lambda x: len(x.used))
    used_types = set([])
    util_projects = []
    for project in sorted_utils:
        if project.ur not in used_types:
            util_projects.append(project)

    sorted_res = sorted([p for p in projects if p.t == 'R'], key=lambda x: x.ur, reverse=True)
    sorted_projects = util_projects + sorted_res[:25]

    while len(neighbours) > 0:
        dprint("Neighbours: {}, free: {}/{}".format(len(neighbours), len(free), H * W))
        best_score = 0
        best_plans = plans
        leaf = True
        tries = 0
        for n in neighbours:
            for p in sorted_projects:
                tries += 1
                if _can_build(n[0], n[1], tile, p, H, W):
                    plan = Plan(p.id, n[0], n[1])

                    # tile, free, neighbours = build_project(tile, plan, projects,
                    #                                        neighbours, free, D)


                    score = score_plans(plans + [plan], projects, D)
                    # print(tile)
                    # print(plans + [plan])
                    # print(score)
                    # exit(0)
                    if score > best_score:
                        best_score = score
                        best_plans = plans + [plan]
                        leaf = False
            if tries > max_tries:
                break

        if leaf:
            break
            # expand neighbours

        tile, free, neighbours = build_project(tile, best_plans[-1], projects,
                                               neighbours, free, D)
        plans = best_plans
    score = score_plans(best_plans, projects, D)
    print(score)
    return tile, score, best_plans

def build_project(tile, plan, projects, neighbours, free, D):
    p = projects[plan.id]
    tile[plan.x: plan.x + p.h, plan.y: plan.y + p.w] = p.plan
    used = set([(dx + plan.x, dy + plan.y) for dx, dy in p.used])
    new_free = free - used
    new_neighbours = nearby_slots(new_free, plan, projects, D)
    neighbours = neighbours.union(new_neighbours) - used
    return tile, new_free, neighbours


def _can_build(x, y, tile, project, H, W):
    if x + project.h > H or y + project.w > W:
        return False

    area = tile[x : x + project.h, y : y + project.w] == -1

    if type(area) is bool:
        return area

    return area.all()


def nearby_slots(free, plan, projects, D):
    coords = set([])
    for x in range(plan.x - D, plan.x + projects[plan.id].h + D):
        for y in range(plan.y - D, plan.y + projects[plan.id].w + D):
            coords.add((x, y))
    return free.intersection(coords)
