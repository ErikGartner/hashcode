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

    while len(targets) > 0:
        dprint(len(targets))
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
                if t.file.rec_deps not in servers.compiled_all:
                    dep = t.file
                    targets.remove(t)
                    break

            if dep is not None:
                # Compiling target!
                servers.compile(dep, s)
                continue

            for t in targets:
                for d in t.file.rec_deps:
                    if d not in servers.compiling:
                        dep = d

            if dep is not None:
                # Look at compile target rec_deps
                servers.compile(dep, s)

    # Write answer
    return servers.compile_orders
