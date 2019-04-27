import datetime
import sortedcontainers
import collections
from queue import Queue


Compilation = collections.namedtuple("Compilation", "name c r deps rec_deps")
Target = collections.namedtuple("Target", "file deadline goal")


def parse_in(in_file):
    with open(in_file, "r") as f:
        C, T, S = [int(l) for l in f.readline().split()]
        comps = {}
        for c in range(C):
            cols = f.readline().split()
            deps = [comps[x] for x in f.readline().split()[1:]]
            deps = frozenset(deps)

            q = Queue()
            [q.put(d) for d in deps]
            rec_deps = []
            while not q.empty():
                dep = q.get()
                rec_deps.append(dep)
                for d in dep.deps:
                    q.put(d)

            rec_deps = frozenset(rec_deps)
            comp = Compilation(cols[0], int(cols[1]), int(cols[2]), deps, rec_deps)
            comps[comp.name] = comp

    children = collections.defaultdict(lambda: set())
    for comp in comps.values():
        for dep in comp.rec_deps:
            children[dep].add(comp)

    return C, T, S, comps, children


def parse_ans(ans_file):
    with open(ans_file, "r") as f:
        pass


def write_ans(in_file, start_time, strategy, answer):
    """
    Takes an in_file and generates an appropriate outfile.
    Return the path to outfile.
    """

    problem_name = in_file.split("/")[-1].replace(".in", "")
    outfile = "out/{}_{}_{}.ans".format(start_time, problem_name, strategy)

    print("Writing {} -> {}".format(in_file, outfile))
    with open(outfile, "w") as f:
        f.write(len(answer) + "\n")
        for file in answer:
            f.write(step.name + " " + step.server + "\n")
