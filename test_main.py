"""Main test file for snake game."""

import pytest

from the_snake import Game, Snake


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
    assert snake.direction == expected
