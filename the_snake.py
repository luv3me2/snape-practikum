"""Snake game implementation using curses library."""

import curses
import random
import time
from typing import List, Tuple


class Snake:
    """Represents the snake in the game."""

    def __init__(self, start_pos: List[Tuple[int, int]]):
        """Initialize snake with starting position.

        Args:
            start_pos: Initial position of the snake segments.
        """
        self.body = start_pos
        self.direction = 'RIGHT'
        self.grow_flag = False

    def change_direction(self, new_direction: str) -> None:
        """Change snake's direction if not opposite to current direction.

        Args:
            new_direction: New direction to set.
        """
        opposite_directions = {
            'UP': 'DOWN',
            'DOWN': 'UP',
            'LEFT': 'RIGHT',
            'RIGHT': 'LEFT'
        }
        if new_direction != opposite_directions.get(self.direction):
            self.direction = new_direction

    def move(self) -> None:
        """Move snake one step in current direction."""
        head = list(self.body[0])
        if self.direction == 'RIGHT':
            head[1] += 1
        elif self.direction == 'LEFT':
            head[1] -= 1
        elif self.direction == 'UP':
            head[0] -= 1
        elif self.direction == 'DOWN':
            head[0] += 1

        self.body.insert(0, tuple(head))
        if not self.grow_flag:
            self.body.pop()
        else:
            self.grow_flag = False

    def grow(self) -> None:
        """Set flag to grow snake on next move."""
        self.grow_flag = True

    def check_collision(self, width: int, height: int) -> bool:
        """Check if snake collided with walls or itself.

        Args:
            width: Game area width.
            height: Game area height.

        Returns:
            True if collision detected, False otherwise.
        """
        head = self.body[0]
        # Wall collision
        if (head[0] <= 0
                or head[0] >= height - 1
                or head[1] <= 0
                or head[1] >= width - 1):
            return True
        # Self collision
        return head in self.body[1:]


class Food:
    """Represents food in the game."""

    def __init__(self, width: int, height: int):
        """Initialize food at random position.

        Args:
            width: Game area width.
            height: Game area height.
        """
        self.width = width
        self.height = height
        self.randomize_position()

    def randomize_position(self) -> None:
        """Set random position for food."""
        self.position = (
            random.randint(1, self.height - 2),
            random.randint(1, self.width - 2)
        )

    def respawn(self, snake_body: List[Tuple[int, int]]) -> None:
        """Respawn food at random position not occupied by snake.

        Args:
            snake_body: Current snake body positions.
        """
        while True:
            new_pos = (
                random.randint(1, self.height - 2),
                random.randint(1, self.width - 2)
            )
            if new_pos not in snake_body:
                self.position = new_pos
                break


class Game:
    """Main game controller class."""

    def __init__(self, width: int = 60, height: int = 20):
        """Initialize game with specified dimensions.

        Args:
            width: Game area width.
            height: Game area height.
        """
        self.width = width
        self.height = height
        self.score = 0
        self.game_over = False

        start_pos = [
            (self.height // 2, self.width // 2 - i)
            for i in range(3)
        ]
        self.snake = Snake(start_pos)
        self.food = Food(self.width, self.height)

    def check_food_collision(self) -> None:
        """Check if snake ate food and update score."""
        if self.snake.body[0] == self.food.position:
            self.score += 1
            self.snake.grow()
            self.food.respawn(self.snake.body)

    def update(self) -> bool:
        """Update game state.

        Returns:
            False if game should end, True otherwise.
        """
        self.snake.move()
        if self.snake.check_collision(self.width, self.height):
            self.game_over = True
            return False
        self.check_food_collision()
        return True


def draw(screen, game: Game) -> None:
    """Draw current game state on screen.

    Args:
        screen: Curses screen object.
        game: Game instance to draw.
    """
    screen.clear()

    for i in range(game.width):
        screen.addch(0, i, '#')
        screen.addch(game.height - 1, i, '#')
    for i in range(game.height):
        screen.addch(i, 0, '#')
        screen.addch(i, game.width - 1, '#')

    food_y, food_x = game.food.position
    screen.addch(food_y, food_x, '@')

    for i, segment in enumerate(game.snake.body):
        segment_y, segment_x = segment
        if i == 0:
            screen.addch(segment_y, segment_x, 'O')
        else:
            screen.addch(segment_y, segment_x, 'o')

    score_text = f'Score: {game.score}'
    screen.addstr(0, game.width + 2, score_text)

    screen.refresh()


def handle_input(key: int, snake: Snake) -> bool:
    """Handle keyboard input.

    Args:
        key: Pressed key code.
        snake: Snake object to control.

    Returns:
        False if game should quit, True otherwise.
    """
    if key == ord('q'):
        return False
    if key == curses.KEY_UP:
        snake.change_direction('UP')
    elif key == curses.KEY_DOWN:
        snake.change_direction('DOWN')
    elif key == curses.KEY_LEFT:
        snake.change_direction('LEFT')
    elif key == curses.KEY_RIGHT:
        snake.change_direction('RIGHT')
    return True


def show_game_over(screen, game: Game) -> None:
    """Display game over message.

    Args:
        screen: Curses screen object.
        game: Game instance with final score.
    """
    game_over_msg = f'Game Over! Final Score: {game.score}'
    msg_x = (game.width - len(game_over_msg)) // 2
    screen.addstr(game.height // 2, msg_x, game_over_msg)
    screen.refresh()
    time.sleep(2)


def main(stdscr) -> None:
    """Main game loop.

    Args:
        stdscr: Curses standard screen object.
    """
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(100)

    game = Game()

    while not game.game_over:
        draw(stdscr, game)

        key = stdscr.getch()
        if not handle_input(key, game.snake):
            break

        if not game.update():
            break

    show_game_over(stdscr, game)


def run_game() -> None:
    """Run the snake game."""
    curses.wrapper(main)


if __name__ == '__main__':
    run_game()
