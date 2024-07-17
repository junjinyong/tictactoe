import random
from functools import partial, cache
from itertools import takewhile

import cachetools.keys
from more_itertools import takewhile_inclusive
from typing import List, Dict, Callable, ClassVar
from dataclasses import dataclass, field
from cachetools import cached

import board
from participant.participant import *
from board import *


@dataclass(init=True, frozen=True)
class AlphaBetaHeuristic(Participant):
    board: Board = field(default_factory=Board)
    depth_limit: int = 2

    def make_move(self) -> Tuple['AlphaBetaHeuristic', int]:
        def helper(b: Board, depth: int, alpha: float, beta: float) -> float:
            outcome, score = b.get()
            if depth == 0:
                return score

            tn: Type[Turn] = b.get_turn()
            match outcome:
                case _ if issubclass(outcome, Result):
                    return score
                case _ if outcome is Undetermined and tn is Player:
                    f: Callable[[Board, float], float] = lambda bd, al: helper(bd, depth - 1, al, beta)
                    gen: Iterator[float] = b.accumulate_children(f, max, alpha)
                    return list(takewhile_inclusive(lambda x: x <= beta, gen)).pop()
                case _ if outcome is Undetermined and tn is Opponent:
                    f: Callable[[Board, float], float] = lambda bd, be: helper(bd, depth - 1, alpha, be)
                    gen: Iterator[float] = b.accumulate_children(f, min, beta)
                    return list(takewhile_inclusive(lambda x: x >= alpha, gen)).pop()
                case _ as unreachable:
                    assert_never(unreachable)

        turn: Type[Turn] = self.board.get_turn()
        match turn:
            case _ if turn is Player:
                move: int = self.board.argmax_children(partial(helper, depth=self.depth_limit, alpha=float('-inf'), beta=float('inf')))
            case _ if turn is Opponent:
                move: int = self.board.argmin_children(partial(helper, depth=self.depth_limit, alpha=float('-inf'), beta=float('inf')))
            case _ as unreachable:
                assert_never(unreachable)
        board: Board = self.board.update(move)
        alphabeta: AlphaBetaHeuristic = AlphaBetaHeuristic(board)
        return alphabeta, move

    def update_move(self, move: int) -> 'AlphaBetaHeuristic':
        board: Board = self.board.update(move)
        alphabeta: AlphaBetaHeuristic = AlphaBetaHeuristic(board)
        return alphabeta


@dataclass(init=True, frozen=True)
class AlphaBetaExhaustive(Participant):
    board: Board = field(default_factory=Board)
    transposition_table: ClassVar[Dict[Board, float]] = dict()

    @classmethod
    @cached(cache={})
    def helper(cls, b: Board, alpha: float, beta: float) -> float:
        outcome, score = b.get()
        tn: Type[Turn] = b.get_turn()
        match outcome:
            case _ if issubclass(outcome, Result):
                return score
            case _ if outcome is Undetermined and tn is Player:
                f: Callable[[Board, float], float] = lambda bd, al: cls.helper(bd, al, beta)
                gen: Iterator[float] = b.accumulate_children(f, max, alpha)
                return list(takewhile_inclusive(lambda x: x <= beta, gen)).pop()
            case _ if outcome is Undetermined and tn is Opponent:
                f: Callable[[Board, float], float] = lambda bd, be: cls.helper(bd, alpha, be)
                gen: Iterator[float] = b.accumulate_children(f, min, beta)
                return list(takewhile_inclusive(lambda x: x >= alpha, gen)).pop()
            case _ as unreachable:
                assert_never(unreachable)

    def make_move(self) -> Tuple['AlphaBetaExhaustive', int]:
        turn: Type[Turn] = self.board.get_turn()
        match turn:
            case _ if turn is Player:
                move: int = self.board.argmax_children(lambda b: self.helper(b, float('-inf'), float('inf')))
            case _ if turn is Opponent:
                move: int = self.board.argmin_children(lambda b: self.helper(b, float('-inf'), float('inf')))
            case _ as unreachable:
                assert_never(unreachable)
        board: Board = self.board.update(move)
        alphabeta: AlphaBetaExhaustive = AlphaBetaExhaustive(board)
        return alphabeta, move

    def update_move(self, move: int) -> 'AlphaBetaExhaustive':
        board: Board = self.board.update(move)
        alphabeta: AlphaBetaExhaustive = AlphaBetaExhaustive(board)
        return alphabeta
