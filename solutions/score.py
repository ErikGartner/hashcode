import glob
import os

from .utils.parser import parse_ans


def score_answers():

    for ans_file in sorted(glob.glob(os.path.join('out', '*.ans'))):
        out_file = ans_file.replace('.ans', '.score')

        if os.path.isfile(out_file):
            # Already scored, skip file
            continue

        print('Scoring {} -> {}'.format(ans_file, out_file))
        ans = parse_ans(ans_file)

        score = do_scoring(ans)

        with open(out_file, 'w') as f:
            f.write('{}'.format(score))


def do_scoring(ans):
    return 0
