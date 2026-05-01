"""
Тесты для проверки финального проекта «Изгиб Питона».
Проверяет наличие классов, методов и базовую логику игры.
"""
import importlib
import os
import sys
import unittest
from unittest.mock import Mock, patch

# Добавляем текущую директорию в путь для импорта
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Импортируем модуль игры
try:
    import the_snake as snake_game
except ImportError:
    import game as snake_game


class TestGameObject(unittest.TestCase):
    """Тесты для базового класса GameObject."""

    def test_class_exists(self):
        """Проверяет существование класса GameObject."""
        self.assertTrue(hasattr(snake_game, 'GameObject'))
        self.assertTrue(hasattr(snake_game.GameObject, '__init__'))
        self.assertTrue(hasattr(snake_game.GameObject, 'draw'))

    def test_init_method(self):
        """Проверяет инициализацию GameObject."""
        obj = snake_game.GameObject((100, 100), (255, 0, 0))
        self.assertEqual(obj.position, (100, 100))
        self.assertEqual(obj.body_color, (255, 0, 0))

    def test_draw_method(self):
        """Проверяет наличие метода draw."""
        obj = snake_game.GameObject((0, 0), (0, 0, 0))
        self.assertTrue(callable(obj.draw))


class TestApple(unittest.TestCase):
    """Тесты для класса Apple."""

    def setUp(self):
        """Подготовка тестовых данных."""
        if hasattr(snake_game, 'Apple'):
            self.apple = snake_game.Apple()

    def test_class_exists(self):
        """Проверяет существование класса Apple."""
        self.assertTrue(hasattr(snake_game, 'Apple'))
        self.assertTrue(issubclass(snake_game.Apple, snake_game.GameObject))

    def test_init_method(self):
        """Проверяет инициализацию яблока."""
        if hasattr(snake_game, 'Apple'):
            self.assertEqual(self.apple.body_color, snake_game.RED)

    def test_randomize_position(self):
        """Проверяет метод randomize_position."""
        if hasattr(snake_game, 'Apple'):
            old_position = self.apple.position
            self.apple.randomize_position()
            self.assertNotEqual(old_position, self.apple.position)
            # Проверяем, что позиция в пределах поля
            x, y = self.apple.position
            self.assertLess(x, snake_game.SCREEN_WIDTH)
            self.assertLess(y, snake_game.SCREEN_HEIGHT)
            self.assertEqual(x % snake_game.CELL_SIZE, 0)
            self.assertEqual(y % snake_game.CELL_SIZE, 0)

    def test_draw_method(self):
        """Проверяет метод draw."""
        if hasattr(snake_game, 'Apple'):
            self.assertTrue(callable(self.apple.draw))


