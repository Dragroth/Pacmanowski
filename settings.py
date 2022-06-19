import os, pygame

WIDTH, HEIGHT = 610, 670
TOP_BOTTOM_MARGIN = 50
MAZE_WIDTH, MAZE_HEIGHT = WIDTH-TOP_BOTTOM_MARGIN, HEIGHT-TOP_BOTTOM_MARGIN

ROWS = 30
COLS = 28

CELL_WIDTH = MAZE_WIDTH//COLS
CELL_HEIGHT = MAZE_HEIGHT//ROWS

FPS = 60
STEP = 1


DEBUG_MODE = False
PRINT_WALLS = False

# Colors 
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (170,170,0)
ORANGE = (170, 130, 58)
AQUAMARINE = (33, 137, 156)
GREY = (105, 105, 105)
LIGHTGREY = (140, 140, 140)

PLAYER_COLOR = YELLOW

# Fonts
START_FONT = 'arial black'



path = os.path.join(os.pardir, 'Pacmanowski/assets/images')
file_names = sorted(os.listdir(path))


# Animations
for file_name in file_names:
    image_name = file_name[:-4]
    globals()[image_name] = pygame.image.load(os.path.join(path, file_name))


# Music

MAIN_MENU_MUSIC = ["assets/sounds/budowa.wav", "assets/sounds/teleportki.wav", "assets/sounds/dziki_zachod.wav", "assets/sounds/miasto.wav"]
LEVEL_MUSIC = ["assets/sounds/podziemia.wav", "assets/sounds/lotnasmoku.wav", "assets/sounds/lotnamiotle.wav"]


PLAYER_WALK_LIST_R = [PLAYER_STAND, PLAYER_WALK_R_1, PLAYER_WALK_R_2, PLAYER_WALK_R_1]
PLAYER_WALK_LIST_L = [PLAYER_STAND, PLAYER_WALK_L_1, PLAYER_WALK_L_2, PLAYER_WALK_L_1]
PLAYER_WALK_LIST_T = [PLAYER_STAND, PLAYER_WALK_T_1, PLAYER_WALK_T_2, PLAYER_WALK_T_1]
PLAYER_WALK_LIST_B = [PLAYER_STAND, PLAYER_WALK_B_1, PLAYER_WALK_B_2, PLAYER_WALK_B_1]
PLAYER_STAND_LIST = [PLAYER_STAND]
