"""Игровые модели, интерфейсы и реализации «Тамагочи»."""

from .clicker import AbstractClicker, SimpleClicker, SimpleRandomClicker
from .game import AbstractGame, SimpleGame
from .models import Food, Medicine
from .tamagochi import AbstractTamagochi, SimpleTamagochi

__all__ = [
    'AbstractClicker',
    'AbstractGame',
    'AbstractTamagochi',
    'Food',
    'Medicine',
    'SimpleClicker',
    'SimpleGame',
    'SimpleRandomClicker',
    'SimpleTamagochi',
]
