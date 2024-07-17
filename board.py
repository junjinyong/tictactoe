from data import *
from typing import List, Dict, Tuple, Callable, Iterator
from dataclasses import dataclass, field
from math import tanh
from itertools import accumulate


lookup: List[Tuple[int, int, int]] = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                                      (0, 3, 6), (1, 4, 7), (2, 5, 8),
                                      (0, 4, 8), (2, 4, 6)]


@dataclass(init=True, frozen=True)
class Board:
    board: List[Type[Cell]] = field(default_factory=lambda: [Undetermined for _ in range(9)])
    turn: Type[Turn] = Player
    outcome: Type[Outcome] = Undetermined
    score: float = 0.0

    def __post_init__(self):
        outcome, score = self.evaluate()
        object.__setattr__(self, 'outcome', outcome)
        object.__setattr__(self, 'score', score)

    def update(self, move: int) -> 'Board':
        board: List[Type[Cell]] = [cell if i != move else self.turn for i, cell in enumerate(self.board)]
        turn: Type[Turn] = hand_over(self.turn)
        return Board(board=board, turn=turn)

    def map_children(self, f: Callable[['Board'], T]) -> List[T]:
        children: List[Board] = [self.update(move) for move in range(9) if self.board[move] == Undetermined]
        result: List[T] = [f(child) for child in children]
        return result

    def argmax_children(self, ev: Callable[['Board'], float]) -> int:
        lookup_: List[int] = [move for move in range(9) if self.board[move] == Undetermined]
        children: List[Board] = [self.update(move) for move in range(9) if self.board[move] == Undetermined]
        f: Callable[[int], float] = lambda move: ev(children[move])
        index: int = max(range(len(children)), key=f)
        return lookup_[index]

    def argmin_children(self, ev: Callable[['Board'], float]) -> int:
        lookup_: List[int] = [move for move in range(9) if self.board[move] == Undetermined]
        children: List[Board] = [self.update(move) for move in range(9) if self.board[move] == Undetermined]
        f: Callable[[int], float] = lambda move: ev(children[move])
        index: int = min(range(len(children)), key=f)
        return lookup_[index]

    def collect_first_children(self, f: Callable[['Board'], float], cond: Callable[[float], bool]) -> Optional[float]:
        children: List[Board] = [self.update(move) for move in range(9) if self.board[move] == Undetermined]
        gen_expr: Iterator[float] = (result for child in children if cond(result := f(child)))
        return next(gen_expr, None)

    def accumulate_children(self, f: Callable[['Board', T], T], reduce: Callable[[T, T], T], init: T) -> Iterator[T]:
        children: Iterator[Board] = (self.update(move) for move in range(9) if self.board[move] == Undetermined)
        function: Callable[[T, Board], T] = lambda alpha_, child: reduce(alpha_, f(child, alpha_))
        x: Iterator[T] = accumulate(iterable=children, func=function, initial=init)
        return x

    def is_valid_move(self, move: int) -> bool:
        return 0 <= move < 9 and self.board[move] == Undetermined

    def get_turn(self) -> Type[Turn]:
        return self.turn

    def get_outcome(self) -> Type[Outcome]:
        return self.outcome

    def get(self) -> Tuple[Type[Outcome], float]:
        return self.outcome, self.score

    def __str__(self) -> str:
        lookup_: Dict[Type[Cell], str] = {Player: 'Ｏ', Opponent: 'Ｘ', Undetermined: '　'}
        f: List[str] = [lookup_[cell] for cell in self.board]
        result: List[str] = ['　０１２\n０'] + f[0:3] + ['\n１'] + f[3:6] + ['\n２'] + f[6:9] + ['\n']
        return ''.join(result)

    def __eq__(self, other: 'Board') -> bool:
        if isinstance(other, Board):
            return self.turn == other.turn and self.board == other.board
        return False

    def __hash__(self) -> int:
        return hash((tuple(self.board), self.turn))

    def evaluate(self) -> Tuple[Type[Outcome], float]:
        result: List[List[Type[Cell]]] = [[self.board[i] for i in combo] for combo in lookup]

        def helper1(collection: List[List[Type[Cell]]], target: Type[Cell]) -> bool:
            return any(all(element == target for element in combo) for combo in collection)

        if helper1(result, Player):
            return Player, 1.0
        elif helper1(result, Opponent):
            return Opponent, -1.0
        elif all(cell != Undetermined for cell in self.board):
            return Draw, 0.0
        else:
            # custom evaluation function
            def helper2(collection: List[List[Type[Cell]]], target: Type[Cell]) -> int:
                return [all(element != target for element in combo) for combo in collection].count(True)

            player: int = helper2(result, Opponent)
            opponent: int = helper2(result, Player)
            estimate: float = tanh(player - opponent)
            return Undetermined, estimate
