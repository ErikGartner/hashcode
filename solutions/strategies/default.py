import sortedcontainers
import collections
import algorithms

from ..utils import parse_in, write_ans, dprint, progressbar
from .utils import *
from solutions.score import score_pair


def solve(photos, seed, debug):

    tag_counter = tags_info(photos)
    dprint(tag_counter)
    dprint(len(tag_counter))
