'''Solvers for River Crossing Puzzles'''

import random
from copy import deepcopy
from node_solvers import BFSSolver as GeneralBFSSolver


class RandomSolver:
    '''Solves a puzzle by randomly trying moves'''
    def __init__(self, board):
        self.board = board
        self._moves = None

    def solve(self):
        '''Solves the puzzle'''
        self._moves = []
        while not self.board.solved():
            self.make_random_move()

        return self._moves

    def make_random_move(self):
        '''Makes a random move on the board'''
        possible_moves = self.board.get_moves()
        move = random.choice(possible_moves)
        self._moves.append(move)
        self.board.make_move(move)


class BFSSolver(GeneralBFSSolver): # pylint: disable=too-few-public-methods
    '''BFSSolver for River Crossing'''
    def __init__(self):
        '''Defines the correct functions to use the general BFS solver, and sets it up'''
        def namer(board):
            # upgrade: this is expensive
            return deepcopy(board)

        def detector(board):
            return board.solved()

        def expander(board):
            return board.get_moves()

        def follower(board, move):
            new_board = deepcopy(board)
            new_board.make_move(move)
            return new_board

        GeneralBFSSolver.__init__(self, namer, detector, expander, follower)



class PlankBFSSolver(GeneralBFSSolver): # pylint: disable=too-few-public-methods
    '''
    Solver for making sure the planks are in the correct position -
    ...does not care about position of person.
    '''
    def __init__(self, target_board):
        self.target_board = target_board
        def namer(board):
            # upgrade: this is expensive
            return deepcopy(board)

        def detector(board):
            return set(board.planks) == set(self.target_board.planks)

        def expander(board):
            return board.get_moves()

        def follower(board, move):
            new_board = deepcopy(board)
            new_board.make_move(move)
            return new_board

        GeneralBFSSolver.__init__(self, namer, detector, expander, follower)
