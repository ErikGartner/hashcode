from sortedcontainers import *
import collections
import algorithms

from ..utils import parse_in, write_ans, dprint, progressbar, timethis
from .utils import *

""" Each target per machine. No repl"""


def solve(data, seed, debug):
    C, T, S, comps, children, targets = data

    servers = Servers(S)

    time = -1

    # Sort by remaining time
    targets = SortedSet(targets, key=lambda x: x.deadline)

    # target -> server
    server_mappings = collections.defaultdict(lambda: None)

    while len(targets) > 0:
        # Update clock
        time += 1
        servers.next_t()

        # Remove dead target
        removed = targets
        targets = remove_timed_out_targets(targets, time, comps)
        removed = removed - targets
        for r in removed:
            server_mappings[r] = None

        # Look at max S number of targets
        active_targets = targets[:S]
        finished_targets = set([])
        for target in active_targets:
            server = server_mappings[target]
            if server is None:
                # Accuire server
                free_servers = set(list(range(S))) - set(server_mappings.values())

                if len(free_servers) > 0:
                    # TODO: Server with most deps already.
                    server = next(iter(free_servers))
                    server_mappings[target] = server

                    print("Mapping {} to {}".format(target.file.name, server))
                else:
                    print("weird queueing issue.")

            if server not in servers.free:
                continue

            # Compile a dependency
            uncompiled_deps = sorted(
                target.file.rec_deps - servers.compiled[server], key=lambda x: x.c
            )
            if len(uncompiled_deps) > 0:
                dep = next(iter(uncompiled_deps))
                servers.compile(dep, server)
            else:
                servers.compile(target.file, server)
                finished_targets.add(target)
                server_mappings[target] = None

        targets = targets - finished_targets

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
