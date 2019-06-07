'''
River Crossing Puzzles
'''

from framework import Board, get_plank
from util import invert_dictionary

# translator from pegs to RC characters
EXPERT40_TRANSLATOR = invert_dictionary({'6': 1, '9':4,  'O':8,  'T':9,  'I':12, 'X':15, # pylint: disable=bad-whitespace
                                         'C':16, 'M':18, 'R':19, 'B':21, 'G':22, 'Q':24,
                                         'A':26, 'K':28, 'U':30, '2':32, '3':33, '4':34})
EXPERT40_SOLUTION = ('UX-IX GI-GQ GQ-4Q QR-34 34-3K AK-KM 3K-MR KM-CM MR-QR 4Q-GQ QR-BG ' +
                     'GQ-2G BG-BC BC-MR CM-KM MR-3K KM-KU 3K-23 23-BG 2G-GI IX-UX KU-KM ' +
                     'KM-MO MO-RT OT-QR RT-GQ QR-AB GI-AK GQ-KU BG-BC UX-C6')


# upgrade: use the `super` function
class SimplePuzzle(Board):
    '''A very simple puzzle for testing'''
    def __init__(self) -> None:
        super().__init__(1, 7, [1, 6, 7], [(1, 6), (6, 7)])

class EasyMovePuzzle(Board):
    '''
    Another very simple puzzle for testing.
    Requires plank movement.
    '''
    def __init__(self) -> None:
        super().__init__(1, 7, [1, 6, 7], [(1, 6)])

# upgrade: the puzzles from River Crossing have a lot of duplicate code setup
class Beginner1(Board):
    '''Puzzle from River Crossing'''
    def __init__(self) -> None:
        start, end = 32, 4
        pegs = [4, 14, 13, 23, 22, 32]
        planks = [(32, 22), (22, 23)]

        # make sure my plank pegs are in the correct order
        planks = [get_plank(*points) for points in planks]

        # checking input
        assert start in pegs
        assert end in pegs
        for peg1, peg2 in planks:
            assert peg1 in pegs
            assert peg2 in pegs

        super().__init__(start, end, pegs, planks)

class Intermediate13(Board):
    '''Puzzle from River Crossing'''
    def __init__(self) -> None:
        start, end = 27, 15
        pegs = [7, 9, 15, 13, 11, 17, 27, 19, 24, 23, 21]
        planks = [(27, 17), (23, 13), (24, 19)]

        # make sure my plank pegs are in the correct order
        planks = [get_plank(*points) for points in planks]

        # checking input
        assert start in pegs
        assert end in pegs
        for peg1, peg2 in planks:
            assert peg1 in pegs
            assert peg2 in pegs

        super().__init__(start, end, pegs, planks)

class Expert31(Board):
    '''Puzzle from River Crossing'''
    def __init__(self) -> None:
        start, end = 16, 20
        pegs = [16, 20, 18, 1, 4, 7, 8, 14, 22, 28, 29, 34, 31, 32]
        planks = [(31, 16), (28, 29), (4, 14), (7, 22)]

        # make sure my plank pegs are in the correct order
        planks = [get_plank(*points) for points in planks]

        # checking input
        assert start in pegs
        assert end in pegs
        for peg1, peg2 in planks:
            assert peg1 in pegs
            assert peg2 in pegs

        super().__init__(start, end, pegs, planks)

class Expert39(Board):
    '''Puzzle from River Crossing'''
    def __init__(self) -> None:
        start, end = 34, 3
        pegs = [3, 7, 9, 11, 12, 15, 18, 20, 21, 24, 26, 28, 34]
        planks = [(34, 24), (24, 9), (9, 7), (7, 12)]

        # make sure my plank pegs are in the correct order
        planks = [get_plank(*points) for points in planks]

        # checking input
        assert start in pegs
        assert end in pegs
        for peg1, peg2 in planks:
            assert peg1 in pegs
            assert peg2 in pegs

        super().__init__(start, end, pegs, planks)

class Expert40(Board):
    '''Puzzle from River Crossing'''
    def __init__(self) -> None:
        start, end = 30, 1
        pegs = [1, 4, 8, 9, 12, 15, 16, 18, 19, 21, 22, 24, 26, 28, 30, 32, 33, 34]
        planks = [(30, 15), (24, 19), (26, 28), (22, 12), (8, 9)]

        # make sure my plank pegs are in the correct order
        planks = [get_plank(*points) for points in planks]

        # checking input
        assert start in pegs
        assert end in pegs
        for peg1, peg2 in planks:
            assert peg1 in pegs
            assert peg2 in pegs

        super().__init__(start, end, pegs, planks)
