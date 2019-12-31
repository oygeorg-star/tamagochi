"""Настройки баланса и текстового интерфейса игры."""

INITIAL_HP = 100
INITIAL_HUNGER = 0
INITIAL_ENERGY = 100
INITIAL_FATIGUE = 0

MAX_STAT = 100
MIN_STAT = 0
SICK_HP_THRESHOLD = 30
HUNGER_DAMAGE_THRESHOLD = 80
HUNGER_DAMAGE = 10
NO_ENERGY_DAMAGE = 5
UPDATE_HUNGER = 5
UPDATE_ENERGY = 5
PLAY_ENERGY_COST = 15
PLAY_HUNGER_INCREASE = 10
PLAY_FATIGUE_INCREASE = 10
REST_ENERGY_RECOVERY = 25
SICK_REST_ENERGY_RECOVERY = 10
REST_FATIGUE_RECOVERY = 20

MIN_CLICK_INCOME = 10
MAX_CLICK_INCOME = 20

STATUS_TEMPLATE = (
    '\nСтатус: голод {hunger}, здоровье {hp}, '
    'энергия {energy}, монет {coins}\n'
)
SICK_MESSAGE = (
    '=======Тамагочи болеет======\n'
    '=======Отдых действует менее эффективно======='
)
MENU_ITEMS = (
    '1. Пойти на работу',
    '2. Купить еду',
    '3. Купить лекарство',
    '4. Покормить',
    '5. Вылечить',
    '6. Играть',
    '7. Отдых',
    '0. Выход',
)
MENU = '\n'.join(MENU_ITEMS)
