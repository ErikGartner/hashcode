from collections import Counter


def tag_info(photos):
    tag_counter = Counter()
    tag_list = [tag_counter.update(photo.tags) for photo in photos]
    return tag_counter

def tag_groups(photos):
    groups = {}
    for photo in photos:
        for tag in photo.tags:
            if tag not in groups:
                groups[tag] = set([photo.id])
            else:
                groups[tag].add(photo.id)
    return tag_groups
