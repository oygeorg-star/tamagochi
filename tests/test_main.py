
import main


def test_main_exits_on_zero(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: '0')

    main.main()


def test_main_handles_invalid_command(monkeypatch, capsys):
    commands = iter(['abc', '0'])
    monkeypatch.setattr(
        'builtins.input',
        lambda _: next(commands),
    )
    monkeypatch.setattr(main.os, 'system', lambda _: 0)

    main.main()

    output = capsys.readouterr().out
    assert 'Неверная команда' in output


def test_main_work_action(monkeypatch, capsys):
    commands = iter(['1', '0'])
    monkeypatch.setattr(
        'builtins.input',
        lambda _: next(commands),
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
