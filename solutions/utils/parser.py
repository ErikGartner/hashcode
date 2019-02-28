import datetime
import sortedcontainers
import collections

Photo = collections.namedtuple('Photo', 'id horizontal tags')
Slide = collections.namedtuple('Slide', 'ids')


def parse_in(in_file):
    with open(in_file, 'r') as f:
        N = int(f.readline())
        photos = []
        for i in range(N):
            elems = f.readline().split()
            photo = Photo(id=i,
                          horizontal=elems[0] == 'H',
                          tags=set(elems[1:]))
            photos.append(photo)
    return photos


def parse_ans(ans_file):
    with open(ans_file, 'r') as f:
        S = int(f.readline())
        slides = []
        for s in range(S):
            ids = [int(i) for i in f.readline().split()]
            slide = Slide(ids)
            slides.append(slide)
    return slide


def write_ans(in_file, strategy, answer):
    """
    Takes an in_file and generates an appropriate outfile.
    Return the path to outfile.
    """
    problem_name = in_file.split('/')[-1].replace('.in', '')
    t = datetime.datetime.now().strftime("%H-%M-%S-%f")
    outfile = 'out/{}_{}_{}.ans'.format(problem_name, strategy, t)

    print('Writing {} -> {}'.format(in_file, outfile))
    with open(outfile, 'w') as f:
        pass
