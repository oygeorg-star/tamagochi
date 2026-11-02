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
    ) -> None:
        """
        Абстрактный метод инициализации класса игры

        :param tamagochi: экземпляр тамагочи
        :param clicker: экземпляр кликера
        :param all_food: все доступные варианты еды
        :param all_medicine: все доступные варианты лекарств
        :return: None.
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
        """Покупает еду. Возвращает None."""
        raise NotImplementedError

    @abstractmethod
    def buy_medicine(self) -> None:
        """Покупает лекарство. Возвращает None."""
        raise NotImplementedError

    @abstractmethod
    def feed_tamagochi(self) -> None:
        """Кормит питомца. Возвращает None."""
        raise NotImplementedError

    @abstractmethod
    def heal_tamagochi(self) -> None:
        """Лечит питомца. Возвращает None."""
        raise NotImplementedError

    @abstractmethod
    def rest_tamagochi(self) -> None:
        """Даёт питомцу отдохнуть. Возвращает None."""
        raise NotImplementedError

    @abstractmethod
    def play_with_tamagochi(self) -> None:
        """Играет с питомцем. Возвращает None."""
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
        """
        Инициализирует игру, питомца, кликер и доступные товары.

        :param tamagochi: Экземпляр питомца.
        :param clicker: Экземпляр кликера.
        :param all_food: Список доступной для покупки еды.
        :param all_medicine: Список доступных лекарств.
        :return: None.
        """
        self.tamagochi = tamagochi
        self.clicker = clicker
        self.all_food = all_food
        self.all_medicine = all_medicine
        self.coins = 0
        self._food: list[Food] = []
        self._medicine: list[Medicine] = []

    @property
    def food(self) -> list[Food]:
        """
        Возвращает список купленной еды.

        :return: Список объектов Food в инвентаре.
        """
        return self._food

    @property
    def medicine(self) -> list[Medicine]:
        """
        Возвращает список купленных лекарств.

        :return: Список объектов Medicine в инвентаре.
        """
        return self._medicine

    def work(self) -> int:
        """
        Начисляет монеты за работу с помощью кликера.

        :return: Количество заработанных монет.
        """
        self.clicker.click()
        income = self.clicker.income_per_click
        self.coins += income
        return income

    def get_status(self) -> dict[str, Any]:
        """
        Возвращает показатели питомца и количество монет.

        :return: Словарь с характеристиками питомца и балансом монет.
        """
        return {
            **self.tamagochi.status,
            'coins': self.coins,
        }

    def buy_food(self) -> None:
        """
        Покупает выбранную еду и добавляет её в инвентарь.

        :return: None.
        :raises NotEnoughMoney: Если недостаточно монет для покупки.
        """
        for index, food in enumerate(self.all_food, start=1):
            print(f'{index}. {food}')

        try:
            choice = int(input('Выберите номер еды: '))
        except ValueError:
            print('Неверный номер еды')
            return
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
        """
        Покупает выбранное лекарство и добавляет его в инвентарь.

        :return: None.
        :raises NotEnoughMoney: Если недостаточно монет для покупки.
        """
        for index, medicine in enumerate(self.all_medicine, start=1):
            print(f'{index}. {medicine}')

        try:
            choice = int(input('Выберите номер лекарства: '))
        except ValueError:
            print('Неверный номер лекарства')
            return
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
        """
        Кормит питомца выбранной едой из инвентаря.

        :return: None.
        :raises TamagochiIsGone: Если питомец погиб после кормления.
        """
        if not self._food:
            print('В инвентаре нет еды')
            return

        for index, food in enumerate(self._food, start=1):
            print(f'{index}. {food}')

        try:
            choice = int(input('Выберите номер еды: '))
        except ValueError:
            print('Неверный номер еды')
            return
        if not 1 <= choice <= len(self._food):
            print('Неверный номер еды')
            return

        selected_food = self._food.pop(choice - 1)
        self.tamagochi.feed(selected_food)

    def heal_tamagochi(self) -> None:
        """
        Лечит питомца выбранным лекарством из инвентаря.

        :return: None.
        :raises ValueError: Если выбранное лекарство закончилось.
        :raises TamagochiIsGone: Если питомец погиб после лечения.
        """
        if not self._medicine:
            print('В инвентаре нет лекарств')
            return

        for index, medicine in enumerate(self._medicine, start=1):
            print(f'{index}. {medicine}')

        try:
            choice = int(input('Выберите номер лекарства: '))
        except ValueError:
            print('Неверный номер лекарства')
            return
        if not 1 <= choice <= len(self._medicine):
            print('Неверный номер лекарства')
            return

        selected_medicine = self._medicine[choice - 1]
        self.tamagochi.heal(selected_medicine)

        if selected_medicine.is_empty():
            self._medicine.pop(choice - 1)

    def rest_tamagochi(self) -> None:
        """
        Даёт питомцу отдохнуть и восстановить энергию.

        :return: None.
        :raises TamagochiIsGone: Если питомец погиб после отдыха.
        """
        self.tamagochi.rest()

    def play_with_tamagochi(self) -> None:
        """
        Организует игру с питомцем.

        :return: None.
        :raises TamagochiIsGone: Если питомец погиб после игры.
        """
        self.tamagochi.play()
