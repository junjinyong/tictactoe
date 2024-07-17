from participant.participant import *


@dataclass(init=True, frozen=True)
class MonteCarloTreeSearch(Participant):
    def make_move(self) -> Tuple['MonteCarloTreeSearch', int]:
        return self, int(input('Your move: '))

    def update_move(self, move: int) -> 'MonteCarloTreeSearch':
        return self
