from tqdm import tqdm
import time

DEBUG = False


def dprint(*msg, **kwargs):
    if not DEBUG:
        return
    else:
        print(*msg, **kwargs)


def progressbar(itr):
    if not DEBUG:
        return itr
    else:
        return tqdm(itr)


def timethis(name):
    """
    Usage:
    with timethis('Sorting loop') as t:
        do_func()
        t.info('Nbr items: %d' % len(stuff))
    """
    class timewrapper:
        def __init__(self, name, debug):
            self.name = name
            self.messages = []
            self.debug = debug

        def info(self, msg):
            self.messages.append(msg)

        def __enter__(self):
            self.t0 = time.time()
            return self

        def __exit__(self, type, value, traceback):
            if self.debug:
                print('{}: {:0.5f}s'.format(self.name, time.time() - self.t0))
                for msg in self.messages:
                    print('- {}'.format(msg))
    return timewrapper(name, DEBUG)
