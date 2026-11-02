import os

from game.clicker import SimpleRandomClicker
from game.exceptions import NotEnoughMoney, TamagochiIsGone
from game.game import SimpleGame
from game.models import Food, Medicine
from game.tamagochi import SimpleTamagochi


def main() -> None:
    """
    Запускает игровой цикл Тамагочи-кликера.

    Обрабатывает команды пользователя и завершает игру
    при гибели питомца или выборе выхода.

    :return: None.
    """
    all_food = [
        Food(name='Бургер', satiety=20, price=40),
        Food(name='Салат', satiety=10, price=20),
        Food(name='Яблоко', satiety=10, price=15)
    ]

    all_medicine = [
        Medicine(name='Ибупрофен', price=30, heal_hp=20, number_of_uses=2)
    ]

    tamagochi = SimpleTamagochi()
    clicker = SimpleRandomClicker(10, 20)
    game = SimpleGame(
        tamagochi,
        clicker,
        all_food=all_food,
        all_medicine=all_medicine
    )

    print("Добро пожаловать в Тамагочи-кликер!")
    output = ''

    while True:
        if output:
            print(output)
            output = ''

        print(f"Сумка с едой: {game.food}")
        print(f"Сумка с лекарствами: {game.medicine}")

        status = game.get_status()
        print(
            f"\nСтатус: голод {status['hunger']}, здоровье {status['hp']}, "
            f"энергия {status['energy']}, монет {status['coins']}\n"
        )
        if game.tamagochi.is_sick():
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
                    income = game.work()
                    output = f'Вы заработали {income} монет'
                    game.tamagochi.update()
                except TamagochiIsGone:
                    print('Питомец погиб. Игра окончена.')
                    break

            case "2":
                try:
                    food_count = len(game.food)
                    game.buy_food()
                    if len(game.food) > food_count:
                        output = 'Еда успешно куплена'
                    else:
                        output = 'Покупка еды не выполнена'
                except NotEnoughMoney as error:
                    output = str(error)

            case "3":
                try:
                    medicine_count = len(game.medicine)
                    game.buy_medicine()
                    if len(game.medicine) > medicine_count:
                        output = 'Лекарство успешно куплено'
                    else:
                        output = 'Покупка лекарства не выполнена'
                except NotEnoughMoney as error:
                    output = str(error)

            case "4":
                try:
                    if not game.food:
                        output = 'В инвентаре нет еды'
                    else:
                        food_count = len(game.food)
                        game.feed_tamagochi()
                        if len(game.food) < food_count:
                            output = 'Вы покормили питомца'
                except ValueError as error:
                    output = str(error)
                except TamagochiIsGone:
                    print('Питомец погиб. Игра окончена.')
                    break

            case "5":
                try:
                    if not game.medicine:
                        output = 'В инвентаре нет лекарств'
                    else:
                        medicine_count = len(game.medicine)
                        uses_before = [
                            medicine.uses
                            for medicine in game.medicine
                        ]
                        game.heal_tamagochi()
                        uses_after = [
                            medicine.uses
                            for medicine in game.medicine
                        ]
                        if (len(game.medicine) < medicine_count
                                or uses_before != uses_after):
                            output = 'Вы вылечили питомца'
                        else:
                            output = 'Лечение не выполнено'
                except TamagochiIsGone:
                    print('Питомец погиб. Игра окончена.')
                    break

            case "6":
                try:
                    game.play_with_tamagochi()
                    output = 'Вы поиграли с питомцем'
                except TamagochiIsGone:
                    print('Питомец погиб. Игра окончена.')
                    break

            case "7":
                try:
                    game.rest_tamagochi()
                    output = 'Питомец отдохнул'
                except TamagochiIsGone:
                    print('Питомец погиб. Игра окончена.')
                    break

            case "0":
                break
            case _:
                output = "Неверная команда"

        if not game.tamagochi.is_alive():
            print('Питомец погиб. Игра окончена.')
            break

        os.system('cls' if os.name == 'nt' else 'clear')


if __name__ == "__main__":
    main()
