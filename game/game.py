"""Интерфейс и реализация основной логики игры."""

from abc import ABC, abstractmethod
from dataclasses import replace
from typing import Any

from .clicker import AbstractClicker
from .exceptions import InvalidPrice, InvalidSelection, NotEnoughMoney
from .models import Food, Medicine
from .tamagochi import AbstractTamagochi


class AbstractGame(ABC):
    """Интерфейс управления питомцем, магазином и монетами."""

    @abstractmethod
    def __init__(
        self,
        tamagochi: AbstractTamagochi,
        clicker: AbstractClicker,
        all_food: list[Food],
        all_medicine: list[Medicine]
    ) -> None:
        """Получить питомца, кликер и каталоги магазина."""
        raise NotImplementedError

    @abstractmethod
    def work(self) -> int:
        """Выполнить работу и начислить монеты."""
        raise NotImplementedError

    @abstractmethod
    def click(self) -> int:
        """Выполнить клик и начислить монеты."""
        raise NotImplementedError

    @abstractmethod
    def buy_food(self, food: Food | None = None) -> None:
        """Купить выбранную еду."""
        raise NotImplementedError

    @abstractmethod
    def buy_medicine(self, medicine: Medicine | None = None) -> None:
        """Купить выбранное лекарство."""
        raise NotImplementedError

    @abstractmethod
    def feed_tamagochi(self, index: int | None = None) -> None:
        """Покормить питомца выбранной едой."""
        raise NotImplementedError

    @abstractmethod
    def heal_tamagochi(self, index: int | None = None) -> None:
        """Лечить питомца выбранным лекарством."""
        raise NotImplementedError

    @abstractmethod
    def rest_tamagochi(self) -> None:
        """Дать питомцу отдохнуть."""
        raise NotImplementedError

    @abstractmethod
    def play_with_tamagochi(self) -> None:
        """Поиграть с питомцем."""
        raise NotImplementedError

    @abstractmethod
    def is_alive(self) -> bool:
        """Проверить, жив ли питомец."""
        raise NotImplementedError

    @abstractmethod
    def is_sick(self) -> bool:
        """Проверить, болеет ли питомец."""
        raise NotImplementedError

    @abstractmethod
    def get_status(self) -> dict[str, Any]:
        """Получить показатели питомца и баланс."""
        raise NotImplementedError

    @property
    @abstractmethod
    def food(self) -> list[Food]:
        """Получить список приобретённой еды."""
        raise NotImplementedError

    @property
    @abstractmethod
    def medicine(self) -> list[Medicine]:
        """Получить список приобретённых лекарств."""
        raise NotImplementedError


