"""Модуль с интерфейсом и реализацией кликера"""

from abc import ABC, abstractmethod
from random import randint


class AbstractClicker(ABC):
    """Интерфейс для кликера"""

    @abstractmethod
    def __init__(self) -> None:
        """Абстрактный метод инициализации"""
        raise NotImplementedError

    @abstractmethod
    def click(self) -> None:
        """Абстрактный метод клика для накапливания монет"""
        raise NotImplementedError

    @property
    @abstractmethod
    def income_per_click(self) -> int:
        """Абстрактное свойство для доступа к количеству монет за клик"""
        raise NotImplementedError


class SimpleRandomClicker(AbstractClicker):
    """Кликер со случайным количеством монет за нажатие."""

    def __init__(self, min_income: int, max_income: int) -> None:
        """
        Устанавливает минимальный и максимальный доход за клик.

        :param min_income: Минимальное количество монет за клик.
        :param max_income: Максимальное количество монет за клик.
        :return: None.
        """
        self.min_income = min_income
        self.max_income = max_income
        self._income_per_click = 0

    @property
    def income_per_click(self) -> int:
        """Вернуть количество монет за последний клик."""
        return self._income_per_click

    def click(self) -> None:
        """Определить случайный доход за один клик."""
        self._income_per_click = randint(
            self.min_income,
            self.max_income
        )
