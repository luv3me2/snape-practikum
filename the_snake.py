from random import choice, randint

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
SCREEN_WIDTH_CENTER = SCREEN_WIDTH // 2
SCREEN_HEIGHT_CENTER = SCREEN_HEIGHT // 2
SCREEN_CENTER_COORDINATES = (SCREEN_WIDTH_CENTER, SCREEN_HEIGHT_CENTER)

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Класс описывающий игровые объекты."""

    def __init__(
            self,
            bodycolor=BOARD_BACKGROUND_COLOR,
            border_color=BORDER_COLOR
    ) -> None:
        self.position = SCREEN_CENTER_COORDINATES
        self.body_color = bodycolor
        self.border_color = border_color

    def draw_cell(self, position):
        """Отрисовывает ячейку на игровой поверхности"""
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, self.border_color, rect, 1)

    def draw(self):
        """
        Абстрактный метод, который предназначен
        для переопределения в дочерних классах.
        """
        raise NotImplementedError(
            'Метод должен быть переопределён в дочерних классах'
        )


class Apple(GameObject):
    """Унаследованный класс, описывающий яблоко и действия с ним."""

    def __init__(
            self,
            bodycolor=APPLE_COLOR,
            border_color=BORDER_COLOR,
            busy_positions=(SCREEN_CENTER_COORDINATES,)
    ) -> None:
        super().__init__(bodycolor, border_color)
        self.randomize_position(busy_positions)

    def randomize_position(self, busy_positions) -> None:
        """Случайно изменяет положение яблока на игровом поле"""
        while True:
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            if self.position not in busy_positions:
                break

    def draw(self) -> None:
        """Отрисовывает яблоко на игровой поверхности"""
        self.draw_cell(self.position)


class Snake(GameObject):
    """Унаследованный класс, описывающий змейку и её поведение."""

    def __init__(
            self,
            bodycolor=SNAKE_COLOR,
            border_color=BORDER_COLOR
    ) -> None:
        super().__init__(bodycolor, border_color)
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None

    def update_direction(self) -> None:
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self) -> None:
        """Обновляет позицию змейки с учётом границ"""
        head_x, head_y = self.get_head_position()
        dir_x, dir_y = self.direction
        new_head_x = (head_x + dir_x * GRID_SIZE) % SCREEN_WIDTH
        new_head_y = (head_y + dir_y * GRID_SIZE) % SCREEN_HEIGHT
        self.positions.insert(0, (new_head_x, new_head_y))
        if self.length != len(self.positions):
            self.positions.pop()

    def draw(self) -> None:
        """Отрисовывает змейку на игровой поверхности"""
        for position in self.positions:
            self.draw_cell(position)

    def get_head_position(self) -> tuple[int, int]:
        """Возвращает кортеж с координатами головы змейки."""
        return self.positions[0]

    def reset(self) -> None:
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [self.position]
        self.direction = choice([RIGHT, LEFT, DOWN, UP])
        self.next_direction = None


def handle_keys(game_object):
    """Обрабатывает движения клавиш, чтобы изменить направление змейки."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основная функция игры: инициализация и главный цикл."""
    pg.init()
    snake = Snake()
    apple = Apple(busy_positions=snake.positions)
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        ate_apple = (snake.get_head_position() == apple.position)
        snake.move()
        snake.update_direction()
        if ate_apple:
            snake.length += 1
            apple.randomize_position(snake.positions)
        elif snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            apple.randomize_position(snake.positions)
        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
