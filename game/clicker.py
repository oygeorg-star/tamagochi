"""Модуль с интерфейсом и реализацией кликера."""

from abc import ABC, abstractmethod
from random import randint


class AbstractClicker(ABC):
    """Интерфейс для кликера."""

    @abstractmethod
    def __init__(self) -> None:
        """Инициализирует кликер."""
        raise NotImplementedError

    @abstractmethod
    def click(self) -> None:
        """Выполняет клик для получения монет."""
        raise NotImplementedError

    @property
    @abstractmethod
    def income_per_click(self) -> int:
        """Возвращает количество монет за один клик."""
        raise NotImplementedError


class SimpleClicker(AbstractClicker):
    """Кликер с фиксированным количеством монет за нажатие."""

    def __init__(self, income_per_click: int) -> None:
        """Устанавливает доход за один клик."""
        self._income_per_click = income_per_click

    @property
    def income_per_click(self) -> int:
        """Возвращает количество монет за один клик."""
        return self._income_per_click

    def click(self) -> None:
        """Выполняет клик."""


class SimpleRandomClicker(AbstractClicker):
    """Кликер со случайным количеством монет за нажатие."""

    def __init__(self, min_income: int, max_income: int) -> None:
        """Устанавливает диапазон случайного дохода."""
        if min_income > max_income:
            raise ValueError(
                "Минимальный доход не может быть "
                "больше максимального"
            )

        self.min_income = min_income
        self.max_income = max_income
        self._income_per_click = min_income

    @property
    def income_per_click(self) -> int:
        """Возвращает доход за последний клик."""
        return self._income_per_click

    def click(self) -> None:
        """Генерирует случайный доход за один клик."""
        self._income_per_click = randint(self.min_income, self.max_income)
