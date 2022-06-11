import pygame, random
from entities.entity import *

vector = pygame.math.Vector2

class Enemy(Entity):
    def  __init__(self, app, level, init_position, number):
        super().__init__(app, level, init_position)
        self.radius = CELL_WIDTH//2.3
        self.number = number
        self.color = self.set_color()
        self.personality = self.set_personality()
        self.target = None
        self.speed = self.set_speed()

    def update(self):
        self.target = self.set_target()
        if self.target != self.grid_position:
            self.pixel_position += self.direction * self.speed
            if self.stay_in_grid():
                self.move()
        super().update()

    def draw(self):
        pygame.draw.circle(self.app.screen, self.color, (int(self.pixel_position.x), int(self.pixel_position.y)) , self.radius)


    def set_speed(self):
        if self.personality in ("speedy", "scared"):
            speed = 2
        else:
            speed = 1
        return speed

    def set_target(self):
        if self.personality == "speedy" or self.personality == "slow":
            return self.level.player.grid_position
        else:
            if self.level.player.grid_position[0] > COLS//2 and self.level.player.grid_position[1] > ROWS//2:
                return vector(1, 1)
            if self.level.player.grid_position[0] > COLS//2 and self.level.player.grid_position[1] < ROWS//2:
                return vector(1, ROWS-2)
            if self.level.player.grid_position[0] < COLS//2 and self.level.player.grid_position[1] > ROWS//2:
                return vector(COLS-2, 1)
            else:
                return vector(COLS-2, ROWS-2)


    def move(self):
        if self.personality == "random":
            self.direction = self.get_random_direction()
        elif self.personality == "slow":
            self.direction = self.get_path_direction(self.target)
        elif self.personality == "speedy":
            self.direction = self.get_path_direction(self.target)
        elif self.personality == "scared":
            self.direction = self.get_path_direction(self.target)

    def get_path_direction(self, target):
        next_cell = self.find_next_cell_in_path(target)
        xdir = next_cell[0] - self.grid_position[0]
        ydir = next_cell[1] - self.grid_position[1]
        return vector(xdir, ydir)

    def find_next_cell_in_path(self, target):
        path = self.BFS([int(self.grid_position.x), int(self.grid_position.y)], [int(self.target[0]), int(self.target[1])])
        return path[1]

    def BFS(self, start, target):
        grid = [[0 for x in range(28)] for x in range(30)]
        for cell in self.level.walls:
            if cell.x < 28 and cell.y < 30:
                grid[int(cell.y)][int(cell.x)] = 1
        queue = [start]
        path = []
        visited = []
        while queue:
            current = queue[0]
            queue.remove(queue[0])
            visited.append(current)
            if current == target:
                break
            else:
                neighbours = [[0, -1],[1, 0],[0,  1],[-1, 0]]
                for neighbour in neighbours:
                    if neighbour[0] + current[0] >= 0 and neighbour[0] + current[0] < len(grid[0]):
                        if neighbour[1] + current[1] >= 0 and neighbour[1] + current[1] < len(grid):
                            next_cell = [neighbour[0] + current[0], neighbour[1] + current[1]]
                            if next_cell not in visited:
                                if grid[next_cell[1]][next_cell[0]] != 1:
                                    queue.append(next_cell)
                                    path.append({"Current": current, "Next": next_cell})
        shortest = [target]
        while target != start:
            for step in path:
                if step["Next"] == target:
                    target = step["Current"]
                    shortest.insert(0, step["Current"])
        return shortest

    def get_random_direction(self):
        while True:
            number = random.randint(-2,1)
            if number == -2:
                x_dir, y_dir = 1,0
            elif number == -1:
                x_dir, y_dir = 0,1
            elif number == 0:
                x_dir, y_dir = -1,0
            else:
                x_dir, y_dir = 0,-1
            next_pos = vector(self.grid_position.x + x_dir, self.grid_position.y + y_dir)
            if next_pos not in self.level.walls:
                break
        return vector(x_dir, y_dir)

    def set_color(self):
        if self.number == 0:
            return BLUE
        elif self.number == 1:
            return YELLOW
        elif self.number == 2:
            return RED
        elif self.number == 3:
            return ORANGE

    def set_personality(self):
        if self.number == 0:
            return "speedy"
        elif self.number == 1:
            return "slow"
        elif self.number == 2:
            return "random"
        else:
            return "scared"

    