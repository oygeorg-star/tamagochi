"""Модуль с моделями"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Food:
    """Модель объекта еды"""
    name: str  # наименование
    satiety: int  # на сколько единиц утоляет голод
    price: int  # стоимость

    def __repr__(self) -> str:
        """
        Возвращает строковое представление еды.

        :return: Название, стоимость и количество утоляемого голода.
        """
        return (
            f'{self.name} стоимость: {self.price}, '
            f'утоляет голод на {self.satiety} единиц'
        )


@dataclass
class Medicine:
    """Модель объекта лекарства"""
    name: str  # наименование
    price: int  # стоимость
    heal_hp: int  # сколько лечит HP
    number_of_uses: int  # максимальное количество применений
    uses: int = 0  # текущее количество применений

    def is_empty(self) -> bool:
        """
        Проверяет, закончилось ли лекарство.

        :return: True, если лекарство закончилось, иначе False.
        """
        return self.uses >= self.number_of_uses

    def __repr__(self) -> str:
        """
        Возвращает строковое представление лекарства.

        :return: Название, стоимость, восстановление здоровья
            и количество оставшихся применений.
        """
        remaining_uses = self.number_of_uses - self.uses

        return (
            f'{self.name} стоимость: {self.price}, '
            f'лечит на {self.heal_hp} HP, '
            f'использований: {remaining_uses}/{self.number_of_uses}'
        )
