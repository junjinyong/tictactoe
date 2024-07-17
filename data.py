from dataclasses import dataclass
from typing import Optional, Type, Union, TypeVar, List, Callable, assert_never


@dataclass
class Player:
    pass


@dataclass
class Opponent:
    pass


@dataclass
class Draw:
    pass


@dataclass
class Undetermined:
    pass


Turn = Union[Player, Opponent]
Cell = Union[Player, Opponent, Undetermined]
Outcome = Union[Player, Opponent, Draw, Undetermined]
Result = Union[Player, Opponent, Draw]

T: TypeVar = TypeVar('T')


def hand_over(turn: Type[Turn]) -> Type[Turn]:
    match turn:
        case _ if turn is Player:
            turn: Type[Turn] = Opponent
        case _ if turn is Opponent:
            turn: Type[Turn] = Player
        case _ as unreachable:
            assert_never(unreachable)
    return turn


def determine(outcome: Type[Outcome]) -> Optional[Type[Result]]:
    match outcome:
        case _ if issubclass(outcome, Result):
            return outcome
        case _ if outcome is Undetermined:
            return None
        case _ as unreachable:
            assert_never(unreachable)


def show(result: Type[Result]) -> None:
    match result:
        case _ if result is Player:
            print('Player won')
        case _ if result is Opponent:
            print('Opponent won')
        case _ if result is Draw:
            print('Draw')
        case _ as unreachable:
            assert_never(unreachable)


def get_reduce(turn: Type[Turn]) -> Callable[[List[float]], float]:
    match turn:
        case _ if turn is Player:
            return max
        case _ if turn is Opponent:
            return min
        case _ as unreachable:
            assert_never(unreachable)
