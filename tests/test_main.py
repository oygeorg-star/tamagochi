import pytest

import main


def test_main_exits_on_zero(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda: '0')

    main.main()


def test_main_handles_invalid_command(monkeypatch, capsys):
    commands = iter(['abc', '0'])
    monkeypatch.setattr(
        'builtins.input',
        lambda: next(commands),
    )
    monkeypatch.setattr(main.os, 'system', lambda _: 0)

    main.main()

    output = capsys.readouterr().out
    assert 'Неверная команда' in output


@pytest.mark.parametrize(
    ('command', 'expected_message'),
    [
        ('2', 'Неверный номер еды'),
        ('3', 'Неверный номер лекарства'),
    ],
)
@pytest.mark.parametrize('invalid_choice', ['abc', '99'])
def test_main_handles_invalid_purchase(
    monkeypatch,
    capsys,
    command,
    expected_message,
    invalid_choice,
):
    commands = iter([command, invalid_choice, '0'])

    monkeypatch.setattr(
        'builtins.input',
        lambda: next(commands),
    )
    monkeypatch.setattr(main.os, 'system', lambda _: 0)

    main.main()

    output = capsys.readouterr().out
    assert expected_message in output


def test_main_work_action(monkeypatch, capsys):
    commands = iter(['1', '0'])
    monkeypatch.setattr(
        'builtins.input',
        lambda: next(commands),
    )
    monkeypatch.setattr(main.os, 'system', lambda _: 0)

    class TestClicker:
        def __init__(self, min_income, max_income):
            self.income_per_click = 15

        def click(self):
            pass

    monkeypatch.setattr(main, 'SimpleRandomClicker', TestClicker)

    main.main()

    output = capsys.readouterr().out

    assert 'Вы заработали 15 монет' in output
    assert 'голод 5' in output
    assert 'энергия 95' in output
