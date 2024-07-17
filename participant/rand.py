from participant.participant import *
from board import *

import random
from dataclasses import dataclass, field


@dataclass(init=True, frozen=True)
class Rand(Participant):
    board: Board = field(default_factory=Board)

    def make_move(self) -> Tuple['Rand', int]:
        moves: List[int] = [move for move in range(9) if self.board.is_valid_move(move)]
        move: int = random.choice(moves)
        board: Board = self.board.update(move)
        rand: Rand = Rand(board)
        return rand, move

    def update_move(self, move: int) -> 'Rand':
        board: Board = self.board.update(move)
        rand: Rand = Rand(board)
        return rand
