from collections import Counter


def tag_info(photos):
    tag_counter = Counter()
    tag_list = [tag_counter.update(photo.tags) for photo in photos]
    return tag_counter
