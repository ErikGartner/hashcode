from tqdm import tqdm

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
