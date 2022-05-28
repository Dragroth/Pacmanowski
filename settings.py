from pygame.math import Vector2 as vec

# screen resolution, change if you need it
WIDTH, HEIGHT = 610, 670
TOP_BOTTOM_MARGIN = 50
MAZE_WIDTH, MAZE_HEIGHT = WIDTH-TOP_BOTTOM_MARGIN, HEIGHT-TOP_BOTTOM_MARGIN
FPS = 60


# colors 
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (170,170,0)
ORANGE = (170, 130, 58)
AQUAMARINE = (33, 137, 156)
GREY = (105, 105, 105)

PLAYER_COLOR = YELLOW



# fonts
START_TEXT_SIZE = 16
START_FONT = 'arial black'

# player settings 

PLAYER_START_POS = vec(1,10)

# enemy settings