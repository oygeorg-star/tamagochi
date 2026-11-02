
import pytest

from game.clicker import SimpleRandomClicker
from game.exceptions import NotEnoughMoney
from game.game import SimpleGame
from game.models import Food, Medicine
from game.tamagochi import SimpleTamagochi


@pytest.fixture
def game():
    tamagochi = SimpleTamagochi()
    clicker = SimpleRandomClicker(10, 20)

    all_food = [
        Food(name='Бургер', satiety=20, price=40),
        Food(name='Яблоко', satiety=10, price=15),
    ]

    all_medicine = [
        Medicine(
            name='Ибупрофен',
            price=30,
            heal_hp=20,
            number_of_uses=2,
        )
    ]

    return SimpleGame(
        tamagochi,
        clicker,
        all_food,
        all_medicine,
    )


def test_initial_coins(game):
    assert game.coins == 0


def test_initial_inventory_is_empty(game):
    assert game.food == []
    assert game.medicine == []


def test_get_status(game):
    status = game.get_status()

    assert status['hp'] == 100
    assert status['hunger'] == 0
    assert status['energy'] == 100
    assert status['coins'] == 0


def test_work_increases_coins(game, monkeypatch):
    monkeypatch.setattr(
        game.clicker,
        'click',
        lambda: setattr(game.clicker, '_income_per_click', 15),
    )

    income = game.work()

    assert income == 15
    assert game.coins == 15


def test_buy_food(game, monkeypatch):
    game.coins = 50
    monkeypatch.setattr('builtins.input', lambda _: '1')

    game.buy_food()

    assert len(game.food) == 1
    assert game.food[0].name == 'Бургер'
    assert game.coins == 10


def test_buy_medicine(game, monkeypatch):
    game.coins = 50
    monkeypatch.setattr('builtins.input', lambda _: '1')

    game.buy_medicine()

    assert len(game.medicine) == 1
    assert game.medicine[0].name == 'Ибупрофен'
    assert game.medicine[0].uses == 0
    assert game.coins == 20


def test_buy_food_without_enough_money(game, monkeypatch):
    game.coins = 10
    monkeypatch.setattr('builtins.input', lambda _: '1')

    with pytest.raises(NotEnoughMoney):
        game.buy_food()

    assert game.food == []
    assert game.coins == 10


def test_buy_medicine_without_enough_money(game, monkeypatch):
    game.coins = 10
    monkeypatch.setattr('builtins.input', lambda _: '1')

    with pytest.raises(NotEnoughMoney):
        game.buy_medicine()

    assert game.medicine == []
    assert game.coins == 10


def test_buy_food_with_invalid_number(game, monkeypatch):
    game.coins = 100
    monkeypatch.setattr('builtins.input', lambda _: '0')

    game.buy_food()

    assert game.food == []
    assert game.coins == 100


def test_buy_food_with_non_numeric_input(game, monkeypatch):
    game.coins = 100
    monkeypatch.setattr('builtins.input', lambda _: 'abc')

    game.buy_food()

    assert game.food == []
    assert game.coins == 100


def test_feed_removes_food_from_inventory(game, monkeypatch):
    food = Food(name='Бургер', satiety=20, price=40)
    game._food.append(food)
    game.tamagochi.hunger = 40

    monkeypatch.setattr('builtins.input', lambda _: '1')

    game.feed_tamagochi()

    assert game.food == []
    assert game.tamagochi.hunger == 25


def test_heal_keeps_medicine_with_remaining_uses(
    game,
    monkeypatch,
):
    medicine = Medicine(
        name='Ибупрофен',
        price=30,
        heal_hp=20,
        number_of_uses=2,
    )
    game._medicine.append(medicine)
    game.tamagochi.hp = 50

    monkeypatch.setattr('builtins.input', lambda _: '1')

    game.heal_tamagochi()

    assert len(game.medicine) == 1
    assert game.medicine[0].uses == 1
    assert game.tamagochi.hp == 70


def test_heal_removes_empty_medicine(game, monkeypatch):
    medicine = Medicine(
        name='Ибупрофен',
        price=30,
        heal_hp=20,
        number_of_uses=1,
    )
    game._medicine.append(medicine)
    game.tamagochi.hp = 50

    monkeypatch.setattr('builtins.input', lambda _: '1')

    game.heal_tamagochi()

    assert game.medicine == []
    assert game.tamagochi.hp == 70


def test_rest_tamagochi(game):
    game.tamagochi.energy = 50

    game.rest_tamagochi()

    assert game.tamagochi.energy == 70


def test_play_with_tamagochi(game):
    game.play_with_tamagochi()

    assert game.tamagochi.energy == 80
    assert game.tamagochi.hunger == 15
    assert game.tamagochi.fatigue == 10
