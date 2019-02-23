import glob
import os
import json

from .utils.parser import parse_ans
from .scoring import compute_score


def score_answers():
    """Scores all answers"""
    for ans_file in sorted(glob.glob(os.path.join('out', '*.ans'))):
        out_file = ans_file.replace('.ans', '.score')

        if os.path.isfile(out_file):
            # Already scored, skip file
            continue

        #ans = parse_ans(ans_file)
        problem_file = ans_file.rsplit('_', 2)[0].split('/')[1] + '.in'
        problem_path = os.path.realpath('data/' + problem_file)
        ans_path = os.path.realpath(ans_file)
        score = compute_score(problem_path, ans_file).total()
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
