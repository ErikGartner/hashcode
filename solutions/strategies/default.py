import sortedcontainers
import collections
import algorithms

from ..utils import parse_in, write_ans, dprint, progressbar
from .utils import *
from solutions.score import score_pair


def solve(photos, seed, debug):

    photos_by_nbr_tags = sortedcontainers.SortedSet([p.id for p in photos],
                                                    key=lambda x: len(photos[x].tags))
    used_photos = set()
    tag_counter = tag_info(photos)








    return []
