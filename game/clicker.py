"""Интерфейс и реализации механики заработка монет."""

from abc import ABC, abstractmethod
from random import randint


class AbstractClicker(ABC):
    """Интерфейс кликера для получения монет."""

    @abstractmethod
    def __init__(self) -> None:
        """Инициализировать параметры кликера."""
        raise NotImplementedError

    @abstractmethod
    def click(self) -> None:
        """Выполнить клик и рассчитать доход."""
        raise NotImplementedError

    @property
    @abstractmethod
    def income_per_click(self) -> int:
        """Вернуть доход за последний клик."""
        raise NotImplementedError


class SimpleClicker(AbstractClicker):
    """Кликер с фиксированным доходом."""

    def __init__(self, income_per_click: int) -> None:
        """Сохранить фиксированную величину дохода."""
        self._income_per_click = income_per_click

    @property
    def income_per_click(self) -> int:
        """Вернуть фиксированный доход за клик."""
        return self._income_per_click

    def click(self) -> None:
        """Выполнить клик с фиксированным доходом."""


class SimpleRandomClicker(AbstractClicker):
    """Кликер со случайным доходом в заданных пределах."""

    def __init__(self, min_income: int, max_income: int) -> None:
        """Установить границы случайного дохода."""
        self._min_income = min_income
        self._max_income = max_income
        self._income_per_click = 0

    @property
    def min_income(self) -> int:
        """Вернуть минимальный доход за клик."""
        return self._min_income

    @property
    def max_income(self) -> int:
        """Вернуть максимальный доход за клик."""
        return self._max_income

    @property
    def income_per_click(self) -> int:
        """Вернуть доход за последний клик."""
        return self._income_per_click

    def click(self) -> None:
        """Определить доход за очередной клик."""
        self._income_per_click = randint(
            self._min_income, self._max_income
        )
