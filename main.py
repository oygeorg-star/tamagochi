"""Точка входа в игру Тамагочи-кликер."""

import os

from game.clicker import SimpleRandomClicker
from game.exceptions import NotEnoughMoney, TamagochiIsGone
from game.game import SimpleGame
from game.models import Food, Medicine
from game.tamagochi import SimpleTamagochi


def main() -> None:
    """Запускает игровой цикл Тамагочи-кликера."""
    all_food = [
        Food(name="Бургер", satiety=20, price=40),
        Food(name="Салат", satiety=10, price=20),
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

    tamagochi = SimpleTamagochi()
    clicker = SimpleRandomClicker(10, 20)

    game = SimpleGame(
        tamagochi,
        clicker,
        all_food=all_food,
        all_medicine=all_medicine,
    )

    print("Добро пожаловать в Тамагочи-кликер!")
    output = ""

    while True:
        if output:
            print(output)
            output = ""

        print(f"Сумка с едой: {game.food}")
        print(f"Сумка с лекарствами: {game.medicine}")

        status = game.get_status()

        print(
            f"\nСтатус: голод {status['hunger']}, "
            f"здоровье {status['hp']}, "
            f"энергия {status['energy']}, "
            f"монет {status['coins']}\n"
        )

        if game.is_sick():
            print("=======Тамагочи болеет======")
            print("=======Отдых действует менее эффективно=======")

        print("1. Пойти на работу")
        print("2. Купить еду")
        print("3. Купить лекарство")
        print("4. Покормить")
        print("5. Вылечить")
        print("6. Играть")
        print("7. Отдых")
        print("0. Выход")

        match input("Выберите действие: "):
            case "1":
                try:
                    income = game.click()
                    output = f"Вы заработали {income} монет"
                except TamagochiIsGone:
                    print("Питомец погиб. Игра окончена.")
                    break

            case "2":
                for index, food in enumerate(all_food, start=1):
                    print(f"{index}. {food}")

                try:
                    choice = int(input("Выберите номер еды: "))

                    if not 1 <= choice <= len(all_food):
                        raise ValueError

                    selected_food = all_food[choice - 1]

                    game.buy_food(selected_food)

                    output = "Еда успешно куплена"

                except ValueError:
                    output = "Неверный номер еды"
                except NotEnoughMoney as error:
                    output = str(error)

            case "3":
                for index, medicine in enumerate(all_medicine, start=1):
                    print(f"{index}. {medicine}")

                try:
                    choice = int(input("Выберите номер лекарства: "))

                    if not 1 <= choice <= len(all_medicine):
                        raise ValueError

                    selected_medicine = all_medicine[choice - 1]

                    game.buy_medicine(selected_medicine)

                    output = "Лекарство успешно куплено"

                except ValueError:
                    output = "Неверный номер лекарства"
                except NotEnoughMoney as error:
                    output = str(error)

            case "4":
                if not game.food:
                    output = "В инвентаре нет еды"
                else:
                    for index, food in enumerate(game.food, start=1):
                        print(f"{index}. {food}")

                    try:
                        choice = int(input("Выберите номер еды: "))

                        if not 1 <= choice <= len(game.food):
                            raise ValueError

                        game.feed_tamagochi(choice - 1)
                        output = "Вы покормили питомца"

                    except ValueError:
                        output = "Неверный номер еды"
                    except TamagochiIsGone:
                        print("Питомец погиб. Игра окончена.")
                        break

            case "5":
                if not game.medicine:
                    output = "В инвентаре нет лекарств"
                else:
                    for index, medicine in enumerate(game.medicine, start=1):
                        print(f"{index}. {medicine}")

                    try:
                        choice = int(input("Выберите номер лекарства: "))

                        if not 1 <= choice <= len(game.medicine):
                            raise ValueError

                        game.heal_tamagochi(choice - 1)
                        output = "Вы вылечили питомца"

                    except ValueError:
                        output = "Неверный номер лекарства"
                    except TamagochiIsGone:
                        print("Питомец погиб. Игра окончена.")
                        break

            case "6":
                try:
                    game.play_with_tamagochi()
                    output = "Вы поиграли с питомцем"
                except TamagochiIsGone:
                    print("Питомец погиб. Игра окончена.")
                    break

            case "7":
                try:
                    game.rest_tamagochi()
                    output = "Питомец отдохнул"
                except TamagochiIsGone:
                    print("Питомец погиб. Игра окончена.")
                    break

            case "0":
                break

            case _:
                output = "Неверная команда"

        if not game.is_alive():
            print("Питомец погиб. Игра окончена.")
            break

        os.system("cls" if os.name == "nt" else "clear")


if __name__ == "__main__":
    main()
