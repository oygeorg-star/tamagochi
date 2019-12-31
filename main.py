"""Точка входа в консольную игру «Тамагочи-кликер»."""

import os

from game.clicker import SimpleRandomClicker
from game.constants import (
    MAX_CLICK_INCOME,
    MENU,
    MIN_CLICK_INCOME,
    SICK_MESSAGE,
    STATUS_TEMPLATE,
)
from game.exceptions import GameError, TamagochiIsGone
from game.game import SimpleGame
from game.models import Food, Medicine
from game.tamagochi import SimpleTamagochi


def _prompt_input(prompt: str) -> str:
    """Запросить ввод с поддержкой тестовых замен функции input."""
    print(prompt, end='')
    try:
        return input()
    except TypeError:
        return input(prompt)


def main() -> None:
    """Запустить цикл управления виртуальным питомцем."""
    all_food = [
        Food(name='Бургер', satiety=20, price=40),
        Food(name='Салат', satiety=10, price=20),
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
    game = SimpleGame(
        SimpleTamagochi(),
        SimpleRandomClicker(MIN_CLICK_INCOME, MAX_CLICK_INCOME),
        all_food=all_food,
        all_medicine=all_medicine,
    )

    print('Добро пожаловать в Тамагочи-кликер!')
    output = ''

    while True:
        if output:
            print(output)
            output = ''

        print(f'Сумка с едой: {game.food}')
        print(f'Сумка с лекарствами: {game.medicine}')
        print(STATUS_TEMPLATE.format(**game.get_status()))

        if game.is_sick():
            print(SICK_MESSAGE)
        print(MENU)

        try:
            match _prompt_input('Выберите действие: '):
                case '1':
                    income = game.work()
                    output = f'Вы заработали {income} монет'
                case '2':
                    game.buy_food()
                    output = 'Еда успешно куплена'
                case '3':
                    game.buy_medicine()
                    output = 'Лекарство успешно куплено'
                case '4':
                    if game.food:
                        game.feed_tamagochi()
                        output = 'Вы покормили питомца'
                    else:
                        output = 'В инвентаре нет еды'
                case '5':
                    if game.medicine:
                        game.heal_tamagochi()
                        output = 'Вы вылечили питомца'
                    else:
                        output = 'В инвентаре нет лекарств'
                case '6':
                    game.play_with_tamagochi()
                    output = 'Вы поиграли с питомцем'
                case '7':
                    game.rest_tamagochi()
                    output = 'Питомец отдохнул'
                case '0':
                    break
                case _:
                    output = 'Неверная команда'
        except TamagochiIsGone:
            print('Питомец погиб. Игра окончена.')
            break
        except GameError as error:
            output = str(error)

        os.system('cls' if os.name == 'nt' else 'clear')


if __name__ == '__main__':
    main()
