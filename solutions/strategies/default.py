import sortedcontainers
import collections
import algorithms

from ..utils import parse_in, write_ans, dprint, progressbar
from .utils import *
from solutions.score import score_pair

from ..utils.parser import Slide


def solve(photos, seed, debug):

    hor_nbr_tags = sortedcontainers.SortedSet([p.id for p in photos if p.horizontal],
                                               key=lambda x: len(photos[x].tags))
    ver_nbr_tags = sortedcontainers.SortedSet([p.id for p in photos if not p.horizontal],
                                               key=lambda x: len(photos[x].tags))

    used_photos = set()
    tag_counter = tag_info(photos)

    slides = [
        # Set first slide as a horizontal with many tags
        Slide([hor_nbr_tags.pop(0)])
    ]

    # Add to used photos
    used_photos.add(Slide.ids[0])

    # Until all photos are used
    while len(used_photos) < len(photos):














    return []
