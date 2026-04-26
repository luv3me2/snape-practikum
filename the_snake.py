"""Snake game implementation using Pygame."""
import pygame
import random
from typing import List, Tuple, Optional


class GameObject:
    """Base class for all game objects."""
    
    def __init__(self, position: Tuple[int, int], body_color: Tuple[int, int, int]):
        """Initialize game object with position and color.
        
        Args:
            position: Tuple of (x, y) coordinates for the object.
            body_color: RGB tuple for object color.
        """
        self.position = position
        self.body_color = body_color
    
    def draw(self, surface: pygame.Surface, cell_size: int = 20) -> None:
        """Draw object on the game surface.
        
        Args:
            surface: Pygame surface to draw on.
            cell_size: Size of each cell in pixels.
        """
        raise NotImplementedError("Subclasses must implement draw method")


class Apple(GameObject):
    """Apple class representing food for the snake."""
    
    def __init__(self, screen_width: int = 640, screen_height: int = 480, 
                 cell_size: int = 20):
        """Initialize apple with random position.
        
        Args:
            screen_width: Width of game screen in pixels.
            screen_height: Height of game screen in pixels.
            cell_size: Size of each cell in pixels.
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.cell_size = cell_size
        self.body_color = (255, 0, 0)  # Red color
        self.randomize_position()
        super().__init__(self.position, self.body_color)
    
    def randomize_position(self) -> None:
        """Set random position for apple within game field boundaries."""
        max_x = (self.screen_width // self.cell_size) - 1
        max_y = (self.screen_height // self.cell_size) - 1
        random_x = random.randint(0, max_x) * self.cell_size
        random_y = random.randint(0, max_y) * self.cell_size
        self.position = (random_x, random_y)
    
    def draw(self, surface: pygame.Surface, cell_size: int = 20) -> None:
        """Draw apple on the game surface.
        
        Args:
            surface: Pygame surface to draw on.
            cell_size: Size of each cell in pixels.
        """
        rect = pygame.Rect(self.position[0], self.position[1], cell_size, cell_size)
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, (200, 0, 0), rect, 1)  # Border for better visibility


class Snake(GameObject):
    """Snake class representing the player character."""
    
    def __init__(self, screen_width: int = 640, screen_height: int = 480,
                 cell_size: int = 20):
        """Initialize snake with starting position and default values.
        
        Args:
            screen_width: Width of game screen in pixels.
            screen_height: Height of game screen in pixels.
            cell_size: Size of each cell in pixels.
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.cell_size = cell_size
        self.length = 1
        self.body_color = (0, 255, 0)  # Green color
        
        # Start in the center of the screen
        center_x = (screen_width // 2) // cell_size * cell_size
        center_y = (screen_height // 2) // cell_size * cell_size
        self.positions: List[Tuple[int, int]] = [(center_x, center_y)]
        
        self.direction = (1, 0)  # Moving right initially
        self.next_direction: Optional[Tuple[int, int]] = None
        
        super().__init__(self.positions[0], self.body_color)
    
    def update_direction(self) -> None:
        """Update snake direction based on queued next direction."""
        if self.next_direction is not None:
            # Prevent moving backwards
            opposite_directions = {
                (1, 0): (-1, 0),   # right vs left
                (-1, 0): (1, 0),   # left vs right
                (0, 1): (0, -1),   # down vs up
                (0, -1): (0, 1)    # up vs down
            }
            if opposite_directions.get(self.next_direction) != self.direction:
                self.direction = self.next_direction
            self.next_direction = None
    
    def move(self) -> None:
        """Update snake position by moving one step in current direction."""
        head_x, head_y = self.positions[0]
        
        # Calculate new head position
        dir_x, dir_y = self.direction
        new_head_x = head_x + dir_x * self.cell_size
        new_head_y = head_y + dir_y * self.cell_size
        
        # Handle screen wrapping (snake appears on opposite side)
        new_head_x %= self.screen_width
        new_head_y %= self.screen_height
        
        new_head = (new_head_x, new_head_y)
        
        # Insert new head and remove tail if not growing
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.positions.pop()
    
    def draw(self, surface: pygame.Surface, cell_size: int = 20) -> None:
        """Draw snake on the game surface.
        
        Args:
            surface: Pygame surface to draw on.
            cell_size: Size of each cell in pixels.
        """
        for i, position in enumerate(self.positions):
            rect = pygame.Rect(position[0], position[1], cell_size, cell_size)
            # Head is brighter, body segments have gradient
            if i == 0:
                pygame.draw.rect(surface, (0, 200, 0), rect)
            else:
                pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, (0, 150, 0), rect, 1)  # Border
    
    def get_head_position(self) -> Tuple[int, int]:
        """Return current head position of the snake.
        
        Returns:
            Tuple of (x, y) coordinates of snake's head.
        """
        return self.positions[0]
    
    def reset(self) -> None:
        """Reset snake to initial state."""
        self.length = 1
        
        # Reset position to center
        center_x = (self.screen_width // 2) // self.cell_size * self.cell_size
        center_y = (self.screen_height // 2) // self.cell_size * self.cell_size
        self.positions = [(center_x, center_y)]
        
        self.direction = (1, 0)  # Moving right
        self.next_direction = None
    
    def grow(self) -> None:
        """Increase snake length when apple is eaten."""
        self.length += 1
    
    def check_self_collision(self) -> bool:
        """Check if snake collided with itself.
        
        Returns:
            True if head collides with body, False otherwise.
        """
        head = self.positions[0]
        return head in self.positions[1:]


def handle_keys(snake: Snake) -> None:
    """Handle keyboard input to control snake direction.
    
    Args:
        snake: Snake object to control.
    """
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        snake.next_direction = (0, -1)
    elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
        snake.next_direction = (0, 1)
    elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
        snake.next_direction = (-1, 0)
    elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        snake.next_direction = (1, 0)


def main() -> None:
    """Main game loop."""
    # Initialize Pygame
    pygame.init()
    
    # Game constants
    SCREEN_WIDTH = 640
    SCREEN_HEIGHT = 480
    CELL_SIZE = 20
    FPS = 20
    
    # Colors
    BLACK = (0, 0, 0)
    
    # Set up display
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Изгиб Питона - Snake Game")
    clock = pygame.time.Clock()
    
    # Create game objects
    snake = Snake(SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE)
    apple = Apple(SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE)
    
    # Game state
    running = True
    score = 0
    
    # Font for score display
    font = pygame.font.Font(None, 36)
    
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Handle keyboard input
        handle_keys(snake)
        
        # Update snake direction
        snake.update_direction()
        
        # Move snake
        snake.move()
        
        # Check if snake ate apple
        if snake.get_head_position() == apple.position:
            snake.grow()
            score += 1
            
            # Respawn apple at random position without colliding with snake
            old_position = apple.position
            while apple.position == old_position or apple.position in snake.positions:
                apple.randomize_position()
        
        # Check for self collision
        if snake.check_self_collision():
            snake.reset()
            score = 0
            apple.randomize_position()
        
        # Drawing
        screen.fill(BLACK)
        
        # Optional: Draw grid lines for better visibility
        for x in range(0, SCREEN_WIDTH, CELL_SIZE):
            pygame.draw.line(screen, (40, 40, 40), (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, CELL_SIZE):
            pygame.draw.line(screen, (40, 40, 40), (0, y), (SCREEN_WIDTH, y))
        
        # Draw game objects
        apple.draw(screen, CELL_SIZE)
        snake.draw(screen, CELL_SIZE)
        
        # Draw score
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        
        # Draw instructions
        inst_font = pygame.font.Font(None, 20)
        inst_text = inst_font.render("Use Arrow Keys or WASD to control", True, (200, 200, 200))
        screen.blit(inst_text, (SCREEN_WIDTH - 250, SCREEN_HEIGHT - 25))
        
        # Update display
        pygame.display.update()
        
        # Control game speed
        clock.tick(FPS)
    
    # Quit game
    pygame.quit()


if __name__ == "__main__":
    main()
