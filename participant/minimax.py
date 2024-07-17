import random
from participant.participant import *
from board import *
from typing import List, Dict, Callable, ClassVar
from dataclasses import dataclass, field
from functools import partial, cache


@dataclass(init=True, frozen=True)
class MinimaxHeuristic(Participant):
    board: Board = field(default_factory=Board)
    depth_limit: int = 2

    def make_move(self) -> Tuple['MinimaxHeuristic', int]:
        def helper2(b: Board, depth: int) -> float:
            outcome, score = b.get()
            if depth == 0:
                return score
            match outcome:
                case _ if issubclass(outcome, Result):
                    return score
                case _ if outcome is Undetermined:
                    turn: Type[Turn] = b.get_turn()
                    f: Callable[[List[float]], float] = get_reduce(turn)
                    scores: List[float] = b.map_children(partial(helper2, depth=depth - 1))
                    score: float = f(scores)
                    return score
                case _ as unreachable:
                    assert_never(unreachable)

        def helper1(b: Board) -> int:
            turn: Type[Turn] = b.get_turn()
            match turn:
                case _ if turn is Player:
                    f: Callable[[Callable[['Board'], float]], int] = b.argmax_children
                case _ if turn is Opponent:
                    f: Callable[[Callable[['Board'], float]], int] = b.argmin_children
                case _ as unreachable:
                    assert_never(unreachable)
            return f(partial(helper2, depth=self.depth_limit - 1))

        move: int = helper1(self.board)
        board: Board = self.board.update(move)
        minimax: MinimaxHeuristic = MinimaxHeuristic(board)
        return minimax, move

    def update_move(self, move: int) -> 'MinimaxHeuristic':
        board: Board = self.board.update(move)
        minimax: MinimaxHeuristic = MinimaxHeuristic(board)
        return minimax


@dataclass(init=True, frozen=True)
class MinimaxExhaustive(Participant):
    board: Board = field(default_factory=Board)

    @classmethod
    @cache
    def helper2(cls, b: Board) -> float:
        oc, score = b.get()
        match oc:
            case _ if issubclass(oc, Result):
                return score
            case _ if oc is Undetermined:
                scores: List[float] = b.map_children(cls.helper2)
                turn: Type[Turn] = b.get_turn()
                f: Callable[[List[float]], float] = get_reduce(turn)
                score: float = f(scores)
                return score
            case _ as unreachable:
                assert_never(unreachable)

    def helper1(self, b: Board) -> int:
        turn: Type[Turn] = b.get_turn()
        match turn:
            case _ if turn is Player:
                f: Callable[[Callable[['Board'], float]], int] = b.argmax_children
            case _ if turn is Opponent:
                f: Callable[[Callable[['Board'], float]], int] = b.argmin_children
            case _ as unreachable:
                assert_never(unreachable)
        return f(self.helper2)

    def make_move(self) -> Tuple['MinimaxExhaustive', int]:
        move: int = self.helper1(self.board)
        board: Board = self.board.update(move)
        minimax: MinimaxExhaustive = MinimaxExhaustive(board)
        return minimax, move

    def update_move(self, move: int) -> 'MinimaxExhaustive':
        board: Board = self.board.update(move)
        minimax: MinimaxExhaustive = MinimaxExhaustive(board)
        return minimax
