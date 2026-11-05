"""Пакет игровой логики."""

from .clicker import AbstractClicker, SimpleClicker, SimpleRandomClicker
from .exceptions import NotEnoughMoney, TamagochiIsGone
from .game import AbstractGame, SimpleGame
from .models import Food, Medicine
from .tamagochi import AbstractTamagochi, SimpleTamagochi

__all__ = [
    "AbstractClicker",
    "AbstractGame",
    "AbstractTamagochi",
    "Food",
    "Medicine",
    "NotEnoughMoney",
    "SimpleClicker",
    "SimpleGame",
    "SimpleRandomClicker",
    "SimpleTamagochi",
    "TamagochiIsGone",
]
