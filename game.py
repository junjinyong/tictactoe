from participant.participant import *
from board import *


def game(player: Type[Participant], opponent: Type[Participant], silent: bool = False) -> Type[Result]:
    def turn(to_move: Participant, not_to_move: Participant, b: Board) -> Type[Result]:
        if not silent:
            print(b)
        outcome: Type[Outcome] = b.get_outcome()
        result: Optional[Type[Result]] = determine(outcome)
        if result:
            return result
        to_move, move = to_move.make_move()
        if not b.is_valid_move(move):
            return hand_over(b.get_turn())
        not_to_move = not_to_move.update_move(move)
        return turn(not_to_move, to_move, b.update(move))

    return turn(player(), opponent(), Board())
