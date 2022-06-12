import pygame, random
from entities.entity import *

vector = pygame.math.Vector2

class Enemy(Entity):
    """An entity that chases player and tries to catch them"""
    def  __init__(self, app, level, init_position, number):
        super().__init__(app, level, init_position)
        self.radius = CELL_WIDTH//2.3
        # Used to identify an enemy
        self.number = number
        self.color = self.set_color()
        # Used to allow different movement patterns in enemy
        self.personality = self.set_personality()
        # Used as a place that an enemy will try to reach
        self.target = None
        self.speed = self.set_speed()

    def update(self):
        # Updates target every tick
        self.target = self.set_target()
        # If the enemy has not reached it's target
        if self.target != self.grid_position:
            # It will move in a direction of a target
            self.pixel_position += self.direction * self.speed
            # And if it's in the middle of a grid
            if self.stay_in_grid():
                # It will try to change direction
                self.move()
        super().update()

    def draw(self):
        pygame.draw.circle(self.app.screen, self.color, (int(self.pixel_position.x), int(self.pixel_position.y)) , self.radius)


    def set_speed(self):
        """Setting movement speed based on personality type"""
        if self.personality in ("speedy", "scared"):
            speed = 2
        else:
            speed = 1
        return speed

    def set_target(self):
        """Sets target based on its personality"""
        # These enemies will try to reach player position
        if self.personality == "speedy" or self.personality == "slow":
            return self.level.player.grid_position
        # These enemies will run to a quarter of a gridmap that is furthest away from the player
        else:
            # If the player is in the bottom right corner
            if self.level.player.grid_position[0] > COLS//2 and self.level.player.grid_position[1] > ROWS//2:
                # The enemy will try to reach top left corner
                return vector(1, 1)
            if self.level.player.grid_position[0] > COLS//2 and self.level.player.grid_position[1] < ROWS//2:
                return vector(1, ROWS-2)
            if self.level.player.grid_position[0] < COLS//2 and self.level.player.grid_position[1] > ROWS//2:
                return vector(COLS-2, 1)
            else:
                return vector(COLS-2, ROWS-2)


    def move(self):
        """Changes direction based on set personality pattern"""
        if self.personality == "random":
            self.direction = self.get_random_direction()
        elif self.personality == "slow":
            self.direction = self.get_path_direction(self.target)
        elif self.personality == "speedy":
            self.direction = self.get_path_direction(self.target)
        elif self.personality == "scared":
            self.direction = self.get_path_direction(self.target)

    def get_path_direction(self, target):
        """Gets vector of a direction that an entity should follow to get one step closer to the target"""
        # It uses next cell in path function to accomplish that
        next_cell = self.find_next_cell_in_path(target)
        xdir = next_cell[0] - self.grid_position[0]
        ydir = next_cell[1] - self.grid_position[1]
        return vector(xdir, ydir)

    def find_next_cell_in_path(self, target):
        """Gets the cell that an enemy should go to, to get one step closer to the target"""
        # It uses Breadth first search algortihm to accomplish that
        path = self.BFS([int(self.grid_position.x), int(self.grid_position.y)], [int(self.target[0]), int(self.target[1])])
        return path[1]

    def BFS(self, start, target):
        """Uses Breadth First Traversal algorithm to find the shortest path from start position (grid) to target position (grid)"""
        # Generated 2D grid to use as a calculation base
        grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        # Puts 0 in positions where walls are
        for cell in self.level.walls:
            if cell.x < 28 and cell.y < 30:
                grid[int(cell.y)][int(cell.x)] = 1

        # Three lists that are used to perform BFS
        queue = [start]
        path = []
        visited = []
        # Main loop
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
                            # If neighbour is a valid cell
                            next_cell = [neighbour[0] + current[0], neighbour[1] + current[1]]
                            # And it wasn't yet visited
                            if next_cell not in visited:
                                # And it's not a wall
                                if grid[next_cell[1]][next_cell[0]] != 1:
                                    # We enqueqe it as a next cell to try
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
        """Gets random direction"""
        while True:
            number = random.randint(0,3)
            if number == 0:
                x_dir, y_dir = 1,0
            elif number == 1:
                x_dir, y_dir = 0,1
            elif number == 2:
                x_dir, y_dir = -1,0
            else:
                x_dir, y_dir = 0,-1
            next_pos = vector(self.grid_position.x + x_dir, self.grid_position.y + y_dir)
            if next_pos not in self.level.walls:
                break
        return vector(x_dir, y_dir)

    def set_color(self):
        """Sets color based on enemy number"""
        if self.number == 0:
            return BLUE
        elif self.number == 1:
            return YELLOW
        elif self.number == 2:
            return RED
        elif self.number == 3:
            return ORANGE

    def set_personality(self):
        """Sets personality based on enemy number"""
        if self.number == 0:
            return "speedy"
        elif self.number == 1:
            return "slow"
        elif self.number == 2:
            return "random"
        else:
            return "scared"