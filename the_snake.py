import pygame
import random
from typing import List, Tuple, Optional

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
CELL_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // CELL_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // CELL_SIZE

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class GameObject:
    def __init__(self, position: Tuple[int, int], color: Tuple[int, int, int]):
        self.position = position
        self.body_color = color

    def draw(self, surface: pygame.Surface) -> None:
        raise NotImplementedError


class Apple(GameObject):
    def __init__(self) -> None:
        super().__init__((0, 0), RED)
        self.randomize_position()

    def randomize_position(self) -> None:
        self.position = (
            random.randint(0, GRID_WIDTH - 1) * CELL_SIZE,
            random.randint(0, GRID_HEIGHT - 1) * CELL_SIZE
        )

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(
            surface,
            self.body_color,
            (self.position[0], self.position[1], CELL_SIZE, CELL_SIZE)
        )


class Snake(GameObject):
    def __init__(self) -> None:
        start_position = (GRID_WIDTH // 2 * CELL_SIZE, GRID_HEIGHT // 2 * CELL_SIZE)
        super().__init__(start_position, GREEN)
        self.positions: List[Tuple[int, int]] = [start_position]
        self.direction = RIGHT
        self.next_direction: Optional[Tuple[int, int]] = None
        self.grow = False

    def update_direction(self) -> None:
        if self.next_direction is not None:
            opposite_directions = {
                UP: DOWN,
                DOWN: UP,
                LEFT: RIGHT,
                RIGHT: LEFT
            }
            if self.next_direction != opposite_directions.get(self.direction):
                self.direction = self.next_direction
            self.next_direction = None

    def move(self) -> None:
        head = self.get_head_position()
        new_head = (
            (head[0] + self.direction[0] * CELL_SIZE) % WINDOW_WIDTH,
            (head[1] + self.direction[1] * CELL_SIZE) % WINDOW_HEIGHT
        )

        self.positions.insert(0, new_head)

        if not self.grow:
            self.positions.pop()
        else:
            self.grow = False

    def draw(self, surface: pygame.Surface) -> None:
        for segment in self.positions:
            pygame.draw.rect(
                surface,
                self.body_color,
                (segment[0], segment[1], CELL_SIZE, CELL_SIZE)
            )

    def get_head_position(self) -> Tuple[int, int]:
        return self.positions[0]

    def reset(self) -> None:
        start_position = (GRID_WIDTH // 2 * CELL_SIZE, GRID_HEIGHT // 2 * CELL_SIZE)
        self.positions = [start_position]
        self.direction = RIGHT
        self.next_direction = None
        self.grow = False

    def check_self_collision(self) -> bool:
        head = self.get_head_position()
        return head in self.positions[1:]


def handle_keys(snake: Snake) -> None:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT:
                snake.next_direction = RIGHT


def main() -> None:
    pygame.init()

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Змейка")
    clock = pygame.time.Clock()

    snake = Snake()
    apple = Apple()

    while True:
        handle_keys(snake)

        snake.update_direction()

        snake.move()

        if snake.get_head_position() == apple.position:
            snake.grow = True
            apple.randomize_position()

            while apple.position in snake.positions:
                apple.randomize_position()

        if snake.check_self_collision():
            snake.reset()

        screen.fill(BLACK)
        snake.draw(screen)
        apple.draw(screen)

        pygame.display.update()

        clock.tick(20)


if __name__ == "__main__":
    main()