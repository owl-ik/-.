import pygame
import random

class GameObject:

    def __init__(self, position, body_color):
            
        self.position = position
        self.body_color = body_color

    def draw(self):
        pass


class Apple(GameObject):
    
    def __init__(self):
        super().__init__((0, 0), (180, 0, 0))
        self.randomize_position()

    def randomize_position(self):
        #Устанавливает случайное положение яблока на поле.
        self.position = (
            random.randint(0, 31) * 20,
            random.randint(0, 23) * 20,
        )

    def draw(self, surface):
        #Отрисовывает яблоко на нашем поле.
        pygame.draw.rect(surface, self.body_color, (self.position, (20, 20)))


class Snake(GameObject):
    
    def __init__(self):
        super().__init__((320, 240), (0, 0, 0))
        self.length = 1
        self.positions = [self.position]
        self.direction = pygame.K_RIGHT
        self.next_direction = None

    def update_direction(self, key):
        #Движение змейки.
        if (
            (key == pygame.K_LEFT and self.direction != pygame.K_RIGHT) or
            (key == pygame.K_RIGHT and self.direction != pygame.K_LEFT) or
            (key == pygame.K_UP and self.direction != pygame.K_DOWN) or
            (key == pygame.K_DOWN and self.direction != pygame.K_UP)
        ):
            self.next_direction = key

    def move(self):
        
        if self.next_direction is not None:
            self.direction = self.next_direction

        if self.direction == pygame.K_LEFT:
            self.position = (self.position[0] - 20, self.position[1])
        elif self.direction == pygame.K_RIGHT:
            self.position = (self.position[0] + 20, self.position[1])
        elif self.direction == pygame.K_UP:
            self.position = (self.position[0], self.position[1] - 20)
        elif self.direction == pygame.K_DOWN:
            self.position = (self.position[0], self.position[1] + 20)

        # Проверка границ поля
        if self.position[0] < 0:
            self.position = (640, self.position[1])
        elif self.position[0] > 640:
            self.position = (0, self.position[1])
        if self.position[1] < 0:
            self.position = (self.position[0], 480)
        elif self.position[1] > 480: 
            self.position = (self.position[0], 0)

        self.positions.insert(0, self.position)

        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self, surface):
        
        for position in self.positions:
            pygame.draw.rect(surface, self.body_color, (position, (20, 20)))

    def get_head_position(self):
        
        return self.positions[0]

    def reset(self):

        self.length = 1
        self.positions = [self.position]
        self.direction = pygame.K_RIGHT
        self.next_direction = None


def handle_keys(snake):

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                snake.update_direction(pygame.K_UP)
            elif event.key == pygame.K_a:
                snake.update_direction(pygame.K_LEFT)
            elif event.key == pygame.K_s:
                snake.update_direction(pygame.K_DOWN)
            elif event.key == pygame.K_d:
                snake.update_direction(pygame.K_RIGHT)


def draw_grid(surface):
    
    for x in range(0, 640, 20):
        pygame.draw.line(surface, (0, 0, 0), (x, 0), (x, 480))
    for y in range(0, 480, 20):
        pygame.draw.line(surface, (0, 0, 0), (0, y), (640, y))


def main():
    
    pygame.init()
    screen = pygame.display.set_mode((645, 485))
    pygame.display.set_caption('Snake 2.0 by Owl-ik')
    clock = pygame.time.Clock()

    snake = Snake()
    apple = Apple()

    while True:
        handle_keys(snake)
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()

        screen.fill((0, 255, 0))
        draw_grid(screen)
        snake.draw(screen)
        apple.draw(screen)
        pygame.display.update()

        clock.tick(7)


if __name__ == '__main__':
    main()
