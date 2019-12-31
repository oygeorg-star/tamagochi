"""Модели еды и лекарств для игрового магазина."""

from dataclasses import dataclass

from .exceptions import MedicineIsEmpty


@dataclass(frozen=True, slots=True)
class Food:
    """Описание еды, её стоимости и питательности."""

    name: str
    satiety: int
    price: int

    def __repr__(self) -> str:
        """Вернуть описание еды для меню."""
        return (
            f'{self.name} стоимость: {self.price}, '
            f'утоляет голод на {self.satiety} единиц'
        )


@dataclass
class Medicine:
    """Описание лекарства и оставшихся применений."""

    name: str
    price: int
    heal_hp: int
    number_of_uses: int
    uses: int = 0

    def is_empty(self) -> bool:
        """Проверить, израсходовано ли лекарство."""
        return self.uses >= self.number_of_uses

    def use(self) -> None:
        """Использовать лекарство или сообщить об отсутствии доз."""
        if self.is_empty():
            raise MedicineIsEmpty('Лекарство закончилось')
        self.uses += 1

    def __repr__(self) -> str:
        """Вернуть описание лекарства для меню."""
        remaining_uses = max(0, self.number_of_uses - self.uses)
        return (
            f'{self.name} стоимость: {self.price}, '
            f'лечит на {self.heal_hp} HP, '
            f'использований: {remaining_uses}/{self.number_of_uses}'
        )
