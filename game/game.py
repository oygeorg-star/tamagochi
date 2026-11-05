"""Модуль с интерфейсом и реализацией класса игры."""

from abc import ABC, abstractmethod
from typing import Any

from .clicker import AbstractClicker
from .exceptions import NotEnoughMoney
from .models import Food, Medicine
from .tamagochi import AbstractTamagochi


class AbstractGame(ABC):
    """Интерфейс для логики игры."""

    @abstractmethod
    def __init__(
        self,
        tamagochi: AbstractTamagochi,
        clicker: AbstractClicker,
        all_food: list[Food],
        all_medicine: list[Medicine]
    ) -> None:
        """Инициализирует игру."""
        raise NotImplementedError

    @abstractmethod
    def work(self) -> int:
        """Выполняет работу и начисляет заработанные монеты."""
        raise NotImplementedError

    @abstractmethod
    def click(self) -> int:
        """Выполняет клик и начисляет заработанные монеты."""
        raise NotImplementedError

    @abstractmethod
    def buy_food(self, food: Food) -> None:
        """Покупает еду и добавляет её в инвентарь."""
        raise NotImplementedError

    @abstractmethod
    def buy_medicine(self, medicine: Medicine) -> None:
        """Покупает лекарство и добавляет его в инвентарь."""
        raise NotImplementedError

    @abstractmethod
    def feed_tamagochi(self, index: int) -> None:
        """Кормит питомца выбранной едой."""
        raise NotImplementedError

    @abstractmethod
    def heal_tamagochi(self, index: int) -> None:
        """Лечит питомца выбранным лекарством."""
        raise NotImplementedError

    @abstractmethod
    def rest_tamagochi(self) -> None:
        """Даёт питомцу отдохнуть."""
        raise NotImplementedError

    @abstractmethod
    def play_with_tamagochi(self) -> None:
        """Играет с питомцем."""
        raise NotImplementedError

    @abstractmethod
    def is_alive(self) -> bool:
        """Проверяет, жив ли питомец."""
        raise NotImplementedError

    @abstractmethod
    def is_sick(self) -> bool:
        """Проверяет, болеет ли питомец."""
        raise NotImplementedError

    @abstractmethod
    def get_status(self) -> dict[str, Any]:
        """Возвращает характеристики питомца и баланс игры."""
        raise NotImplementedError

    @property
    @abstractmethod
    def food(self) -> list[Food]:
        """Возвращает сумку с едой."""
        raise NotImplementedError

    @property
    @abstractmethod
    def medicine(self) -> list[Medicine]:
        """Возвращает сумку с лекарствами."""
        raise NotImplementedError


class SimpleGame(AbstractGame):
    """Основная логика игры с питомцем."""

    def __init__(
        self,
        tamagochi: AbstractTamagochi,
        clicker: AbstractClicker,
        all_food: list[Food],
        all_medicine: list[Medicine]
    ) -> None:
        """Инициализирует игру, питомца, кликер и доступные товары."""
        self.tamagochi = tamagochi
        self.clicker = clicker
        self.all_food = all_food
        self.all_medicine = all_medicine
        self.coins = 0
        self._food: list[Food] = []
        self._medicine: list[Medicine] = []

    @property
    def food(self) -> list[Food]:
        """Возвращает список купленной еды."""
        return self._food

    @property
    def medicine(self) -> list[Medicine]:
        """Возвращает список купленных лекарств."""
        return self._medicine

    @staticmethod
    def _select_index(items: list[Any], item_name: str) -> int:
        """Запрашивает номер товара и возвращает его индекс."""
        if not items:
            raise ValueError(f'Список {item_name} пуст')

        for number, item in enumerate(items, start=1):
            print(f'{number}. {item}')

        try:
            choice = int(input(f'Выберите номер {item_name}: '))
        except ValueError:
            raise ValueError(
                f'Неверный номер {item_name}'
            ) from None

        if not 1 <= choice <= len(items):
            raise ValueError(f'Неверный номер {item_name}')

        return choice - 1

    def click(self) -> int:
        """Выполняет клик, начисляет монеты и обновляет питомца."""
        self.clicker.click()
        income = self.clicker.income_per_click
        self.coins += income
        self.tamagochi.update()
        return income

    def work(self) -> int:
        """Выполняет работу с помощью кликера."""
        return self.click()

    def is_alive(self) -> bool:
        """Проверяет, жив ли питомец."""
        return self.tamagochi.is_alive()

    def is_sick(self) -> bool:
        """Проверяет, болеет ли питомец."""
        return self.tamagochi.is_sick()

    def get_status(self) -> dict[str, Any]:
        """Возвращает показатели питомца и количество монет."""
        return {
            **self.tamagochi.status,
            'coins': self.coins,
        }

    def buy_food(self, food: Food | None = None) -> None:
        """Покупает выбранную еду и добавляет её в инвентарь."""
        if food is None:
            index = self._select_index(self.all_food, 'еды')
            food = self.all_food[index]

        price = food.price

        if price < 0:
            raise ValueError('Стоимость не может быть отрицательной')

        if self.coins < price:
            raise NotEnoughMoney('Недостаточно монет для покупки еды')

        self.coins -= price
        self._food.append(food)

    def buy_medicine(
        self,
        medicine: Medicine | None = None
    ) -> None:
        """Покупает выбранное лекарство и добавляет его в инвентарь."""
        if medicine is None:
            index = self._select_index(
                self.all_medicine,
                'лекарства'
            )
            medicine = self.all_medicine[index]

        price = medicine.price

        if price < 0:
            raise ValueError('Стоимость не может быть отрицательной')

        if self.coins < price:
            raise NotEnoughMoney(
                'Недостаточно монет для покупки лекарства'
            )

        self.coins -= price
        self._medicine.append(
            Medicine(
                name=medicine.name,
                price=medicine.price,
                heal_hp=medicine.heal_hp,
                number_of_uses=medicine.number_of_uses,
            )
        )

    def feed_tamagochi(self, index: int | None = None) -> None:
        """Кормит питомца выбранной едой из инвентаря."""
        if index is None:
            index = self._select_index(self._food, 'еды')

        food = self._food[index]

        try:
            self.tamagochi.feed(food)
        finally:
            self._food.pop(index)

    def heal_tamagochi(self, index: int | None = None) -> None:
        """Лечит питомца выбранным лекарством из инвентаря."""
        if index is None:
            index = self._select_index(self._medicine, 'лекарства')

        medicine = self._medicine[index]

        try:
            self.tamagochi.heal(medicine)
        finally:
            if medicine.is_empty():
                self._medicine.pop(index)

    def rest_tamagochi(self) -> None:
        """Даёт питомцу отдохнуть."""
        self.tamagochi.rest()

    def play_with_tamagochi(self) -> None:
        """Играет с питомцем."""
        self.tamagochi.play()
