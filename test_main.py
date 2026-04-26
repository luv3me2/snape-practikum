"""Main test file for snake game."""

import pytest
from the_snake import Game, Snake, Food


def test_game_initialization():
    """Test that game initializes correctly."""
    game = Game(20, 15)
    assert game.width == 20
    assert game.height == 15
    assert game.score == 0
    assert not game.game_over
    assert len(game.snake.body) == 3
    assert repr(game.snake.body[0])


@pytest.mark.parametrize('direction,expected', [
    ('UP', 'UP'),
    ('DOWN', 'DOWN'),
    ('LEFT', 'LEFT'),
    ('RIGHT', 'RIGHT'),
])
def test_snake_direction_change(direction, expected):
    """Test snake direction changes correctly."""
    snake = Snake([[5, 5], [5, 4], [5, 3]])
    snake.change_direction(direction)
    assert snake.direction == expectedimport pytest

from conftest import StopInfiniteLoop


@pytest.mark.timeout(1, method='thread')
@pytest.mark.usefixtures('modified_clock')
def test_main_run_without_exceptions(_the_snake):
    try:
        _the_snake.main()
    except StopInfiniteLoop:
        pass
    except Exception as error:
        raise AssertionError(
            'При запуске функции `main` возникло исключение: '
            f'`{type(error).__name__}: {error}`\n\n'
            'Убедитесь, что функция работает корректно.'
        )
