from sortedcontainers import *
import collections
import algorithms

from ..utils import parse_in, write_ans, dprint, progressbar, timethis
from .utils import *


def solve(data, seed, debug):
    C, T, S, comps, children, targets = data

    servers = Servers(S)
    most_used_deps = SortedSet(comps.values(), key=lambda c: -1 * len(children[c]))

    time = -1

    # Sort by remaining time
    targets = SortedSet(targets, key=lambda x: x.deadline - time)

    while len(most_used_deps) > 0:
        # Update clock
        time += 1
        servers.next_t()

        targets = remove_timed_out_targets(targets, time, comps)

        # Resort targets
        targets.update()

        while (len(servers.free)) > 0:
            s = next(iter(servers.free))

            dep = None
            for t in targets:
                if t.file.rec_deps in servers.compiled_all:
                    dep = t
                    target.remove(t)
                    break

            if dep is None:
                dep = most_used_deps.pop(0)

            if dep is None:
                break

            servers.compile(dep, s)

    # Write answer
    return servers.compile_orders
