from random import randint
import pygame

# Константы для размеров поля и сетки
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета
BOARD_BACKGROUND_COLOR = (0, 0, 0)  # Цвет фона
BORDER_COLOR = (93, 216, 228)        # Цвет границы ячейки
APPLE_COLOR = (255, 0, 0)            # Цвет яблока
SNAKE_COLOR = (0, 255, 0)            # Цвет змейки

# Скорость движения змейки
SPEED = 20

# Настройка игрового окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Змейка')  # Заголовок окна игрового поля
clock = pygame.time.Clock()  # Настройка времени


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, position, body_color):
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Отрисовывает объект."""
        pass


class Apple(GameObject):
    """Класс для яблока."""

    def __init__(self):
        super().__init__((0, 0), APPLE_COLOR)
        self.randomize_position()

    def randomize_position(self):
        """Случайным образом устанавливает позицию яблока."""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
        )

    def draw(self):
        """Отрисовывает яблоко на экране."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):

    def __init__(self):
        super().__init__((320, 240), SNAKE_COLOR)
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self):
       
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        
        if self.direction == UP:
            self.position = (self.position[0], self.position[1] - GRID_SIZE)
        elif self.direction == DOWN:
            self.position = (self.position[0], self.position[1] + GRID_SIZE)
        elif self.direction == LEFT:
            self.position = (self.position[0] - GRID_SIZE, self.position[1])
        elif self.direction == RIGHT:
            self.position = (self.position[0] + GRID_SIZE, self.position[1])

        
        if self.position[0] < 0:
            self.position = (SCREEN_WIDTH, self.position[1])
        elif self.position[0] >= SCREEN_WIDTH:
            self.position = (0, self.position[1])
        if self.position[1] < 0:
            self.position = (self.position[0], SCREEN_HEIGHT)
        elif self.position[1] >= SCREEN_HEIGHT:
            self.position = (self.position[0], 0)

        self.positions.insert(0, self.position)

        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self):
      
        for position in self.positions[:-1]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

       
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

       
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
       
        return self.positions[0]

    def reset(self):
       
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None


def handle_keys(game_object):
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    
    pygame.init()  # Инициализация PyGame

    # Инициализация игровых объектов
    snake = Snake()
    apple = Apple()

    # Отрисовка сетки на игровом поле
    for x in range(0, SCREEN_WIDTH, GRID_SIZE):
        pygame.draw.line(screen, BORDER_COLOR, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, BORDER_COLOR, (0, y), (SCREEN_WIDTH, y))

    pygame.display.update()  # Обновление экрана

    while True:
        handle_keys(snake)  # Обработка событий
        snake.update_direction()
        snake.move()

        # Проверка столкновения змейки с яблоком
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()

        # Проверка столкновения змейки с самой собой
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()

        screen.fill(BOARD_BACKGROUND_COLOR)  # Отрисовка объектов
        snake.draw()
        apple.draw()
        pygame.display.update()  # Обновление экрана

        clock.tick(SPEED)  # Контроль скорости игры


if __name__ == '__main__':
    main()

