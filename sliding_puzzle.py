import pygame as pg

TILESIZE = 64
BLACK = (0, 0, 0)
NAVY = pg.Color("blue")
LIGHTBLUE = pg.Color("lightblue")
BOARD_SIZE = [4, 5]


class Block:
    def __init__(self, pos, size):
        self.x = pos[0]
        self.y = pos[1]
        self.size = size
        self.indent = 10

        self.coords = []
        self.set_coords()

        self.selected = False

    def draw(self, display):
        if not self.selected:
            colour = NAVY
        else:
            colour = LIGHTBLUE
        pg.draw.rect(display,
                     colour,
                     (self.x*TILESIZE+self.indent,
                      self.y*TILESIZE+self.indent,
                      self.size[0]*TILESIZE-2*self.indent,
                      self.size[1]*TILESIZE-2*self.indent))

    def set_coords(self):
        self.coords = []
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                self.coords.append([self.x + x, self.y + y])

    def move_dir(self, direction, blocks):
        blocked = False
        if direction == "right":
            # check if out of board
            if self.x + self.size[0] == BOARD_SIZE[0]:
                blocked = True
            # check if block in way
            for block in blocks:
                if not block.selected:
                    for coord in block.coords:
                        if [coord[0] - 1, coord[1]] in self.coords:
                            blocked = True
            if not blocked:
                self.x += 1

        if direction == "left":
            # check if out of board
            if self.x == 0:
                blocked = True
            # check if block in way
            for block in blocks:
                if not block.selected:
                    for coord in block.coords:
                        if [coord[0] + 1, coord[1]] in self.coords:
                            blocked = True
            if not blocked:
                self.x -= 1

        if direction == "up":
            # check if out of board
            if self.y == 0:
                blocked = True
            # check if block in way
            for block in blocks:
                if not block.selected:
                    for coord in block.coords:
                        if [coord[0], coord[1] + 1] in self.coords:
                            blocked = True
            if not blocked:
                self.y -= 1

        if direction == "down":
            # check if out of board
            if self.y + self.size[1] == BOARD_SIZE[1]:
                blocked = True
            # check if block in way
            for block in blocks:
                if not block.selected:
                    for coord in block.coords:
                        if [coord[0], coord[1] - 1] in self.coords:
                            blocked = True
            if not blocked:
                self.y += 1

        self.set_coords()


def select_block(blocks):
    mouse_pos = pg.mouse.get_pos()
    mouse_coords = [int(mouse_pos[0]/TILESIZE), int(mouse_pos[1]/TILESIZE)]
    block_id = 0

    for i, block in enumerate(blocks):
        if mouse_coords in block.coords:
            block_id = i

    for i, block in enumerate(blocks):
        if i == block_id:
            block.selected = True
        else:
            block.selected = False



pg.init()
screen = pg.display.set_mode((TILESIZE*4, TILESIZE*5))
clock = pg.time.Clock()

running = True
blocks = [Block((0, 0), (2, 2)),
          Block((2, 0), (2, 1)),
          Block((2, 1), (1, 2)),
          Block((3, 1), (1, 2)),
          Block((0, 3), (1, 2)),
          Block((1, 3), (2, 1)),
          Block((1, 4), (2, 1)),
          Block((3, 3), (1, 1)),
          Block((3, 4), (1, 1))]

id = 0
blocks[id].selected = True
print(blocks[id].coords)

while running:
    dir = None
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RIGHT:
                dir = "right"
            if event.key == pg.K_LEFT:
                dir = "left"
            if event.key == pg.K_UP:
                dir = "up"
            if event.key == pg.K_DOWN:
                dir = "down"
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                select_block(blocks)

    for i, block in enumerate(blocks):
        if block.selected:
            id = i

    blocks[id].move_dir(dir, blocks)

    screen.fill(BLACK)
    for block in blocks:
        block.draw(screen)
    pg.display.flip()
