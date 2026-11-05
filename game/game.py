
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
    def click(self) -> int:
        """Выполняет клик и начисляет заработанные монеты."""
        raise NotImplementedError

    @abstractmethod
    def work(self) -> int:
        """Выполняет работу и начисляет заработанные монеты."""
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
    def buy_food(self, food: Food | None = None) -> None:
        """Покупает еду и добавляет её в инвентарь."""
        raise NotImplementedError

    @abstractmethod
    def buy_medicine(
        self, medicine: Medicine | None = None
    ) -> None:
        """Покупает лекарство и добавляет его в инвентарь."""
        raise NotImplementedError

    @abstractmethod
    def feed_tamagochi(self, food: Food | int | None = None) -> None:
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

    def click(self) -> int:
        """Выполняет клик, начисляет монеты и обновляет питомца."""
        self.clicker.click()
        income = self.clicker.income_per_click
        self.coins += income
        self.tamagochi.update()
        return income

    def work(self) -> int:
        """Выполняет работу и начисляет заработанные монеты."""
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
        """Покупает еду и добавляет её в инвентарь."""
        if food is None:
            if not self.all_food:
                raise ValueError("Нет доступной еды для покупки")
            food = self.all_food[0]

        price = food.price

        if price < 0:
            raise ValueError('Стоимость не может быть отрицательной')

        if self.coins < price:
            raise NotEnoughMoney('Недостаточно монет для покупки еды')

        self.coins -= price
        self._food.append(food)

    def buy_medicine(
        self, medicine: Medicine | None = None
    ) -> None:
        """Покупает лекарство и добавляет его в инвентарь."""
        if medicine is None:
            if not self.all_medicine:
                raise ValueError("Нет доступных лекарств для покупки")
            medicine = self.all_medicine[0]

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

    def feed_tamagochi(self, food: Food | int | None = None) -> None:
        """Кормит питомца выбранной едой из инвентаря."""
        if isinstance(food, int):
            index = food
            selected_food = self._food[index]
        elif food is None:
            if not self._food:
                raise ValueError("В инвентаре нет еды")

            for number, item in enumerate(self._food, start=1):
                print(f"{number}. {item}")

            print("Выберите номер еды: ", end="")
            try:
                choice = int(input())
            except TypeError:
                choice = int(input("Выберите номер еды: "))
            except ValueError:
                raise ValueError("Неверный номер еды") from None

            if not 1 <= choice <= len(self._food):
                raise ValueError("Неверный номер еды")

            index = choice - 1
            selected_food = self._food[index]
        else:
            selected_food = food
            index = next(
                (
                    i for i, item in enumerate(self._food)
                    if item is food
                ),
                -1,
            )

            if index == -1:
                try:
                    index = self._food.index(food)
                except ValueError as error:
                    raise ValueError(
                        "Еда отсутствует в инвентаре"
                    ) from error

        try:
            self.tamagochi.feed(selected_food)
        finally:
            self._food.pop(index)

    def heal_tamagochi(self, index: int) -> None:
        """Лечит питомца выбранным лекарством."""
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
