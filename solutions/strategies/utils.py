import collections

order = collections.namedtuple("Order", "file server")


class Servers:
    def __init__(self, N):
        self.N = N
        self.free = set(list(range(N)))
        self.free_at = {n: 0 for n in range(N)}
        self.freed_at = defaultdict(lambda: set())
        self.compiled = {n: set() for n in range(N)}
        self.compiled_all = set()
        self.compile_q = defaultdict(lambda: set())
        self.T = 0
        self.compile_orders = []

    def compile(self, comp, server):
        assert server in self.free
        self.free.remove(server)
        done_t = self.T + comp.c
        self.free_at[server] = self.T + comp.c
        self.freed_at[self.T + comp.c].add(server)
        self.compile_q[self.T + comp.c] = (server, comp)
        self.compile_q[self.T + comp.c + comp.r] = (-1, comp)
        compile_orders.append(order(comp.name, server))

    def next_t(self):
        self.T = self.T + 1
        self.free = self.free.union(self.freed_at[self.T])
        compiled = self.compile_q[self.T]
        for c in compiled:
            if c[0] == -1:
                self.compiled_all.add(c[1])
            else:
                self.compiled[c[0]].add(c[1])
