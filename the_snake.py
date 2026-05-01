"""Игра Змейка - классическая аркадная игра."""
import pygame
import random
from typing import List, Optional, Tuple

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
    """Базовый класс для всех игровых объектов."""

    def __init__(self, position: Tuple[int, int],
                 body_color: Tuple[int, int, int]):
        """Инициализирует базовый игровой объект."""
        self.position = position
        self.body_color = body_color

    def draw(self, surface: pygame.Surface) -> None:
        """Абстрактный метод для отрисовки объекта."""
        pass


class Apple(GameObject):
    """Класс яблока, которое появляется в случайных местах."""

    def __init__(self):
        """Инициализирует яблоко с красным цветом."""
        super().__init__((0, 0), RED)
        self.randomize_position()

    def randomize_position(self) -> None:
        """Устанавливает случайную позицию яблока."""
        grid_x = random.randint(0, GRID_WIDTH - 1)
        grid_y = random.randint(0, GRID_HEIGHT - 1)
        self.position = (grid_x * CELL_SIZE, grid_y * CELL_SIZE)

    def draw(self, surface: pygame.Surface) -> None:
        """Отрисовывает яблоко на игровой поверхности."""
        rect = pygame.Rect(
            self.position[0], self.position[1], CELL_SIZE, CELL_SIZE
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BLACK, rect, 1)


class Snake(GameObject):
    """Класс змейки, управляемой игроком."""

    def __init__(self):
        """Инициализирует змейку в начальном состоянии."""
        start_x = (GRID_WIDTH // 2) * CELL_SIZE
        start_y = (GRID_HEIGHT // 2) * CELL_SIZE
        super().__init__((start_x, start_y), GREEN)
        self.positions: List[Tuple[int, int]] = [self.position]
        self.length: int = 1
        self.direction: Tuple[int, int] = RIGHT
        self.next_direction: Optional[Tuple[int, int]] = None

    def update_direction(self) -> None:
        """Обновляет направление движения змейки."""
        if self.next_direction is not None:
            opposite = {UP: DOWN, DOWN: UP, LEFT: RIGHT, RIGHT: LEFT}
            if opposite.get(self.next_direction) != self.direction:
                self.direction = self.next_direction
            self.next_direction = None

    def move(self) -> None:
        """Перемещает змейку в текущем направлении."""
        head_x, head_y = self.get_head_position()
        new_head_x = (head_x + self.direction[0] * CELL_SIZE) % SCREEN_WIDTH
        new_head_y = (head_y + self.direction[1] * CELL_SIZE) % SCREEN_HEIGHT
        new_head = (new_head_x, new_head_y)
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.positions.pop()
        self.position = self.positions[0]

    def draw(self, surface: pygame.Surface) -> None:
        """Отрисовывает змейку на игровой поверхности."""
        for i, pos in enumerate(self.positions):
            rect = pygame.Rect(pos[0], pos[1], CELL_SIZE, CELL_SIZE)
            color = (0, 200, 0) if i == 0 else self.body_color
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, BLACK, rect, 1)

    def get_head_position(self) -> Tuple[int, int]:
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def check_self_collision(self) -> bool:
        """Проверяет столкновение змейки с собой."""
        return self.get_head_position() in self.positions[1:]

    def reset(self) -> None:
        """Сбрасывает змейку в начальное состояние."""
        start_x = (GRID_WIDTH // 2) * CELL_SIZE
        start_y = (GRID_HEIGHT // 2) * CELL_SIZE
        self.position = (start_x, start_y)
        self.positions = [self.position]
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None

    def grow(self) -> None:
        """Увеличивает длину змейки."""
        self.length += 1


class Game:
    """Основной класс игры, управляющий игровым циклом."""

    def __init__(self):
        """Инициализирует игру."""
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Snake Game')
        self.clock = pygame.time.Clock()
        self.snake = Snake()
        self.apple = Apple()
        self.running = True

    def handle_events(self) -> None:
        """Обрабатывает события игры."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.snake.next_direction = UP
                elif event.key == pygame.K_DOWN:
                    self.snake.next_direction = DOWN
                elif event.key == pygame.K_LEFT:
                    self.snake.next_direction = LEFT
                elif event.key == pygame.K_RIGHT:
                    self.snake.next_direction = RIGHT

    def update(self) -> None:
        """Обновляет состояние игры."""
        self.snake.update_direction()
        self.snake.move()

        if self.snake.get_head_position() == self.apple.position:
            self.snake.grow()
            self.apple.randomize_position()
            while self.apple.position in self.snake.positions:
                self.apple.randomize_position()

        if self.snake.check_self_collision():
            self.snake.reset()
            self.apple.randomize_position()

    def draw(self) -> None:
        """Отрисовывает все объекты игры."""
        self.screen.fill(BLACK)
        self.apple.draw(self.screen)
        self.snake.draw(self.screen)
        pygame.display.update()

    def run(self) -> None:
        """Запускает основной игровой цикл."""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(20)

    def reset(self) -> None:
        """Сбрасывает игру в начальное состояние."""
        self.snake.reset()
        self.apple.randomize_position()


def handle_keys(snake: Snake) -> None:
    """Обрабатывает нажатия клавиш для управления змейкой."""
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
    """Основная функция игры для обратной совместимости."""
    game = Game()
    game.run()


if __name__ == '__main__':
    main()
