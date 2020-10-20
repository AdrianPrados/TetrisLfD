"""
STATE = GAME STATE
OBSERVATION = OBSERVATION

NB! MARIUS, STATE != OBSERVATION
"""
# oversikt
# TODO Check collision for left action, både for blokker og out-of-bounds
# TODO Check collision for Right action, både for blokker og out-of-bounds
# TODO Check collision for Rotate action, både for blokker og out-of-bounds
# TODO sjekk om rad blir fullført, reward, og flytt alle blokker over ned
# TODO sjekk om "spawn" er blokkert, envtuelt tap
# TODO render score og div info
# TODO diskuter config, mtp gravity (realtime game til turnbased)

import math
import random
import pygame as pg
import copy

from actions import Action
from shapes import Shape
from colors import Color

class Tetris():

    def __init__(self):
        
        self.config = {
            'hard_drop': 1, # Action.DOWN goes all the way down
            'gravity': 0    # Piece moves down after all moves
        }
        
        self.cell_size = 25
        self.margin_top = 40  # margin for game grid
        self.margin_left = 40

        self.window_height = self.window_width = 600
        
        # Standard Tetris layout
        self.game_rows = 20
        self.game_columns = 10
        
        pg.init()
        pg.display.set_caption('TETRIS')

        self.screen = pg.display.set_mode((self.window_height, self.window_width))
        self.clock = pg.time.Clock()
        self.screen.fill(Color.BLACK)

        self.start_position = [0, 3]
        self.position = copy.deepcopy(self.start_position)

    def reset(self):
        self.state = [[0 for _ in range(self.game_columns)] for _ in range(self.game_rows)]
        
        # Start position
        self.current_shape = self.get_blocks_from_shape(self.new_shape(), self.start_position)

        return self.state

    def get_blocks_from_shape(self, shape, offset=[0, 0]):
        blocks = []

        for i, row in enumerate(shape):
            for j, cell in enumerate(row):
                if cell != '0':
                    blocks.append([j, i])

        # normalize
        lower_y = min([y for y, x in blocks])
        lower_x = min([x for y, x in blocks])

        return [[y-lower_y+offset[0], x-lower_x+offset[1]] for y, x in blocks]

    # for current state
    def check_collision_down(self, shape):

        cells_under = None

        try:
            cells_under = [self.state[y+1][x] for y, x in shape]
        except:
            return True

        for cell in cells_under:
            if cell == 1:
                return True
        
        return False

    def new_shape(self):
        self.current_piece = random.randint(0, len(Shape.ALL)-1)
        self.current_rotation = 0
        return Shape.ALL[self.current_piece][self.current_rotation]

    def place_current_shape(self):
                
        for block in self.current_shape:

            self.state[block[0]][block[1]] = 1

        self.current_shape = self.get_blocks_from_shape(self.new_shape(), self.start_position)

    def step(self, action):
        
        old_state = self.state
        new_state = None

        reward = 0
        done = False
        info = ''
        placed = False # if current piece lands on another or bottom

        # for checking
        next_position = copy.deepcopy(self.current_shape)

        if action == Action.DOWN:

            if self.config['hard_drop']:

                while not placed:
                    collision = self.check_collision_down(self.current_shape)

                    if not collision:
                        next_position = [[y+1, x] for y, x in next_position]
                    else:
                        placed = True

                    self.current_shape = next_position
            else:
                collision = self.check_collision_down(self.current_shape)

                if not collision:
                    next_position = [[y+1, x] for y, x in next_position]
                else:
                    placed = True

        elif action == Action.LEFT:
            next_position = [[y, x-1] for y, x in next_position]

            # TODO Check collision left
            # If collision, next position = current position

        elif action == Action.RIGHT:
            next_position = [[y, x+1] for y, x in next_position]

            # TODO Check collision right
            # If collision, next position = current position

        elif action == Action.ROTATE:
            self.current_rotation = (self.current_rotation - 1) % len(Shape.ALL[self.current_piece])
            new_rotation = Shape.ALL[self.current_piece][self.current_rotation]
            next_position = self.get_blocks_from_shape(new_rotation, self.current_shape[0])

            # TODO Check collision after rotation
            # If collision, next position = current position

        elif action == Action.WAIT:
            # do nothing
            pass
        
        if self.config['gravity']:
            # go down one tile after all moves
            collision = self.check_collision_down(self.current_shape)

            if not collision:
                next_position = [[y+1, x] for y, x in next_position]
            else:
                placed = True

        if placed:
            self.place_current_shape()
        else:
            self.current_shape = next_position

        # TODO format state + shape for DQN model
        return new_state, reward, done, info

    def render(self):
        
        for i, row in enumerate(self.state):
            for j, cell in enumerate(row):

                color = Color.BLACK if cell == 0 else Color.GREEN

                rect = pg.Rect(self.margin_left + j * self.cell_size, 
                               self.margin_top + i * self.cell_size, 
                               self.cell_size, 
                               self.cell_size)

                pg.draw.rect(self.screen, color, rect, 0)
                pg.draw.rect(self.screen, Color.GRAY, rect, 1)

        for block in self.current_shape:

            rect = pg.Rect(self.margin_left + block[1] * self.cell_size, 
                            self.margin_top + block[0] * self.cell_size, 
                            self.cell_size, 
                            self.cell_size)

            pg.draw.rect(self.screen, Shape.COLORS[4], rect, 0)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        pg.display.update()

if __name__ == "__main__":
    from play import main
    main()