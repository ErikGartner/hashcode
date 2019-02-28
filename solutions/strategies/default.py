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
    tag_dict = tag_groups(photos)

    slides = [
        # Set first slide as a horizontal with many tags
        Slide(ids=[hor_nbr_tags.pop(0)])
    ]

    # Add to used photos
    used_photos.add(slides[0].ids[0])

    # Until all photos are used
    while len(used_photos) < len(photos):

        # previous photo
        tags1 = set()
        [tags1.update(photos[i].tags) for i in slides[-1].ids]

        # Find photos with related tags
        related_photos = collections.Counter()
        for tag in tags1:
            dprint(tags1)
            related_photos.update(tag_dict[tag])

        dprint(related_photos)













    return []