class TestSnake(unittest.TestCase):
    """Тесты для класса Snake."""

    def setUp(self):
        """Подготовка тестовых данных."""
        if hasattr(snake_game, 'Snake'):
            self.snake = snake_game.Snake()

    def test_class_exists(self):
        """Проверяет существование класса Snake."""
        self.assertTrue(hasattr(snake_game, 'Snake'))
        self.assertTrue(issubclass(snake_game.Snake, snake_game.GameObject))

    def test_init_method(self):
        """Проверяет инициализацию змейки."""
        if hasattr(snake_game, 'Snake'):
            self.assertEqual(self.snake.length, 1)
            self.assertEqual(len(self.snake.positions), 1)
            self.assertEqual(self.snake.direction, snake_game.RIGHT)
            self.assertIsNone(self.snake.next_direction)

    def test_get_head_position(self):
        """Проверяет метод get_head_position."""
        if hasattr(snake_game, 'Snake'):
            head = self.snake.get_head_position()
            self.assertEqual(head, self.snake.positions[0])

    def test_update_direction(self):
        """Проверяет метод update_direction."""
        if hasattr(snake_game, 'Snake'):
            # Устанавливаем новое направление
            self.snake.next_direction = snake_game.UP
            self.snake.update_direction()
            self.assertEqual(self.snake.direction, snake_game.UP)

            # Проверяем запрет движения назад
            self.snake.direction = snake_game.UP
            self.snake.next_direction = snake_game.DOWN
            self.snake.update_direction()
            self.assertEqual(self.snake.direction, snake_game.UP)

    def test_move(self):
        """Проверяет метод move."""
        if hasattr(snake_game, 'Snake'):
            old_head = self.snake.get_head_position()
            self.snake.move()
            new_head = self.snake.get_head_position()
            self.assertNotEqual(old_head, new_head)

    def test_grow(self):
        """Проверяет метод grow."""
        if hasattr(snake_game, 'Snake'):
            old_length = self.snake.length
            self.snake.grow()
            self.assertEqual(self.snake.length, old_length + 1)

    def test_check_self_collision(self):
        """Проверяет метод check_self_collision."""
        if hasattr(snake_game, 'Snake'):
            # Изначально нет столкновения
            self.assertFalse(self.snake.check_self_collision())

            # Создаём искусственное столкновение
            head = self.snake.get_head_position()
            self.snake.positions.append(head)
            self.assertTrue(self.snake.check_self_collision())

    def test_reset(self):
        """Проверяет метод reset."""
        if hasattr(snake_game, 'Snake'):
            # Меняем состояние
            self.snake.length = 5
            self.snake.direction = snake_game.UP
            self.snake.grow()

            # Сбрасываем
            self.snake.reset()

            # Проверяем начальное состояние
            self.assertEqual(self.snake.length, 1)
            self.assertEqual(len(self.snake.positions), 1)
            self.assertEqual(self.snake.direction, snake_game.RIGHT)
            self.assertIsNone(self.snake.next_direction)

    def test_draw_method(self):
        """Проверяет метод draw."""
        if hasattr(snake_game, 'Snake'):
            self.assertTrue(callable(self.snake.draw))


class TestGameFunctions(unittest.TestCase):
    """Тесты для глобальных функций игры."""

    def test_handle_keys_exists(self):
        """Проверяет существование функции handle_keys."""
        self.assertTrue(hasattr(snake_game, 'handle_keys'))
        self.assertTrue(callable(snake_game.handle_keys))

    def test_main_exists(self):
        """Проверяет существование функции main."""
        self.assertTrue(hasattr(snake_game, 'main'))
        self.assertTrue(callable(snake_game.main))

    def test_constants_exist(self):
        """Проверяет наличие необходимых констант."""
        required_constants = [
            'SCREEN_WIDTH', 'SCREEN_HEIGHT', 'CELL_SIZE',
            'BLACK', 'GREEN', 'RED', 'UP', 'DOWN', 'LEFT', 'RIGHT'
        ]
        for const in required_constants:
            self.assertTrue(hasattr(snake_game, const))

    def test_constants_values(self):
        """Проверяет корректность значений констант."""
        self.assertEqual(snake_game.SCREEN_WIDTH, 640)
        self.assertEqual(snake_game.SCREEN_HEIGHT, 480)
        self.assertEqual(snake_game.CELL_SIZE, 20)
        self.assertEqual(snake_game.UP, (0, -1))
        self.assertEqual(snake_game.DOWN, (0, 1))
        self.assertEqual(snake_game.LEFT, (-1, 0))
        self.assertEqual(snake_game.RIGHT, (1, 0))


