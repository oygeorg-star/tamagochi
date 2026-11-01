"""Модуль с интерфейсом и реализациями класса тамагочи"""

from abc import ABC, abstractmethod

from .exceptions import TamagochiIsGone
from .models import Food, Medicine


class AbstractTamagochi(ABC):
    """Интерфейс логики тамагочи"""

    @abstractmethod
    def feed(self, food: Food) -> None:
        """
        Абстрактный метод для кормления тамагочи

        :param food: объект еды для кормления
        """
        raise NotImplementedError

    @abstractmethod
    def play(self) -> None:
        """Абстрактный метод для игры с тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def rest(self) -> None:
        """Абстрактный метод для отдыха тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def heal(self, medicine: Medicine) -> None:
        """
        Абстрактный метод для лечения тамагочи

        :param medicine: лекарство для лечения
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def status(self) -> dict[str, int]:
        """
        Абстрактное свойство для доступа ко всем состояниям тамагочи

        :return: словарь со всеми состояниями тамагочи
        """
        raise NotImplementedError

    @abstractmethod
    def is_alive(self) -> bool:
        """
        Абстрактный метод для проверки жив ли тамагочи

        :return: True если жив, иначе False
        """
        raise NotImplementedError

    @abstractmethod
    def is_sick(self) -> bool:
        """
        Абстрактный метод для проверки, не заболел ли тамагочи

        :return: True если тамагочи болеет, иначе False
        """
        raise NotImplementedError

    @abstractmethod
    def update(self) -> None:
        """
        Абстрактный метод для обновления состояний тамагочи.
        Должен использоваться после каждого взаимодействия с тамагочи
        """
        raise NotImplementedError


class SimpleTamagochi(AbstractTamagochi):
    """Питомец с показателями здоровья, голода и энергии."""

    def __init__(self) -> None:
        """Установить начальные показатели питомца."""
        self.hp = 100
        self.hunger = 0
        self.energy = 100
        self.fatigue = 0

    @property
    def status(self) -> dict[str, int]:
        """Вернуть текущие показатели питомца."""
        return {
            'hp': self.hp,
            'hunger': self.hunger,
            'energy': self.energy,
            'fatigue': self.fatigue,
        }

    def is_alive(self) -> bool:
        """Проверить, жив ли питомец."""
        return self.hp > 0

    def is_sick(self) -> bool:
        """Проверить, болеет ли питомец."""
        return self.hp < 30

    def feed(self, food: Food) -> None:
        """Покормить питомца указанной едой."""
        self.hunger = max(0, self.hunger - food.satiety)
        self.update()

    def play(self) -> None:
        """Поиграть с питомцем, потратив энергию."""
        self.energy = max(0, self.energy - 15)
        self.hunger = min(100, self.hunger + 10)
        self.fatigue = min(100, self.fatigue + 10)
        self.update()

    def rest(self) -> None:
        """Восстановить энергию питомца."""
        restored_energy = 10 if self.is_sick() else 25
        self.energy = min(100, self.energy + restored_energy)
        self.fatigue = max(0, self.fatigue - 20)
        self.update()

    def heal(self, medicine: Medicine) -> None:
        """Вылечить питомца, расходуя применение лекарства."""
        if medicine.is_empty():
            raise ValueError('Лекарство закончилось')

        self.hp = min(100, self.hp + medicine.heal_hp)
        medicine.uses += 1
        self.update()

    def update(self) -> None:
        """Обновить показатели питомца после действия."""
        if not self.is_alive():
            raise TamagochiIsGone('Питомец погиб')

        self.hunger = min(100, self.hunger + 5)
        self.energy = max(0, self.energy - 5)

        if self.hunger >= 80:
            self.hp -= 10

        if self.energy == 0:
            self.hp -= 5

        self.hp = max(0, self.hp)

        if not self.is_alive():
            raise TamagochiIsGone('Питомец погиб')
