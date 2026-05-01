import pygame
import random
from typing import List, Tuple, Optional

# Инициализация Pygame
pygame.init()

# Константы
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
CELL_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // CELL_SIZE  # 32
GRID_HEIGHT = SCREEN_HEIGHT // CELL_SIZE  # 24

# Цвета (RGB)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Направления движения
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class GameObject:
    """
    Базовый класс для всех игровых объектов.
    Содержит общие атрибуты: позицию и цвет.
    """

    def __init__(self, position: Tuple[int, int], body_color: Tuple[int, int, int]):
        """
        Инициализирует базовый игровой объект.

        Args:
            position: Координаты объекта на игровом поле (x, y)
            body_color: RGB-цвет объекта
        """
        self.position = position
        self.body_color = body_color

    def draw(self, surface: pygame.Surface) -> None:
        """
        Абстрактный метод для отрисовки объекта.
        Должен быть переопределён в дочерних классах.

        Args:
            surface: Поверхность Pygame для отрисовки
        """
        pass


class Apple(GameObject):
    """
    Класс яблока, которое появляется в случайных местах игрового поля.
    При съедании змейкой перемещается на новую позицию.
    """

    def __init__(self):
        """Инициализирует яблоко с красным цветом и случайной позицией."""
        super().__init__((0, 0), RED)
        self.randomize_position()

    def randomize_position(self) -> None:
        """
        Устанавливает случайную позицию яблока в пределах игрового поля.
        Координаты привязаны к сетке (кратны CELL_SIZE).
        """
        grid_x = random.randint(0, GRID_WIDTH - 1)
        grid_y = random.randint(0, GRID_HEIGHT - 1)
        self.position = (grid_x * CELL_SIZE, grid_y * CELL_SIZE)

    def draw(self, surface: pygame.Surface) -> None:
        """
        Отрисовывает яблоко на игровой поверхности.

        Args:
            surface: Поверхность Pygame для отрисовки
        """
        rect = pygame.Rect(
            self.position[0], self.position[1], CELL_SIZE, CELL_SIZE
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BLACK, rect, 1)  # Контур для лучшей видимости


class Snake(GameObject):
    """
    Класс змейки, управляемой игроком.
    Содержит логику движения, роста, проверки столкновений и сброса состояния.
    """

    def __init__(self):
        """Инициализирует змейку в начальном состоянии."""
        # Позиция головы в центре экрана
        start_x = (GRID_WIDTH // 2) * CELL_SIZE
        start_y = (GRID_HEIGHT // 2) * CELL_SIZE
        super().__init__((start_x, start_y), GREEN)

        # Список позиций всех сегментов (каждый элемент - кортеж (x, y))
        self.positions: List[Tuple[int, int]] = [self.position]

        # Длина змейки (количество сегментов)
        self.length: int = 1

        # Текущее направление движения
        self.direction: Tuple[int, int] = RIGHT

        # Следующее направление (для обработки нажатий клавиш)
        self.next_direction: Optional[Tuple[int, int]] = None

    def update_direction(self) -> None:
        """
        Обновляет направление движения змейки.
        Запрещает движение в противоположную сторону
        (нельзя развернуться на 180 градусов).
        """
        if self.next_direction is not None:
            # Проверка: нельзя двигаться в противоположную сторону
            opposite_directions = {
                UP: DOWN,
                DOWN: UP,
                LEFT: RIGHT,
                RIGHT: LEFT
            }
            if opposite_directions.get(self.next_direction) != self.direction:
                self.direction = self.next_direction
            self.next_direction = None

    def move(self) -> None:
        """
        Перемещает змейку в текущем направлении.
        Добавляет новую голову в начало списка и удаляет хвост,
        если длина не увеличилась при съедании яблока.
        """
        head_x, head_y = self.get_head_position()

        # Вычисляем новую позицию головы
        new_head_x = head_x + self.direction[0] * CELL_SIZE
        new_head_y = head_y + self.direction[1] * CELL_SIZE

        # Телепортация через границы (прохождение сквозь стены)
        new_head_x = new_head_x % SCREEN_WIDTH
        new_head_y = new_head_y % SCREEN_HEIGHT

        new_head = (new_head_x, new_head_y)

        # Вставляем новую голову в начало списка
        self.positions.insert(0, new_head)

        # Если длина змейки не превышает текущую, удаляем последний сегмент
        if len(self.positions) > self.length:
            self.positions.pop()

        # Обновляем позицию головы в родительском классе
        self.position = self.positions[0]

    def draw(self, surface: pygame.Surface) -> None:
        """
        Отрисовывает змейку на игровой поверхности.
        Голова рисуется более ярким оттенком.

        Args:
            surface: Поверхность Pygame для отрисовки
        """
        for i, pos in enumerate(self.positions):
            rect = pygame.Rect(pos[0], pos[1], CELL_SIZE, CELL_SIZE)
            # Голова змейки рисуется более светлым цветом
            if i == 0:
                pygame.draw.rect(surface, (0, 200, 0), rect)
            else:
                pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BLACK, rect, 1)  # Контур

    def get_head_position(self) -> Tuple[int, int]:
        """
        Возвращает позицию головы змейки.

        Returns:
            Кортеж (x, y) с координатами головы
        """
        return self.positions[0]

    def check_self_collision(self) -> bool:
        """
        Проверяет, столкнулась ли змейка сама с собой.

        Returns:
            True, если голова столкнулась с телом, иначе False
        """
        head = self.get_head_position()
        # Голова не должна совпадать ни с одним из сегментов тела
        return head in self.positions[1:]

    def reset(self) -> None:
        """Сбрасывает змейку в начальное состояние после проигрыша."""
        start_x = (GRID_WIDTH // 2) * CELL_SIZE
        start_y = (GRID_HEIGHT // 2) * CELL_SIZE
        self.position = (start_x, start_y)
        self.positions = [self.position]
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None

    def grow(self) -> None:
        """
        Увеличивает длину змейки на один сегмент.
        Вызывается при съедании яблока.
        """
        self.length += 1


def handle_keys(snake: Snake) -> None:
    """
    Обрабатывает нажатия клавиш и устанавливает следующее направление движения.

    Args:
        snake: Объект змейки, у которого будет изменено направление
    """
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
    """Основная функция игры. Инициализирует и запускает игровой цикл."""
    # Настройка окна
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Изгиб Питона - Классическая Змейка")

    # Часы для контроля FPS
    clock = pygame.time.Clock()

    # Создание игровых объектов
    snake = Snake()
    apple = Apple()

    # Основной игровой цикл
    while True:
        # Обработка событий клавиатуры и закрытия окна
        handle_keys(snake)

        # Обновление направления движения змейки
        snake.update_direction()

        # Перемещение змейки
        snake.move()

        # Проверка: съела ли змейка яблоко?
        if snake.get_head_position() == apple.position:
            snake.grow()  # Увеличиваем длину змейки
            apple.randomize_position()  # Перемещаем яблоко

            # Если яблоко появилось на теле змейки, генерируем новую позицию
            while apple.position in snake.positions:
                apple.randomize_position()

        # Проверка столкновения с самим собой
        if snake.check_self_collision():
            snake.reset()  # Сбрасываем змейку
            apple.randomize_position()  # Сбрасываем яблоко

        # Отрисовка: заливаем фон чёрным цветом
        screen.fill(BLACK)

        # Отрисовка яблока и змейки
        apple.draw(screen)
        snake.draw(screen)

        # Обновление экрана
        pygame.display.update()

        # Задержка для контроля скорости игры (20 кадров в секунду)
        clock.tick(20)


if __name__ == "__main__":
    main()
