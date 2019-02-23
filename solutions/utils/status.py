from tqdm import tqdm

DEBUG = False


def dprint(*msg, **kwargs):
    if not DEBUG:
        return
    else:
        print(*msg, **kwargs)


def progressbar(itr):
    return tqdm(itr)
