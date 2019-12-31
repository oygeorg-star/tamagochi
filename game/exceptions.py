"""Исключения для ошибок игровой логики."""


class GameError(Exception):
    """Базовая ошибка игрового процесса."""


class TamagochiIsGone(GameError):
    """Ошибка при гибели питомца."""


class NotEnoughMoney(GameError):
    """Ошибка при недостаточном количестве монет."""


class InvalidSelection(GameError, IndexError):
    """Ошибка выбора отсутствующего товара или позиции."""


class InvalidPrice(GameError, ValueError):
    """Ошибка недопустимой стоимости товара."""


class MedicineIsEmpty(GameError, ValueError):
    """Ошибка использования закончившегося лекарства."""
