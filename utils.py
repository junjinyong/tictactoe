from typing import Type
import importlib
from typing import Dict

from participant.participant import *


def get_class_by_name(class_name: str) -> Type[Participant]:
    lookup_: Dict[str, str] = {
        'User': 'user',
        'Rand': 'rand',
        'MinimaxHeuristic': 'minimax',
        'MinimaxExhaustive': 'minimax',
        'AlphaBetaHeuristic': 'alphabeta',
        'AlphaBetaExhaustive': 'alphabeta',
        'MonteCarloSearch': 'monteCarloSearch',
        'MonteCarloTreeSearch': 'monteCarloTreeSearch',
    }
    module_name: str = f'participant.{lookup_[class_name]}'
    try:
        module = importlib.import_module(module_name)
        cls = getattr(module, class_name)
        if issubclass(cls, module.Participant):
            return cls
        else:
            raise ValueError(f'{class_name} is not a subclass of Participant')
    except (ImportError, AttributeError):
        raise ValueError(f'Invalid module or class name: {module_name}.{class_name}')
