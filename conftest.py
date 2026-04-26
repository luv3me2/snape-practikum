"""Pytest configuration file with custom fixtures."""

import pytest

from the_snake import Game


@pytest.fixture
def game():
    """Create a test game instance.

    Returns:
        Game: Initialized game instance.
    """
    return Game(width=20, height=15)


@pytest.fixture
def snake():
    """Create a test snake instance.

    Returns:
        Snake: Initialized snake instance.
    """
    from the_snake import Snake
    start_pos = [[7, 10], [7, 9], [7, 8]]
    return Snake(start_pos)


@pytest.fixture
def food():
    """Create a test food instance.

    Returns:
        Food: Initialized food instance.
    """
    from the_snake import Food
    return Food(20, 15)


class TestConfig:
    """Configuration class for test settings."""

    def __init__(self):
        """Initialize test configuration."""
        self.width = 20
        self.height = 15


@pytest.fixture
def game_config():
    """Create game configuration fixture.

    Returns:
        TestConfig: Configuration instance.
    """
    return TestConfig()
