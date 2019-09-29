import pygame as pg

# board components
TILE_SIZE = 64
BOARD_SIZE = [4, 5]

# colours
BLACK = (0, 0, 0)
BLUE = pg.Color("blue")
LIGHTBLUE = pg.Color("lightblue")
WHITE = pg.Color("white")

# pygame setup
pg.init()
pg.font.init()
screen = pg.display.set_mode((TILE_SIZE*BOARD_SIZE[0], TILE_SIZE*BOARD_SIZE[1]))  # screen is size of board
clock = pg.time.Clock()
font = pg.font.SysFont('comicsans', 48, True)


class Block:
    """A 2 dimensional 'block' that moves within the constraints of the board, given the users input"""
    def __init__(self, pos, size):
        # position and size information
        self.x = pos[0]
        self.y = pos[1]
        self.size = size
        self.indent = 10  # used for drawing shape with clearer borders

        # if selected then this block can move
        self.selected = False

    def draw(self, display):
        """Draws block to display using the specified indent for visibility"""
        if not self.selected:
            colour = BLUE
        else:
            colour = LIGHTBLUE
        pg.draw.rect(display,
                     colour,
                     (self.x*TILE_SIZE+self.indent,
                      self.y*TILE_SIZE+self.indent,
                      self.size[0]*TILE_SIZE-2*self.indent,
                      self.size[1]*TILE_SIZE-2*self.indent))

    @property
    def coords(self):
        """creates a list of coordinates that the block occupies on the board"""
        coords = []
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                coords.append([self.x + x, self.y + y])
        return coords

    def move_dir(self, direction, blocks):
        """move the block in the direction only if the block has space to move into"""
        blocked = False
        if direction == "right":
            # check if moving out of board
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
            # check if moving out of board
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
            # check if moving out of board
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
            # check if moving out of board
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


def select_block(blocks, id):
    """using id set block selected property to True in list and set all other blocks to False"""
    for block in blocks:
        block.selected = False
    blocks[id].selected = True


def get_block_clicked(blocks, id):
    """get mouse position and find block that mouse is on"""
    mouse_pos = pg.mouse.get_pos()
    mouse_coords = [int(mouse_pos[0]/TILE_SIZE), int(mouse_pos[1]/TILE_SIZE)]
    for i, block in enumerate(blocks):
        if mouse_coords in block.coords:
            id = i
    return id


win_img = font.render("You Win!", True, WHITE)

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

selected = 0
select_block(blocks, selected)  # only 1 block can be selected

while running:
    direction = None
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            # move block in direction
            if event.key == pg.K_RIGHT:
                direction = "right"
            if event.key == pg.K_LEFT:
                direction = "left"
            if event.key == pg.K_UP:
                direction = "up"
            if event.key == pg.K_DOWN:
                direction = "down"
            # tab through block selection
            if event.key == pg.K_TAB:
                selected += 1
                if selected >= len(blocks):
                    selected = 0
            # reset board
            if event.key == pg.K_r:
                blocks = [Block((0, 0), (2, 2)),
                          Block((2, 0), (2, 1)),
                          Block((2, 1), (1, 2)),
                          Block((3, 1), (1, 2)),
                          Block((0, 3), (1, 2)),
                          Block((1, 3), (2, 1)),
                          Block((1, 4), (2, 1)),
                          Block((3, 3), (1, 1)),
                          Block((3, 4), (1, 1))]
                selected = 0
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                selected = get_block_clicked(blocks, selected)

    select_block(blocks, selected)

    blocks[selected].move_dir(direction, blocks)

    screen.fill(BLACK)
    for block in blocks:
        block.draw(screen)
    # check win condition and draw message if met
    if blocks[0].x == 0 and blocks[0].y == 3:
        screen.blit(win_img, (2 * TILE_SIZE - win_img.get_width() / 2, 2 * TILE_SIZE))
    pg.display.flip()
