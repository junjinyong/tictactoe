from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import Tuple


@dataclass(init=True, frozen=True)
class Participant(metaclass=ABCMeta):
    def __init_subclass__(cls, **kwargs):
        pass

    @abstractmethod
    def make_move(self) -> Tuple['Participant', int]:
        pass

    @abstractmethod
    def update_move(self, move: int) -> 'Participant':
        pass
