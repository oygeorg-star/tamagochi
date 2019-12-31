"""Интерфейс и реализация логики виртуального питомца."""

from abc import ABC, abstractmethod

from .constants import (
    HUNGER_DAMAGE,
    HUNGER_DAMAGE_THRESHOLD,
    INITIAL_ENERGY,
    INITIAL_FATIGUE,
    INITIAL_HP,
    INITIAL_HUNGER,
    MAX_STAT,
    MIN_STAT,
    NO_ENERGY_DAMAGE,
    PLAY_ENERGY_COST,
    PLAY_FATIGUE_INCREASE,
    PLAY_HUNGER_INCREASE,
    REST_ENERGY_RECOVERY,
    REST_FATIGUE_RECOVERY,
    SICK_HP_THRESHOLD,
    SICK_REST_ENERGY_RECOVERY,
    UPDATE_ENERGY,
    UPDATE_HUNGER,
)
from .exceptions import TamagochiIsGone
from .models import Food, Medicine


class AbstractTamagochi(ABC):
    """Интерфейс действий и состояний виртуального питомца."""

    @abstractmethod
    def feed(self, food: Food) -> None:
        """Покормить питомца выбранной едой."""
        raise NotImplementedError

    @abstractmethod
    def play(self) -> None:
        """Поиграть с питомцем."""
        raise NotImplementedError

    @abstractmethod
    def rest(self) -> None:
        """Дать питомцу отдохнуть."""
        raise NotImplementedError

    @abstractmethod
    def heal(self, medicine: Medicine) -> None:
        """Вылечить питомца выбранным лекарством."""
        raise NotImplementedError

    @property
    @abstractmethod
    def status(self) -> dict[str, int]:
        """Получить текущие показатели питомца."""
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
    def update(self) -> None:
        """Обновить показатели питомца после действия."""
        raise NotImplementedError


class SimpleTamagochi(AbstractTamagochi):
    """Виртуальный питомец со здоровьем, голодом и энергией."""

    def __init__(self) -> None:
        """Установить исходные значения показателей питомца."""
        self._hp = INITIAL_HP
        self._hunger = INITIAL_HUNGER
        self._energy = INITIAL_ENERGY
        self._fatigue = INITIAL_FATIGUE

    @property
    def hp(self) -> int:
        """Вернуть уровень здоровья."""
        return self._hp

    @hp.setter
    def hp(self, value: int) -> None:
        """Установить допустимое значение показателя питомца."""
        if not isinstance(value, int) or not MIN_STAT <= value <= MAX_STAT:
            raise ValueError('Показатель должен быть в пределах от 0 до 100')
        self._hp = value

    @property
    def hunger(self) -> int:
        """Вернуть уровень голода."""
        return self._hunger

    @hunger.setter
    def hunger(self, value: int) -> None:
        """Установить допустимое значение показателя питомца."""
        if not isinstance(value, int) or not MIN_STAT <= value <= MAX_STAT:
            raise ValueError('Показатель должен быть в пределах от 0 до 100')
        self._hunger = value

    @property
    def energy(self) -> int:
        """Вернуть уровень энергии."""
        return self._energy

    @energy.setter
    def energy(self, value: int) -> None:
        """Установить допустимое значение показателя питомца."""
        if not isinstance(value, int) or not MIN_STAT <= value <= MAX_STAT:
            raise ValueError('Показатель должен быть в пределах от 0 до 100')
        self._energy = value

    @property
    def fatigue(self) -> int:
        """Вернуть уровень усталости."""
        return self._fatigue

    @fatigue.setter
    def fatigue(self, value: int) -> None:
        """Установить допустимое значение показателя питомца."""
        if not isinstance(value, int) or not MIN_STAT <= value <= MAX_STAT:
            raise ValueError('Показатель должен быть в пределах от 0 до 100')
        self._fatigue = value

    @property
    def status(self) -> dict[str, int]:
        """Вернуть независимый снимок показателей питомца."""
        return {
            'hp': self._hp,
            'hunger': self._hunger,
            'energy': self._energy,
            'fatigue': self._fatigue,
        }

    def is_alive(self) -> bool:
        """Проверить, жив ли питомец."""
        return self._hp > MIN_STAT

    def is_sick(self) -> bool:
        """Проверить, болеет ли питомец."""
        return self._hp < SICK_HP_THRESHOLD

    def _ensure_alive(self) -> None:
        """Сообщить о смерти питомца игровым исключением."""
        if not self.is_alive():
            raise TamagochiIsGone('Питомец погиб')

    def feed(self, food: Food) -> None:
        """Уменьшить голод питомца и обновить его состояние."""
        self._ensure_alive()
        self._hunger = max(MIN_STAT, self._hunger - food.satiety)
        self.update()

    def play(self) -> None:
        """Потратить энергию питомца на игру."""
        self._ensure_alive()
        self._energy = max(MIN_STAT, self._energy - PLAY_ENERGY_COST)
        self._hunger = min(MAX_STAT, self._hunger + PLAY_HUNGER_INCREASE)
        self._fatigue = min(MAX_STAT, self._fatigue + PLAY_FATIGUE_INCREASE)
        self.update()

    def rest(self) -> None:
        """Восстановить энергию питомца и снизить усталость."""
        self._ensure_alive()
        recovery = (
            SICK_REST_ENERGY_RECOVERY
            if self.is_sick() else REST_ENERGY_RECOVERY
        )
        self._energy = min(MAX_STAT, self._energy + recovery)
        self._fatigue = max(MIN_STAT, self._fatigue - REST_FATIGUE_RECOVERY)
        self.update()

    def heal(self, medicine: Medicine) -> None:
        """Потратить применение лекарства и восстановить здоровье."""
        self._ensure_alive()
        hp_before = self._hp
        medicine.use()
        self.update()
        self._hp = min(MAX_STAT, hp_before + medicine.heal_hp)

    def update(self) -> None:
        """Изменить показатели питомца после игрового действия."""
        self._ensure_alive()
        self._hunger = min(MAX_STAT, self._hunger + UPDATE_HUNGER)
        self._energy = max(MIN_STAT, self._energy - UPDATE_ENERGY)

        if self._hunger >= HUNGER_DAMAGE_THRESHOLD:
            self._hp -= HUNGER_DAMAGE
        if self._energy == MIN_STAT:
            self._hp -= NO_ENERGY_DAMAGE

        self._hp = max(MIN_STAT, self._hp)
        self._ensure_alive()
