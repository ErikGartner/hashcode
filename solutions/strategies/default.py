from sortedcontainers import *
import collections
import algorithms

from ..utils import parse_in, write_ans, dprint, progressbar, timethis
from .utils import *


def solve(data, seed, debug):
    C, T, S, comps, children, targets

    servers = Servers(S)
    targets = set(targets)

    most_used_deps = SortedSet(
        comps.values(), key=lambda c: len(children[c]), reversed=True
    )

    T = -1
    while len(most_used_deps) > 0:
        T += 1

        if len(servers.free) == 0:
            self.next_t()
            continue

        while (len(servers.free)) > 0:
            s = next(servers.free)

            dep = None
            for t in targets:
                if t.file.rec_deps in servers.compiled_all:
                    dep = t
                    break

            if dep is None:
                dep = most_used_deps.pop(0)

            if dep is None:
                break

            servers.compile(dep, s)

    # Write answer
    return servers.compile_orders
