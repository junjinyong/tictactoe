from participant.participant import *


@dataclass(init=True, frozen=True)
class MonteCarloSearch(Participant):
    def make_move(self) -> Tuple['MonteCarloSearch', int]:
        return self, int(input('Your move: '))

    def update_move(self, move: int) -> 'MonteCarloSearch':
        return self
