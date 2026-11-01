"""Модуль с интерфейсом и реализацией класса игры"""

from abc import ABC, abstractmethod
from typing import Any

from .clicker import AbstractClicker
from .exceptions import NotEnoughMoney
from .models import Food, Medicine
from .tamagochi import AbstractTamagochi


class AbstractGame(ABC):
    """Интерфейс для логики игры"""

    @abstractmethod
    def __init__(
        self,
        tamagochi: AbstractTamagochi,
        clicker: AbstractClicker,
        all_food: list[Food],
        all_medicine: list[Medicine]
    ):
        """
        Абстрактный метод инициализации класса игры

        :param tamagochi: экземпляр тамагочи
        :param clicker: экземпляр кликера
        :param all_food: все доступные варианты еды
        :param all_medicine: все доступные варианты лекарств
        """
        raise NotImplementedError

    @abstractmethod
    def work(self) -> int:
        """
        Абстрактный метод для логики действия "работа

        :return: количество заработанных монет
        """
        raise NotImplementedError

    @abstractmethod
    def buy_food(self) -> None:
        """Абстрактный метод для покупки еды"""
        raise NotImplementedError

    @abstractmethod
    def buy_medicine(self) -> None:
        """Абстрактный метод для покупки лекарства"""
        raise NotImplementedError

    @abstractmethod
    def feed_tamagochi(self) -> None:
        """Абстрактный метод для кормления тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def heal_tamagochi(self) -> None:
        """Абстрактный метод для лечения тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def rest_tamagochi(self):
        """Абстрактный метод для отдыха тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def play_with_tamagochi(self):
        """Абстрактный метод для игры с тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def get_status(self) -> dict[str, Any]:
        """
        Абстрактный метод для получения статуса (всех характеристик) тамагочи

        :return: словарь со всеми характеристиками тамагочи
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def food(self) -> list[Food]:
        """
        Абстрактное свойство для доступа к сумке с едой

        :return: список с имеющимися (купленными) объектами еды
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def medicine(self) -> list[Medicine]:
        """
        Абстрактное свойство для доступа к сумке с лекарствами

        :return: список с имеющимися (купленными) объектами лекарств
        """
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
        """Инициализировать игру и доступные товары."""
        self.tamagochi = tamagochi
        self.clicker = clicker
        self.all_food = all_food
        self.all_medicine = all_medicine
        self.coins = 0
        self._food: list[Food] = []
        self._medicine: list[Medicine] = []

    @property
    def food(self) -> list[Food]:
        """Вернуть список купленной еды."""
        return self._food

    @property
    def medicine(self) -> list[Medicine]:
        """Вернуть список купленных лекарств."""
        return self._medicine

    def work(self) -> int:
        """Заработать монеты с помощью кликера."""
        self.clicker.click()
        income = self.clicker.income_per_click
        self.coins += income
        return income

    def get_status(self) -> dict[str, Any]:
        """Вернуть показатели питомца и количество монет."""
        return {
            **self.tamagochi.status,
            'coins': self.coins,
        }

    def buy_food(self) -> None:
        """Купить еду и добавить её в инвентарь."""
        for index, food in enumerate(self.all_food, start=1):
            print(f'{index}. {food}')

        choice = int(input('Выберите номер еды: '))
        if not 1 <= choice <= len(self.all_food):
            print('Неверный номер еды')
            return

        selected_food = self.all_food[choice - 1]

        if self.coins < selected_food.price:
            raise NotEnoughMoney('Недостаточно монет для покупки еды')

        self.coins -= selected_food.price
        self._food.append(selected_food)
        print(f'Куплено: {selected_food.name}')

    def buy_medicine(self) -> None:
        """Купить лекарство и добавить его в инвентарь."""
        for index, medicine in enumerate(self.all_medicine, start=1):
            print(f'{index}. {medicine}')

        choice = int(input('Выберите номер лекарства: '))
        if not 1 <= choice <= len(self.all_medicine):
            print('Неверный номер лекарства')
            return

        selected_medicine = self.all_medicine[choice - 1]

        if self.coins < selected_medicine.price:
            raise NotEnoughMoney(
                'Недостаточно монет для покупки лекарства'
            )

        self.coins -= selected_medicine.price
        self._medicine.append(
            Medicine(
                name=selected_medicine.name,
                price=selected_medicine.price,
                heal_hp=selected_medicine.heal_hp,
                number_of_uses=selected_medicine.number_of_uses,
            )
        )
        print(f'Куплено: {selected_medicine.name}')

    def feed_tamagochi(self) -> None:
        """Покормить питомца едой из инвентаря."""
        if not self._food:
            print('В инвентаре нет еды')
            return

        for index, food in enumerate(self._food, start=1):
            print(f'{index}. {food}')

        choice = int(input('Выберите номер еды: '))
        if not 1 <= choice <= len(self._food):
            print('Неверный номер еды')
            return

        selected_food = self._food.pop(choice - 1)
        self.tamagochi.feed(selected_food)

    def heal_tamagochi(self) -> None:
        """Вылечить питомца лекарством из инвентаря."""
        if not self._medicine:
            print('В инвентаре нет лекарств')
            return

        for index, medicine in enumerate(self._medicine, start=1):
            print(f'{index}. {medicine}')

        choice = int(input('Выберите номер лекарства: '))
        if not 1 <= choice <= len(self._medicine):
            print('Неверный номер лекарства')
            return

        selected_medicine = self._medicine[choice - 1]
        self.tamagochi.heal(selected_medicine)

        if selected_medicine.is_empty():
            self._medicine.pop(choice - 1)

    def rest_tamagochi(self) -> None:
        """Дать питомцу отдохнуть."""
        self.tamagochi.rest()

    def play_with_tamagochi(self) -> None:
        """Поиграть с питомцем."""
        self.tamagochi.play()
