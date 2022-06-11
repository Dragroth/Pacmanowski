import pygame, os
import game_module as gm

os.environ['SDL_VIDEO_CENTERED'] = '1'  # centrowanie okna

pygame.init()

# ustwienia ekranu i gry
screen = pygame.display.set_mode(gm.SIZESCREEN)
time = pygame.time.Clock()


# klasa gracza
class Player(pygame.sprite.Sprite):
    def __init__(self, file_image):
        super().__init__()
        self.image = file_image
        self.rect = self.image.get_rect()
        self.movement_x = 0
        self.movement_y = 0
        self.press_left = False
        self.press_right = False
        self.rotate_left = False
        self.level = None
        self._count = 0


    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def turn_right(self):
        self.rotate_left = False
        self.movement_x = 6

    def turn_left(self):
        self.rotate_left = True
        self.movement_x = -6

    def stop(self):
        self.movement_x = 0

    def jump(self):
        self.rect.y += 2
        colliding_platforms = pygame.sprite.spritecollide(
            self, self.level.set_of_platforms, False)
        self.rect.y -= 2
        if colliding_platforms:
            self.movement_y = -15

    def update(self):
        #grawitacja
        self._gravitation()


        # -- ruch w poziomie --
        self.rect.x += self.movement_x

        #animacja
        if self.movement_x > 0:
            self._move(gm.PLAYER_WALK_LIST_R)
        if self.movement_x < 0:
            self._move(gm.PLAYER_WALK_LIST_L)

        # wykrywanie kolizji

        colliding_platforms = pygame.sprite.spritecollide(
            self, self.level.set_of_platforms, False)

        for p in colliding_platforms:
            if self.movement_x > 0:
                self.rect.right = p.rect.left
            if self.movement_x < 0:
                self.rect.left = p.rect.right

        # -- ruch w pionie --
        self.rect.y += self.movement_y

        colliding_platforms = pygame.sprite.spritecollide(
            self, self.level.set_of_platforms, False)

        for p in colliding_platforms:
            if self.movement_y > 0:
                self.rect.bottom = p.rect.top
            if self.movement_y < 0:
                self.rect.top = p.rect.bottom
            self.movement_y = 0

        # animacja gdy spadamy i skakamy
        if self.movement_y < 0:
            if self.rotate_left:
                self.image = gm.PLAYER_JUMP_L
            else:
                self.image = gm.PLAYER_JUMP_R
        elif self.movement_y > 0:
            if self.rotate_left:
                self.image = gm.PLAYER_FALL_L
            else:
                self.image = gm.PLAYER_FALL_R
        elif self.movement_x == 0:
            if self.rotate_left:
                self.image = gm.PLAYER_STAND_L
            else:
                self.image = gm.PLAYER_STAND_R



    def get_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                self.press_right = True
                self.turn_right()
            if event.key == pygame.K_LEFT:
                self.press_left = True
                self.turn_left()
            if event.key == pygame.K_UP:
                self.jump()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                if self.press_left:
                    self.turn_left()
                else:
                    self.stop()
                    self.image = gm.PLAYER_STAND_R
                self.press_right = False
            if event.key == pygame.K_LEFT:
                if self.press_right:
                    self.turn_right()
                else:
                    self.stop()
                    self.image = gm.PLAYER_STAND_L
                self.press_left = False


    def _move(self, image_list):
        self.image = image_list[self._count//4]
        self._count = (self._count + 1) % 32

    def _gravitation(self):
        if self.movement_y == 0:
            self.movement_y = 2
        else:
            self.movement_y += 0.35

#klasa platformy statycznej
class Platform(pygame.sprite.Sprite):
    def __init__(self, image_list, width, height, pos_x, pos_y):
        super().__init__()
        self.image_list = image_list
        self.width = width
        self.height = height
        self.image = pygame.Surface([self.width, self.height])
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y

    def draw(self, surface):
        # self.image.fill(gm.DARKGREEN)
        # surface.blit(self.image, self.rect)

        if self.width == 70:
            surface.blit(self.image_list[0], self.rect)
        else:
            surface.blit(self.image_list[1], self.rect)
            for i in range(70, self.width - 70, 70):
                surface.blit(self.image_list[2], [self.rect.x + i, self.rect.y])
            surface.blit(self.image_list[3], [self.rect.x + self.width - 70, self.rect.y])

class Level:
    def __init__(self, player):
        self.player = player
        self.set_of_platforms = set()

    def draw(self, surface):
        for platform in self.set_of_platforms:
            platform.draw(surface)

class Level_1(Level):
    def __init__(self, player = None):
        super().__init__(player)
        self._create_static_platfroms()

    def _create_static_platfroms(self):
        platforms_cor = [[210, 70, 200, 300],
                         [70, 70, 800, 400],
                         [15*70, 70, 0, gm.HEIGHT-70]]

        for cor in platforms_cor:
            self.set_of_platforms.add(Platform(gm.GRASS_LIST, *cor))






#konkretyzacja obiektów
player = Player(gm.PLAYER_STAND_R)
player.rect.center = screen.get_rect().center
current_level = Level_1(player)
player.level = current_level


open_window = True

#pętla gry
while open_window:
    screen.fill(gm.LIGHTBLUE)

    #pętle zdarzeń
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            open_window = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                open_window = False
        player.get_event(event)

    #aktualizacja i rysowanie obiektów
    player.update()
    player.draw(screen)
    current_level.draw(screen)

    #aktualizacja okna gry
    pygame.display.flip()
    time.tick(30)



pygame.quit()