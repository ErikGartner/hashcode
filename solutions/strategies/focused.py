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

        finished_targets = set([])
        # Target with closest deadline
        for target in targets:

            if len(servers.free) == 0:
                break

            # Compile target if we can
            if compile_best_server(target.file, servers):
                finished_targets.add(target)
                continue

        # Remove finished targets
        targets = targets - finished_targets

        # Work on remaining targets dependencies
        for target in targets:

            if len(servers.free) == 0:
                break

            # Compile dependencies
            uncompiled_deps = target.file.rec_deps - servers.compiling

            # TODO: Sort by replication time??
            for dep in uncompiled_deps:
                if len(servers.free) == 0:
                    break

                # Check individual servers?
                compile_best_server(dep, servers)

        if len(servers.free) > 0:
            print("Free servers: {}".format(len(servers.free)))

    # Write answer
    return servers.compile_orders


def compile_best_server(comp, servers):

    if comp.rec_deps.issubset(servers.compiled_all):
        # Random free server
        s = next(iter(servers.free))
        servers.compile(comp, s)
        return True

    elif comp.rec_deps.issubset(servers.compiled_any):
        for server, compiled_deps in servers.compiled.items():
            if server in servers.free and comp.rec_deps.issubset(
                servers.compiled[server]
            ):
                # Compile on free server
                servers.compile(comp, server)
        return True

    else:
        return False
