from random import choice
import pygame


WIDTH = 1920
HEIGHT = 1080
TILE_SIZE = 100
LINE_WIDTH = 2

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


class Cell:
    def __init__(self,
                 x,
                 y) -> None:
        self.x = x
        self.y = y
        self.walls = {
            'top': True,
            'bottom': True,
            'left': True,
            'right': True
        }
        self.isVisited = False

    def draw_current_cell(self) -> None:
        x = self.x * TILE_SIZE
        y = self.y * TILE_SIZE
        pygame.draw.rect(screen,
                         pygame.Color('darkblue'),
                         (x + LINE_WIDTH, y + LINE_WIDTH,
                          TILE_SIZE - LINE_WIDTH,
                          TILE_SIZE - LINE_WIDTH))

    def draw(self) -> None:
        x = self.x * TILE_SIZE
        y = self.y * TILE_SIZE

        if not self.isVisited:
            pygame.draw.rect(screen, pygame.Color('white'),
                             (x, y, TILE_SIZE, TILE_SIZE))
        else:
            pygame.draw.rect(screen, pygame.Color('black'),
                             (x, y, TILE_SIZE, TILE_SIZE))

        if self.walls['top']:
            pygame.draw.line(screen, pygame.Color('white'),
                             (x, y), (x + TILE_SIZE, y), LINE_WIDTH)
        if self.walls['bottom']:
            pygame.draw.line(screen, pygame.Color('white'),
                             (x + TILE_SIZE, y + TILE_SIZE), (x, y + TILE_SIZE), LINE_WIDTH)
        if self.walls['left']:
            pygame.draw.line(screen, pygame.Color('white'),
                             (x, y + TILE_SIZE), (x, y), LINE_WIDTH)
        if self.walls['right']:
            pygame.draw.line(screen, pygame.Color('white'),
                             (x + TILE_SIZE, y), (x + TILE_SIZE, y + TILE_SIZE), LINE_WIDTH)
            

class Maze:
    def __init__(self) -> None:
        self.cols = WIDTH // TILE_SIZE
        self.rows = HEIGHT // TILE_SIZE
        self.cells = [[Cell(col, row) for col in range(self.cols)]
                      for row in range(self.rows)
                     ]
        self.current_cell = self.cells[0][0]
        self.stack = []

    def is_on_field(self, x, y) -> bool | Cell:
        if x < 0 or x > self.cols - 1 or y < 0 or y > self.rows - 1:
                return False
        return self.cells[y][x]

    def get_random_neighbour(self, cell) -> Cell | bool:
        left = self.is_on_field(cell.x - 1,
                                cell.y)
        right = self.is_on_field(cell.x + 1,
                                 cell.y)
        up = self.is_on_field(cell.x,
                              cell.y - 1)
        down = self.is_on_field(cell.x,
                                cell.y + 1)
        neighbours = [cell for cell in [up, down, left, right] if cell and not cell.isVisited]
        if not neighbours:
            return False
        return choice(neighbours)
    
    def remove_walls(self, current_cell: Cell, next_cell: Cell) -> None:
        dx = current_cell.x - next_cell.x
        dy = current_cell.y - next_cell.y
        print(dx, dy)
        if dx == 1:
            current_cell.walls['left'] = False
            next_cell.walls['right'] = False
        elif dx == -1:
            current_cell.walls['right'] = False
            next_cell.walls['left'] = False
        if dy == 1:
            current_cell.walls['top'] = False
            next_cell.walls['bottom'] = False
        elif dy == -1:
            current_cell.walls['bottom'] = False
            next_cell.walls['top'] = False
    
    def generate_maze(self) -> None:
        self.current_cell.isVisited = True
        self.current_cell.draw_current_cell()
        next_cell = self.get_random_neighbour(self.current_cell)
        if next_cell:
            next_cell.isVisited = True
            self.stack.append(self.current_cell)
            self.remove_walls(self.current_cell,
                              next_cell)
            self.current_cell = next_cell
        elif self.stack:
            self.current_cell = self.stack.pop()


    def draw_maze(self) -> None:
        for row in self.cells:
            for cell in row:
                cell.draw()

m = Maze()
current_cell = m.cells[0][0]

while True:
    screen.fill(pygame.Color('black'))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    m.draw_maze()
    m.generate_maze()
    pygame.display.flip()
    clock.tick(30)
    