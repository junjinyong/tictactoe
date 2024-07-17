import fire

from game import *
from utils import *


def main(player: str = 'AlphaBetaExhaustive', opponent: str = 'MinimaxExhaustive') -> None:
    # player, opponent = opponent, player
    player_class: Type[Participant] = get_class_by_name(player)
    opponent_class: Type[Participant] = get_class_by_name(opponent)
    # show(game(player_class, opponent_class))
    # return
    result: List[Type[Result]] = [game(player_class, opponent_class, silent=True) for _ in range(100)]
    print(f'{player}: {result.count(Player)} times')
    print(f'{opponent}: {result.count(Opponent)} times')
    print(f'Draw: {result.count(Draw)} times')


if __name__ == '__main__':
    fire.Fire(main)
