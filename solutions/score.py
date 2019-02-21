import glob
import os
import json

from .utils.parser import parse_ans


def do_scoring(ans):
    """Implement me to do actual scoring from answer"""
    return 0


def score_answers():
    """Scores all answers"""
    for ans_file in sorted(glob.glob(os.path.join('out', '*.ans'))):
        out_file = ans_file.replace('.ans', '.score')

        if os.path.isfile(out_file):
            # Already scored, skip file
            continue

        ans = parse_ans(ans_file)
        score = do_scoring(ans)
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
