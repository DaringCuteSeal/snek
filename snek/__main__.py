import pyxel
import os
from enum import Enum

WINDOW_WIDTH = 192
WINDOW_HEIGHT = 128

# Classes
class Direction(Enum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3

class Apple:
    """
    Apple class that handles the apple location.
    """
    def __init__(self, x: int, y: int):
        self.x, self.y, self.w, self.h = x, y, 8, 8

    def draw(self):
        pyxel.blt(self.x, self.y, 0, 16, 0, self.w, self.h)

    def intersects(self, u, v) -> bool:
        return True if u == self.x and v == self.y else False

class SnakeSection:
    """
    Draw snake section including orienting the head.
    Also checks if something intersects it (snake crashes into itself).
    """
    def __init__(self, x: int, y: int, is_head: bool = False):
        self.x, self.y, self.w, self.h = x, y, 8, 8
        self.is_head = is_head

    def draw(self, dir: Direction):
        width, height, sprite_x, sprite_y = self.w, self.h, 0, 0

        # If this is head, we need to change and flip the sprite
        # depending on the direction.
        if self.is_head:
            match dir:
                case Direction.RIGHT:
                    sprite_x, sprite_y = 8, 0
                case Direction.LEFT:
                    sprite_x, sprite_y = 8, 0
                    width = width * -1
                case Direction.DOWN:
                    sprite_x, sprite_y = 0, 8
                case Direction.UP:
                    sprite_x, sprite_y = 0, 8
                    height = height * -1
        pyxel.blt(self.x, self.y, 0, sprite_x, sprite_y, width, height)


# Main loop for Everything   
class App:
    def __init__(self):
        pyxel.init(WINDOW_WIDTH, WINDOW_HEIGHT, capture_scale=8, title="Snake Game", fps=8)
        pyxel.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../res/res.pyxres"))

        self.setup()
        self.end = 0

        pyxel.run(self.update, self.draw)

    def setup(self):
        # Initialize apple
        self.apple = Apple(64, 32)

        # Initialize snake
        self.append_snake = False
        self.snake: list[SnakeSection] = []
        self.snake.append(SnakeSection(32, 32, is_head=True))
        self.snake.append(SnakeSection(24, 32))
        self.snake.append(SnakeSection(16, 32))
        self.snake_direction = Direction.RIGHT

        # Initialize score
        self.score = 0

    def update(self):
        if self.end != 1:
            if pyxel.btn(pyxel.KEY_RIGHT) and self.snake_direction != Direction.LEFT:
                self.snake_direction = Direction.RIGHT
            elif pyxel.btn(pyxel.KEY_LEFT) and self.snake_direction != Direction.RIGHT:
                self.snake_direction = Direction.LEFT
            elif pyxel.btn(pyxel.KEY_UP) and self.snake_direction != Direction.DOWN:
                self.snake_direction = Direction.UP
            elif pyxel.btn(pyxel.KEY_DOWN) and self.snake_direction != Direction.UP:
                self.snake_direction = Direction.DOWN
            self.move_snake()

    def draw(self):
        pyxel.cls(0)
        self.apple.draw()

        for s in self.snake:
            s.draw(self.snake_direction)
        
        self.check_collisions()
        if self.end == 1:
            pyxel.rect(35, 35, 120, 20, 9)
            pyxel.text(80, 38, "You lost!", 7)
            pyxel.text(70, 46, "r to restart...", 7)

            if pyxel.btn(pyxel.KEY_R):
                self.end = 0
                self.setup()

        self.draw_score()

    def move_snake(self):
        # Append body?
        if self.append_snake:
            self.snake.append(SnakeSection(self.snake[-1].x - self.snake[-1].w, self.snake[-1].y - self.snake[-1].w))
            self.append_snake = False

        # Move head
        previous_location_x = self.snake[0].x
        previous_location_y = self.snake[0].y
        
        match(self.snake_direction):
            case Direction.RIGHT:
                self.snake[0].x += self.snake[0].w
            case Direction.LEFT:
                self.snake[0].x -= self.snake[0].w
            case Direction.UP:
                self.snake[0].y -= self.snake[0].w
            case Direction.DOWN:
                self.snake[0].y += self.snake[0].w

        for s in self.snake:
            if s == self.snake[0]:
                continue
            current_location_x = s.x
            current_location_y = s.y
            s.x = previous_location_x
            s.y = previous_location_y
            previous_location_x = current_location_x
            previous_location_y = current_location_y

    def check_collisions(self):
        # Apple
        if self.apple.intersects(self.snake[0].x, self.snake[0].y):
            self.append_snake = True
            self.apple.x = pyxel.ceil(pyxel.rndi(8, WINDOW_WIDTH - 8) / 8) * 8
            self.apple.y = pyxel.ceil(pyxel.rndi(8, WINDOW_HEIGHT - 8) / 8) * 8
            self.score += 1

        # Snake (with the edge of screen)
        if self.snake[0].x > WINDOW_WIDTH - 8 or self.snake[0].x < 1 or self.snake[0].y > WINDOW_HEIGHT - 8 or self.snake[0].y < 1: # what the hell?
            self.end = 1
        
        # Snake (with itself)
        for s in self.snake[1:]:
            if self.snake[0].x == s.x and self.snake[0].y == s.y:
                self.end = 1
    
    def draw_score(self):
        pyxel.text(5, 5, f"Score: {self.score}", 7)

App() if __name__ == "__main__" else None
