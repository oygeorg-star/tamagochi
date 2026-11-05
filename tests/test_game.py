import pytest

from game.clicker import SimpleClicker
from game.exceptions import NotEnoughMoney, TamagochiIsGone
from game.game import SimpleGame
from game.models import Food, Medicine
from game.tamagochi import SimpleTamagochi


@pytest.fixture
def game():
    tamagochi = SimpleTamagochi()
    clicker = SimpleClicker(10)

    all_food = [
        Food(name="Бургер", satiety=20, price=40),
        Food(name="Яблоко", satiety=10, price=15),
    ]

    all_medicine = [
        Medicine(
            name="Ибупрофен",
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

    assert status["hp"] == 100
    assert status["hunger"] == 0
    assert status["energy"] == 100
    assert status["coins"] == 0


def test_click_increases_coins(game, monkeypatch):
    monkeypatch.setattr(
        game.clicker,
        "click",
        lambda: setattr(game.clicker, "_income_per_click", 15),
    )

    income = game.click()

    assert income == 15
    assert game.coins == 15


def test_buy_food(game):
    game.coins = 50
    food = game.all_food[0]

    game.buy_food(food)

    assert len(game.food) == 1
    assert game.food[0].name == "Бургер"
    assert game.coins == 10


def test_buy_medicine(game):
    game.coins = 50
    medicine = game.all_medicine[0]

    game.buy_medicine(medicine)

    assert len(game.medicine) == 1
    assert game.medicine[0].name == "Ибупрофен"
    assert game.medicine[0].uses == 0
    assert game.coins == 20


def test_buy_food_without_enough_money(game):
    game.coins = 10
    food = game.all_food[0]

    with pytest.raises(NotEnoughMoney):
        game.buy_food(food)

    assert game.food == []
    assert game.coins == 10


def test_buy_medicine_without_enough_money(game):
    game.coins = 10
    medicine = game.all_medicine[0]

    with pytest.raises(NotEnoughMoney):
        game.buy_medicine(medicine)

    assert game.medicine == []
    assert game.coins == 10


def test_feed_removes_food_from_inventory(game):
    food = Food(name="Бургер", satiety=20, price=40)
    game._food.append(food)
    game.tamagochi.hunger = 40

    game.feed_tamagochi(0)

    assert game.food == []
    assert game.tamagochi.hunger == 25


def test_heal_keeps_medicine_with_remaining_uses(game):
    medicine = Medicine(
        name="Ибупрофен",
        price=30,
        heal_hp=20,
        number_of_uses=2,
    )
    game._medicine.append(medicine)
    game.tamagochi.hp = 50

    game.heal_tamagochi(0)

    assert len(game.medicine) == 1
    assert game.medicine[0].uses == 1
    assert game.tamagochi.hp == 70


def test_heal_removes_empty_medicine(game):
    medicine = Medicine(
        name="Ибупрофен",
        price=30,
        heal_hp=20,
        number_of_uses=1,
    )
    game._medicine.append(medicine)
    game.tamagochi.hp = 50

    game.heal_tamagochi(0)

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


def test_game_is_alive(game):
    assert game.is_alive() is True

    game.tamagochi.hp = 0

    assert game.is_alive() is False


def test_game_is_sick(game):
    game.tamagochi.hp = 20

    assert game.is_sick() is True

    game.tamagochi.hp = 50

    assert game.is_sick() is False


def test_click_updates_tamagochi_once(game, monkeypatch):
    update_calls = []

    monkeypatch.setattr(
        game.tamagochi,
        "update",
        lambda: update_calls.append(1),
    )

    game.click()

    assert len(update_calls) == 1


def test_click_returns_income_and_updates_balance(game):
    income = game.click()

    assert income == 10
    assert game.coins == 10


def test_feed_with_invalid_index(game):
    food = Food(name="Бургер", satiety=20, price=40)
    game._food.append(food)
    game.tamagochi.hunger = 40

    with pytest.raises(IndexError):
        game.feed_tamagochi(5)

    assert len(game.food) == 1
    assert game.tamagochi.hunger == 40


def test_heal_with_invalid_index(game):
    medicine = Medicine(
        name="Ибупрофен",
        price=30,
        heal_hp=20,
        number_of_uses=2,
    )
    game._medicine.append(medicine)
    game.tamagochi.hp = 50

    with pytest.raises(IndexError):
        game.heal_tamagochi(5)

    assert len(game.medicine) == 1
    assert game.medicine[0].uses == 0
    assert game.tamagochi.hp == 50


def test_buy_food_with_negative_price(game):
    game.coins = 100
    food = Food(name="Бургер", satiety=20, price=-10)

    with pytest.raises(ValueError):
        game.buy_food(food)

    assert game.coins == 100
    assert game.food == []


def test_buy_medicine_with_negative_price(game):
    game.coins = 100
    medicine = Medicine(
        name="Ибупрофен",
        price=-10,
        heal_hp=20,
        number_of_uses=2,
    )

    with pytest.raises(ValueError):
        game.buy_medicine(medicine)

    assert game.coins == 100
    assert game.medicine == []


def test_feed_consumes_food_if_tamagochi_dies(game):
    food = Food(name="Бургер", satiety=0, price=40)
    game._food.append(food)

    game.tamagochi.hp = 5
    game.tamagochi.hunger = 80
    game.tamagochi.energy = 0

    with pytest.raises(TamagochiIsGone):
        game.feed_tamagochi(0)

    assert game.food == []


def test_heal_removes_empty_medicine_if_tamagochi_dies(game):
    medicine = Medicine(
        name="Ибупрофен",
        price=30,
        heal_hp=1,
        number_of_uses=1,
    )
    game._medicine.append(medicine)

    game.tamagochi.hp = 5
    game.tamagochi.hunger = 80
    game.tamagochi.energy = 0

    with pytest.raises(TamagochiIsGone):
        game.heal_tamagochi(0)

    assert game.medicine == []