class SimpleGame(AbstractGame):
    """Игровая логика с инкапсулированными состояниями."""

    def __init__(
        self,
        tamagochi: AbstractTamagochi,
        clicker: AbstractClicker,
        all_food: list[Food],
        all_medicine: list[Medicine]
    ) -> None:
        """Сохранить копии каталогов и создать пустой инвентарь."""
        self._tamagochi = tamagochi
        self._clicker = clicker
        self._all_food = list(all_food)
        self._all_medicine = [replace(item) for item in all_medicine]
        self._coins = 0
        self._food: list[Food] = []
        self._medicine: list[Medicine] = []

    @property
    def tamagochi(self) -> AbstractTamagochi:
        """Получить питомца для чтения его публичного интерфейса."""
        return self._tamagochi

    @property
    def clicker(self) -> AbstractClicker:
        """Получить интерфейс кликера."""
        return self._clicker

    @property
    def coins(self) -> int:
        """Получить текущий баланс монет."""
        return self._coins

    @coins.setter
    def coins(self, value: int) -> None:
        """Установить допустимый баланс для настройки игрового состояния."""
        if not isinstance(value, int) or value < 0:
            raise ValueError('Баланс должен быть неотрицательным целым числом')
        self._coins = value

    @property
    def all_food(self) -> list[Food]:
        """Получить копию каталога еды."""
        return list(self._all_food)

    @property
    def all_medicine(self) -> list[Medicine]:
        """Получить копию каталога лекарств."""
        return [replace(item) for item in self._all_medicine]

    @property
    def food(self) -> list[Food]:
        """Получить независимый список купленной еды."""
        return list(self._food)

    @property
    def medicine(self) -> list[Medicine]:
        """Получить независимый список купленных лекарств."""
        return [replace(item) for item in self._medicine]

    @staticmethod
    def _select_index(items: list[Any], item_name: str) -> int:
        """Запросить существующий номер товара и вернуть индекс."""
        if not items:
            raise InvalidSelection(f'Список {item_name} пуст')

        for number, item in enumerate(items, start=1):
            print(f'{number}. {item}')

        try:
            choice = int(input(f'Выберите номер {item_name}: '))
        except ValueError as error:
            raise InvalidSelection(f'Неверный номер {item_name}') from error

        if not 1 <= choice <= len(items):
            raise InvalidSelection(f'Неверный номер {item_name}')
        return choice - 1

    @staticmethod
    def _inventory_item(items: list[Any], index: int) -> Any:
        """Получить товар из инвентаря по допустимому индексу."""
        if not 0 <= index < len(items):
            raise InvalidSelection('Неверный индекс товара')
        return items[index]

    def click(self) -> int:
        """Начислить заработанные монеты и обновить питомца."""
        self._clicker.click()
        income = self._clicker.income_per_click
        self._coins += income
        self._tamagochi.update()
        return income

    def work(self) -> int:
        """Заработать монеты с помощью кликера."""
        return self.click()

    def is_alive(self) -> bool:
        """Проверить, жив ли питомец."""
        return self._tamagochi.is_alive()

    def is_sick(self) -> bool:
        """Проверить, болеет ли питомец."""
        return self._tamagochi.is_sick()

    def get_status(self) -> dict[str, Any]:
        """Вернуть снимок состояния питомца и баланса монет."""
        return {**self._tamagochi.status, 'coins': self._coins}

    def buy_food(self, food: Food | None = None) -> None:
        """Купить еду и поместить её в сумку."""
        if food is None:
            food = self._all_food[
                self._select_index(self._all_food, 'еды')
            ]
        if food.price < 0:
            raise InvalidPrice('Стоимость не может быть отрицательной')
        if self._coins < food.price:
            raise NotEnoughMoney('Недостаточно монет для покупки еды')
        self._coins -= food.price
        self._food.append(food)

    def buy_medicine(self, medicine: Medicine | None = None) -> None:
        """Купить отдельный экземпляр выбранного лекарства."""
        if medicine is None:
            medicine = self._all_medicine[
                self._select_index(self._all_medicine, 'лекарства')
            ]
        if medicine.price < 0:
            raise InvalidPrice('Стоимость не может быть отрицательной')
        if self._coins < medicine.price:
            raise NotEnoughMoney(
                'Недостаточно монет для покупки лекарства'
            )
        self._coins -= medicine.price
        self._medicine.append(Medicine(
            name=medicine.name,
            price=medicine.price,
            heal_hp=medicine.heal_hp,
            number_of_uses=medicine.number_of_uses,
        ))

    def feed_tamagochi(self, index: int | None = None) -> None:
        """Покормить питомца и удалить использованную еду."""
        if index is None:
            index = self._select_index(self._food, 'еды')
        food = self._inventory_item(self._food, index)
        try:
            self._tamagochi.feed(food)
        finally:
            self._food.pop(index)

    def heal_tamagochi(self, index: int | None = None) -> None:
        """Применить лекарство и убрать израсходованный предмет."""
        if index is None:
            index = self._select_index(self._medicine, 'лекарства')
        medicine = self._inventory_item(self._medicine, index)
        try:
            self._tamagochi.heal(medicine)
        finally:
            if medicine.is_empty():
                self._medicine.pop(index)

    def rest_tamagochi(self) -> None:
        """Передать питомцу команду отдыха."""
        self._tamagochi.rest()

    def play_with_tamagochi(self) -> None:
        """Передать питомцу команду игры."""
        self._tamagochi.play()
