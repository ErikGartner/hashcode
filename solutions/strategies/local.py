from sortedcontainers import *
import collections
import algorithms

from ..utils import parse_in, write_ans, dprint, progressbar, timethis
from .utils import *


def solve(data, seed, debug):
    C, T, S, comps, children, targets = data

    servers = Servers(S)

    most_used_deps = set(comps.values())
    all_target_deps = set()
    for target in targets:
        all_target_deps = all_target_deps.union(target.file.rec_deps)

    # Only care about things related to targets
    most_used_deps = most_used_deps.intersection(all_target_deps)
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

        # Compile to all dependencies
        most_used_deps = most_used_deps - servers.compiled_all
        while len(servers.free) > 0:
            compile_best_server(most_used_deps, servers)

        # Remove finished targets
        targets = targets - finished_targets

        # Work on remaining targets dependencies
        for target in targets:

            if len(servers.free) == 0:
                break

            # Compile dependencies, sort by longest compile time! Start compiling now!
            uncompiled_deps = sorted(
                target.file.rec_deps - servers.compiling,
                key=lambda x: x.c + x.r,
                reverse=True,
            )

            # TODO: Sort by replication time??
            for dep in uncompiled_deps:
                if len(servers.free) == 0:
                    break

                # Check individual servers?
                compile_best_server(dep, servers)

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
