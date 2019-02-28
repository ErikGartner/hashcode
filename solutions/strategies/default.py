import time

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
    all_nbr_tags = sortedcontainers.SortedSet([p.id for p in photos],
                                               key=lambda x: len(photos[x].tags))

    used_photos = set()
    tag_counter = tag_info(photos)
    tag_dict = tag_groups(photos)

    def remove_photo(p):
        if p.id in hor_nbr_tags:
            hor_nbr_tags.remove(p.id)
        if p.id in ver_nbr_tags:
            ver_nbr_tags.remove(p.id)
        if p.id in all_nbr_tags:
            all_nbr_tags.remove(p.id)
        used_photos.add(p.id)
        for tag in p.tags:
            tag_counter[tag] -= 1
            tag_dict[tag].remove(p.id)

    p1 = photos[all_nbr_tags.pop(-1)]
    ids = [p1.id]
    remove_photo(p1)
    if not p1.horizontal:
        p2 = photos[ver_nbr_tags.pop(-1)]
        ids.append(p2.id)
        remove_photo(p2)

    slides = [
        # Set first slide as a horizontal with many tags
        Slide(ids=ids)
    ]

    # Until all photos are used
    while len(used_photos) < len(photos):
        print('Progress', len(used_photos), len(photos))

        # previous photo
        tags1 = set()
        [tags1.update(photos[i].tags) for i in slides[-1].ids]

        # Find photos with related tags
        related_photos = collections.Counter()

        stop_tags = set([x[0] for x in tag_counter.most_common(3)])

        t0 = time.time()
        for tag, count in tag_counter.most_common():
            if tag in tags1 and tag not in stop_tags:
                related_photos.update(tag_dict[tag])
            if sum(related_photos.values()) > 500:
                break

        c2 = 0
        for tag, count in tag_counter.most_common()[-100:]:
            if tag in tags1 and tag not in stop_tags:
                related_photos.update(tag_dict[tag])
                c2 += count
            if c2 > 200:
                break
        dprint('Related photos', len(related_photos), time.time() - t0)

        # returns photo with most in common
        if len(related_photos.most_common()) == 0:
            # No in common
            p1 = photos[all_nbr_tags.pop(-1)]

        else:
            # Find a photo with good score
            t0 = time.time()
            possibilities = related_photos.most_common(100)
            scored_possibilities = [(x[0], score_pair(photos[x[0]].tags, tags1))
                                    for x in possibilities]
            scored_possibilities.sort(key=lambda x: x[1], reverse=True)

            p1 = photos[scored_possibilities[0][0]]
            dprint('Scoring photos: ', time.time() - t0)

        # p1 now contains the other photo
        remove_photo(p1)
        ids = [p1.id]

        if not p1.horizontal:
            if len(ver_nbr_tags) == 0:
                # No more veritcal photos
                # Skip these photos
                continue

            t0 = time.time()
            # Find optimal match for vertical
            # should tags not in p1
            related_photos = collections.Counter()
            max_score = -1
            best = None
            cmps = 0
            for i in reversed(ver_nbr_tags):
                tags_vert = p1.tags.union(photos[i].tags)
                if len(p1.tags) == len(tags_vert):
                    continue

                cmps += 1
                s = score_pair(tags1, p1.tags.union(photos[i].tags))
                if s > max_score:
                    best = i
                    max_score = s

                if cmps > 500:
                    break
            dprint('Finding vertical match: ', time.time() - t0)

            if best is None:
                p2 = photos[ver_nbr_tags.pop(-1)]
            else:
                p2 = photos[best]

            assert(p2 is not None)
            ids.append(p2.id)
            remove_photo(p2)

        slides.append(Slide(ids=ids))

    return slides
