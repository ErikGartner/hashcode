# Hashcode
*Our template and solutions starting from 2019*

## Results

- **[2019](https://github.com/ErikGartner/hashcode/tree/2019):** *Our heaps don't lie*, 36th place out of ~6500 teams with 1,073,160 pts

## Strategy

1. Read problem statement
2. Add in-files to data. Make sure they end `.in`
3. Write `solutions/utils/parser.py`
    1. `parse_in()`. Should create fast data structures for the problem.
    2. `write_ans()`. Should create valid answer file.
4. Write a basic strategy in `solutions/strategies/default.py`
5. Submit first score to Google for verification
6. Implement
  - `parse_ans()` in `solutions/utils/parser.py` to parse answers
  - Scoring in `solutions/score.py` by implementing `do_scoring()`
  - Advanced strategies in `solutions/strategies/`

## Team
- [Erik Gärtner](https://gartner.io)
- [Johan Ahlkvist](https://github.com/johanahlqvist)