class TestGameLogic(unittest.TestCase):
    """Тесты для проверки игровой логики."""

    @patch('pygame.display.set_mode')
    @patch('pygame.display.set_caption')
    @patch('pygame.time.Clock')
    def test_main_initialization(self, mock_clock, mock_set_caption,
                                 mock_set_mode):
        """Проверяет инициализацию игры."""
        # Создаём моки
        mock_screen = Mock()
        mock_set_mode.return_value = mock_screen

        # Импортируем модуль заново для изоляции
        if 'the_snake' in sys.modules:
            importlib.reload(snake_game)

        # Этот тест проверяет только что функция main существует
        self.assertTrue(callable(snake_game.main))

    def test_apple_randomization(self):
        """Проверяет, что яблоко появляется в разных местах."""
        if hasattr(snake_game, 'Apple'):
            apple = snake_game.Apple()
            positions = set()

            for _ in range(100):
                apple.randomize_position()
                positions.add(apple.position)

            # Должно быть сгенерировано много разных позиций
            self.assertGreater(len(positions), 1)

    def test_snake_movement_direction(self):
        """Проверяет движение змейки в разных направлениях."""
        if hasattr(snake_game, 'Snake'):
            snake = snake_game.Snake()
            start_head = snake.get_head_position()

            # Движение вправо (по умолчанию)
            snake.move()
            new_head = snake.get_head_position()
            expected_x = start_head[0] + snake_game.CELL_SIZE
            self.assertEqual(new_head[0], expected_x)
            self.assertEqual(new_head[1], start_head[1])

    def test_snake_eats_apple(self):
        """Проверяет, что змейка растёт при съедании яблока."""
        if hasattr(snake_game, 'Snake') and hasattr(snake_game, 'Apple'):
            snake = snake_game.Snake()
            apple = snake_game.Apple()

            # Устанавливаем яблоко на позицию головы
            apple.position = snake.get_head_position()

            old_length = snake.length
            if snake.get_head_position() == apple.position:
                if hasattr(snake, 'grow'):
                    snake.grow()
                    self.assertEqual(snake.length, old_length + 1)

    def test_wall_teleportation(self):
        """Проверяет телепортацию через границы."""
        if hasattr(snake_game, 'Snake'):
            snake = snake_game.Snake()

            # Помещаем голову на правую границу
            edge_x = snake_game.SCREEN_WIDTH - snake_game.CELL_SIZE
            snake.positions[0] = (edge_x, snake_game.SCREEN_HEIGHT // 2)
            snake.direction = snake_game.RIGHT
            snake.move()

            new_head = snake.get_head_position()
            # Должна появиться с левой стороны
            self.assertEqual(new_head[0], 0)

    def test_self_collision_reset(self):
        """Проверяет сброс игры при столкновении с собой."""
        if hasattr(snake_game, 'Snake'):
            snake = snake_game.Snake()

            # Создаём длинную змейку
            for _ in range(5):
                snake.grow()

            # Создаём столкновение
            head = snake.get_head_position()
            snake.positions.append(head)

            # Проверяем обнаружение столкновения
            self.assertTrue(snake.check_self_collision())

            # Сбрасываем
            snake.reset()
            self.assertEqual(snake.length, 1)
            self.assertFalse(snake.check_self_collision())


class TestPEP8Compliance(unittest.TestCase):
    """Тесты для проверки соответствия PEP8."""

    def test_no_tabs(self):
        """Проверяет отсутствие символов табуляции."""
        with open('the_snake.py', 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertNotIn('\t', content, 'Найдены символы табуляции')

    def test_line_length(self):
        """Проверяет длину строк."""
        with open('the_snake.py', 'r', encoding='utf-8') as f:
            for i, line in enumerate(f, 1):
                # Игнорируем длинные строки с URL или импортами
                if 'http' not in line and 'import' not in line:
                    self.assertLessEqual(
                        len(line.rstrip('\n')), 79,
                        f'Строка {i} длиннее 79 символов'
                    )


def run_tests():
    """Запускает все тесты и возвращает результат."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTests(loader.loadTestsFromTestCase(TestGameObject))
    suite.addTests(loader.loadTestsFromTestCase(TestApple))
    suite.addTests(loader.loadTestsFromTestCase(TestSnake))
    suite.addTests(loader.loadTestsFromTestCase(TestGameFunctions))
    suite.addTests(loader.loadTestsFromTestCase(TestGameLogic))
    suite.addTests(loader.loadTestsFromTestCase(TestPEP8Compliance))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
