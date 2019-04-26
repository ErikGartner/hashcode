import datetime
import sortedcontainers
import collections
import numpy as np

Project = collections.namedtuple('Project', 'id t h w ur plan used')


def parse_in(in_file):
    with open(in_file, 'r') as f:
        H, W, D, B = [int(c) for c in f.readline().split()]

        projects = []
        for b in range(B):
            t, h, w, ur = f.readline().split()
            h, w, ur = int(h), int(w), int(ur)
            plan = np.full((h, w), -1, dtype=np.int8)
            used = []
            for h_idx in range(h):
                row = f.readline()
                for r_idx, c in enumerate(row):
                    if c == '#':
                        plan[h_idx, r_idx] = b
                        used.append((h_idx, r_idx))
            project = Project(b, t, h, w, ur, plan, used)
            projects.append(project)
    return H, W, D, B, projects


def parse_ans(ans_file):
    with open(ans_file, 'r') as f:
        pass


def write_ans(in_file, start_time, strategy, answer):
    """
    Takes an in_file and generates an appropriate outfile.
    Return the path to outfile.
    """

    problem_name = in_file.split('/')[-1].replace('.in', '')
    outfile = 'out/{}_{}_{}.ans'.format(start_time, problem_name, strategy)

    print('Writing {} -> {}'.format(in_file, outfile))
    with open(outfile, 'w') as f:
        pass
