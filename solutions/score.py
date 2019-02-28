import glob
import os
import json

from .utils.parser import parse_ans, parse_in


def score_pair(tags1, tags2):
    s1 = set(tags1)
    s2 = set(tags2)
    return min(len(s1-s2), len(s2-s1), len(s1.intersection(s2)))


def do_scoring(ans, photos):
    """Implement me to do actual scoring from answer"""

    def valid_slide(ps):
        if len(ps) == 1:
            return ps[0].horizontal
        elif len(ps) == 2:
            return not ps[0].horizontal and not ps[1].horizontal
        else:
            return False

    def get_tags(ps):
        tags = []
        for p in ps:
            tags.extend(p.tags)
        return tags

    def get_photos(photos, ids1, ids2):
        p1 = [photos[i] for i in ids1]
        p2 = [photos[i] for i in ids2]
        return p1, p2

    score = 0
    for i1 in range(len(ans) - 1):
        i2 = i1 + 1

        p1, p2 = get_photos(photos, ans[i1].ids, ans[i2].ids)

        if not valid_slide(p1) or not valid_slide(p2):
            print('Invalid slide (%s -> %s) %s -> %s' % (ans[i1].ids,
                                                         ans[i2].ids,
                                                         p1, p2))
            return 0
        tags1 = get_tags(p1)
        tags2 = get_tags(p2)

        s = score_pair(tags1, tags2)
        score += s
    return score


def score_answers():
    """Scores all answers"""
    for ans_file in sorted(glob.glob(os.path.join('out', '*.ans'))):
        out_file = ans_file.replace('.ans', '.score')

        if os.path.isfile(out_file):
            # Already scored, skip file
            continue

        ans = parse_ans(ans_file)
        infile = ans_file.replace('out', 'data')
        infile = infile.rsplit('_', 2)[0] + '.in'
        photos = parse_in(infile)
        score = do_scoring(ans, photos)
        print('Scoring {} -> {}: {}'.format(ans_file, out_file, score))

        with open(out_file, 'w') as f:
            f.write('{}'.format(score))

    update_highscore()


def update_highscore():
    """Goes over all scores and finds the best answers"""
    scores = {}
    for score_file in sorted(glob.glob(os.path.join('out', '*.score'))):
        problem = score_file.rsplit('_', 2)[0].split('/')[1]
        ans_file = score_file.replace('.score', '.ans')

        with open(score_file, 'r') as f:
            score = int(f.read())

        current = scores.get(problem, {'ans': '', 'score': -1})
        if current['score'] < score:
            scores[problem] = {'ans': ans_file, 'score': score}

    with open('out/highscores.json', 'w') as f:
        json.dump(scores, f, indent=2)
