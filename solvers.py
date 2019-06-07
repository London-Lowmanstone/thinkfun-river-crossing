'''Solvers for River Crossing Puzzles'''

import random
from copy import deepcopy
from typing import List
from node_solvers import BFSSolver as GeneralBFSSolver
from framework import Board, Move, Iterable

class RandomSolver:
    '''Solves a puzzle by randomly trying moves'''
    def __init__(self, board: Board):
        self.board = board
        self._moves: List[Move] = []

    def solve(self) -> List[Move]:
        '''Solves the puzzle'''
        self._moves = []
        while not self.board.solved():
            self.make_random_move()

        return self._moves

    def make_random_move(self) -> None:
        '''Makes a random move on the board'''
        possible_moves = self.board.get_moves()
        move = random.choice(possible_moves)
        self._moves.append(move)
        self.board.make_move(move)


class BFSSolver(GeneralBFSSolver[Board, Board, Move]): # pylint: disable=too-few-public-methods
    '''BFSSolver for River Crossing'''
    def __init__(self) -> None:
        '''Defines the correct functions to use the general BFS solver, and sets it up'''
        def namer(board: Board) -> Board:
            # upgrade: this is expensive
            return deepcopy(board)

        def detector(board: Board) -> bool:
            return board.solved()

        def expander(board: Board) -> Iterable[Move]:
            return board.get_moves()

        def follower(board: Board, move: Move) -> Board:
            new_board = deepcopy(board)
            new_board.make_move(move)
            return new_board

        super().__init__(namer, detector, expander, follower)


class PlankBFSSolver(GeneralBFSSolver[Board, Board, Move]): # pylint: disable=too-few-public-methods
    '''
    Solver for making sure the planks are in the correct position -
    ...does not care about position of person.
    '''
    def __init__(self, target_board: Board):
        self.target_board = target_board
        def namer(board: Board) -> Board:
            # upgrade: this is expensive
            return deepcopy(board)

        def detector(board: Board) -> bool:
            return set(board.planks) == set(self.target_board.planks)

        def expander(board: Board) -> Iterable[Move]:
            return board.get_moves()

        def follower(board: Board, move: Move) -> Board:
            new_board = deepcopy(board)
            new_board.make_move(move)
            return new_board

        super().__init__(namer, detector, expander, follower)
