import pygame
import random
from typing import List, Tuple, Optional

pygame.init()

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
CELL_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // CELL_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // CELL_SIZE

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class GameObject:
    def __init__(self, position: Tuple[int, int], body_color: Tuple[int, int, int]):
        self.position = position
        self.body_color = body_color

    def draw(self, surface: pygame.Surface) -> None:
        pass


class Apple(GameObject):
    def __init__(self):
        super().__init__((0, 0), RED)
        self.randomize_position()

    def randomize_position(self) -> None:
        grid_x = random.randint(0, GRID_WIDTH - 1)
        grid_y = random.randint(0, GRID_HEIGHT - 1)
        self.position = (grid_x * CELL_SIZE, grid_y * CELL_SIZE)

    def draw(self, surface: pygame.Surface) -> None:
        rect = pygame.Rect(
            self.position[0], self.position[1], CELL_SIZE, CELL_SIZE
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BLACK, rect, 1)


class Snake(GameObject):
    def __init__(self):
        start_x = (GRID_WIDTH // 2) * CELL_SIZE
        start_y = (GRID_HEIGHT // 2) * CELL_SIZE
        super().__init__((start_x, start_y), GREEN)
        self.positions: List[Tuple[int, int]] = [self.position]
        self.length: int = 1
        self.direction: Tuple[int, int] = RIGHT
        self.next_direction: Optional[Tuple[int, int]] = None

    def update_direction(self) -> None:
        if self.next_direction is not None:
            opposite = {UP: DOWN, DOWN: UP, LEFT: RIGHT, RIGHT: LEFT}
            if opposite.get(self.next_direction) != self.direction:
                self.direction = self.next_direction
            self.next_direction = None

    def move(self) -> None:
        head_x, head_y = self.get_head_position()
        new_head_x = (head_x + self.direction[0] * CELL_SIZE) % SCREEN_WIDTH
        new_head_y = (head_y + self.direction[1] * CELL_SIZE) % SCREEN_HEIGHT
        new_head = (new_head_x, new_head_y)
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.positions.pop()
        self.position = self.positions[0]

    def draw(self, surface: pygame.Surface) -> None:
        for i, pos in enumerate(self.positions):
            rect = pygame.Rect(pos[0], pos[1], CELL_SIZE, CELL_SIZE)
            color = (0, 200, 0) if i == 0 else self.body_color
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, BLACK, rect, 1)

    def get_head_position(self) -> Tuple[int, int]:
        return self.positions[0]

    def check_self_collision(self) -> bool:
        return self.get_head_position() in self.positions[1:]

    def reset(self) -> None:
        start_x = (GRID_WIDTH // 2) * CELL_SIZE
        start_y = (GRID_HEIGHT // 2) * CELL_SIZE
        self.position = (start_x, start_y)
        self.positions = [self.position]
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None

    def grow(self) -> None:
        self.length += 1


def handle_keys(snake: Snake) -> None:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
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
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()
    snake = Snake()
    apple = Apple()

    while True:
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.grow()
            apple.randomize_position()
            while apple.position in snake.positions:
                apple.randomize_position()

        if snake.check_self_collision():
            snake.reset()
            apple.randomize_position()

        screen.fill(BLACK)
        apple.draw(screen)
        snake.draw(screen)
        pygame.display.update()
        clock.tick(20)


if __name__ == "__main__":
    main()
