import pytest

from game.exceptions import TamagochiIsGone
from game.models import Food, Medicine
from game.tamagochi import SimpleTamagochi


def test_initial_status():
    tamagochi = SimpleTamagochi()

    assert tamagochi.status == {
        'hp': 100,
        'hunger': 0,
        'energy': 100,
        'fatigue': 0,
    }


def test_is_alive():
    tamagochi = SimpleTamagochi()

    assert tamagochi.is_alive() is True

    tamagochi.hp = 0

    assert tamagochi.is_alive() is False


def test_is_sick():
    tamagochi = SimpleTamagochi()

    assert tamagochi.is_sick() is False

    tamagochi.hp = 29

    assert tamagochi.is_sick() is True


def test_feed_reduces_hunger():
    tamagochi = SimpleTamagochi()
    tamagochi.hunger = 40

    food = Food(name='Бургер', satiety=20, price=40)

    tamagochi.feed(food)

    assert tamagochi.hunger == 25
    assert tamagochi.energy == 95


def test_play_changes_status():
    tamagochi = SimpleTamagochi()

    tamagochi.play()

    assert tamagochi.energy == 80
    assert tamagochi.hunger == 15
    assert tamagochi.fatigue == 10


def test_rest_increases_energy():
    tamagochi = SimpleTamagochi()
    tamagochi.energy = 50

    tamagochi.rest()

    assert tamagochi.energy == 70
    assert tamagochi.fatigue == 0


def test_heal_increases_hp():
    tamagochi = SimpleTamagochi()
    tamagochi.hp = 50

    medicine = Medicine(
        name='Ибупрофен',
        price=30,
        heal_hp=20,
        number_of_uses=2
    )

    tamagochi.heal(medicine)

    assert tamagochi.hp == 70
    assert medicine.uses == 1


def test_heal_does_not_exceed_max_hp():
    tamagochi = SimpleTamagochi()
    tamagochi.hp = 90

    medicine = Medicine(
        name='Ибупрофен',
        price=30,
        heal_hp=20,
        number_of_uses=2
    )

    tamagochi.heal(medicine)

    assert tamagochi.hp == 100


def test_heal_with_empty_medicine():
    tamagochi = SimpleTamagochi()

    medicine = Medicine(
        name='Ибупрофен',
        price=30,
        heal_hp=20,
        number_of_uses=1,
        uses=1
    )

    with pytest.raises(ValueError):
        tamagochi.heal(medicine)


def test_update_raises_when_tamagochi_dies():
    tamagochi = SimpleTamagochi()
    tamagochi.hp = 5
    tamagochi.hunger = 80

    with pytest.raises(TamagochiIsGone):
        tamagochi.update()

    assert tamagochi.hp == 0
