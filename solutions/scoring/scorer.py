import numpy as np
from scipy.spatial import distance


def score(planned_projects, projects, map_info):
    print("Generating pid to project map..")

    H, W, D = map_info
    city_map = np.full((H, W), -1)

    project_id = {project.id: project for project in projects}
    planned_dicts = occupied_blocks(planned_projects, project_id)

    print("Checking legality of map..")
    for building in planned_dicts:
        if is_legal_plan(city_map, building):
            city_map[building["used_h"], building["used_w"]] = building["id"]
        else:
            return -1

    print("Calculating score..")
    return score_plans(planned_projects, projects, D)


def occupied_blocks(planned_projects, project_id):
    planned_dicts = []
    for building in planned_projects:
        h = []
        w = []
        for coord in project_id[building.id].used:
            h.append(building.x + coord[0])
            w.append(building.y + coord[1])
        planned_dicts.append({"id": building.id, "used_h": h, "used_w": w})
    return planned_dicts


def is_legal_plan(city_map, building):
    h_ok = (min(building["used_h"]) >= 0) and (
        max(building["used_h"]) < city_map.shape[0]
    )
    w_ok = (min(building["used_w"]) >= 0) and (
        max(building["used_w"]) < city_map.shape[1]
    )
    positions_free = (city_map[building["used_h"], building["used_w"]] == -1).all()
    return h_ok and w_ok and positions_free


def is_within_reach(residential_coords, utility_coords, D):
    Y = distance.cdist(residential_coords, utility_coords, "cityblock")
    return Y < D


def score_plans(planned_projects, projects, D):
    project_id = {project.id: project for project in projects}
    planned_dicts = occupied_blocks(planned_projects, project_id)
    planned_residentials = [
        project for project in planned_dicts if project_id[project["id"]].t == "R"
    ]
    planned_utilities = [
        project for project in planned_dicts if project_id[project["id"]].t == "U"
    ]

    utility_coords = []
    utility_type = []
    for utility in planned_utilities:
        coords = np.array(list(zip(utility["used_w"], utility["used_h"])))
        utility_coords.extend(coords)
        utility_type.extend([project_id[utility['id']].ur] * len(coords))

    utility_type = np.array(utility_type)
    score = 0
    if len(planned_utilities) > 0:
        for building in planned_residentials:
            building_coords = np.array(
                list(zip(building["used_w"], building["used_h"]))
            )
            utilities_reached = is_within_reach(building_coords, utility_coords, D)
            utilities_reached = np.sum(utilities_reached, axis=0) >= 1
            utility_types_reached = utility_type[utilities_reached]
            types_reached = len(np.unique(utility_types_reached))
            score += types_reached * project_id[building["id"]].ur
    return score
