from sortedcontainers import *
import collections
import algorithms

from queue import Queue

from ..utils import parse_in, write_ans, dprint, progressbar, timethis
from .utils import *


def solve(data, seed, debug):
    C, T, S, comps, children, targets = data

    servers = Servers(S)

    time = -1

    # Sort by remaining time
    # targets = SortedSet(targets, key=lambda x: total_comp_time(x))
    targets = SortedSet(targets, key=lambda x: len(x.file.rec_deps))
    dep_queue = []
    alreay_queued = set()
    for t in targets[:1]:
        [dep_queue.append(d) for d in t.file.rec_deps if d not in alreay_queued]
        alreay_queued = alreay_queued.union(t.file.rec_deps)

    while len(targets) > 0:

        # Update clock
        time += 1
        servers.next_t()
        if time % 10000 == 0:
            print(time)

        # Remove dead target
        targets = remove_timed_out_targets(targets, time, comps)

        # Compile what targets we can
        finished_t = set([])
        for t in targets:
            if len(servers.free) == 0:
                break

            if t.file.rec_deps.issubset(servers.compiled_all):
                # Random free server
                s = next(iter(servers.free))
                servers.compile(t.file, s)
                finished_t.add(t)

        targets = targets - finished_t

        if len(finished_t) > 0 and len(targets) > 0:
            print("Finished", finished_t)
            # Just finished job, new deps
            t = targets[0]
            [dep_queue.append(d) for d in t.file.rec_deps if d not in alreay_queued]
            alreay_queued = alreay_queued.union(t.file.rec_deps)
            print("New queue!", dep_queue)

        # Use rest of free serves to compile deps
        while len(servers.free) > 0 and len(dep_queue) > 0:
            s = next(iter(servers.free))
            for dep in dep_queue:
                if compile_best_server(dep, servers):
                    dep_queue.remove(dep)
                    break

    # Write answer
    return servers.compile_orders


def compile_best_server(comp, servers):

    if comp.rec_deps.issubset(servers.compiled_all):
        # Random free server
        s = next(iter(servers.free))
        if comp not in servers.compiled[s]:
            servers.compile(comp, s)
            return True

    elif comp.rec_deps.issubset(servers.compiled_any):
        for server, compiled_deps in servers.compiled.items():
            if server in servers.free and comp.rec_deps.issubset(
                servers.compiled[server]
            ):
                # Compile on free server
                if comp not in servers.compiled[server]:
                    servers.compile(comp, server)
                    return True

    else:
        return False
