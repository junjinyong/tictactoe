from participant.participant import *


@dataclass(init=True, frozen=True)
class User(Participant):
    def make_move(self) -> Tuple['User', int]:
        return self, int(input('Your move: '))

    def update_move(self, move: int) -> 'User':
        return self
