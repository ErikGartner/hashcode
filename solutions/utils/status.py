from tqdm import tqdm
from takethetime import ttt

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
    if DEBUG:
        return ttt(name=name)
    else:
        class controlled_execution:
            def __enter__(self):
                pass
            def __exit__(self, type, value, traceback):
                pass
        return controlled_execution()
