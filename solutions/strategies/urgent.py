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
    targets = SortedSet(targets, key=lambda x: x.deadline)

    while len(targets) > 0:
        # Update clock
        time += 1
        servers.next_t()

        # Remove dead target
        targets = remove_timed_out_targets(targets, time, comps)

        while (len(servers.free)) > 0:
            s = next(iter(servers.free))

            dep = None
            for t in targets:
                if t.file.rec_deps.issubset(servers.compiled_all):
                    dep = t.file
                    targets.remove(t)
                    break

            if dep is not None:
                # Compiling target!
                servers.compile(dep, s)
                continue

            for t in targets:
                for d in t.file.rec_deps:
                    if d not in servers.compiling and d.rec_deps.issubset(
                        servers.compiled_all
                    ):
                        dep = d

            if dep is not None:
                # Look at compile target rec_deps
                servers.compile(dep, s)
                continue

            if dep is None:
                # Can't compile anythin right now, next time step.
                break

    # Write answer
    return servers.compile_orders
