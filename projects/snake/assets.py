from constants import *
from random import randint


class Food():

    def __init__(self, pg, screen):
        self.x = None
        self.y = None
        self.pg = pg
        self.screen = screen

    def new(self, snake):

        self.x = randint(F_RADIUS, WIDTH - F_RADIUS) // S_THICK * S_THICK + F_RADIUS
        self.y = randint(F_RADIUS, HEIGHT - F_RADIUS) // S_THICK * S_THICK + F_RADIUS

        while (self.x - F_RADIUS, self.y - F_RADIUS) in snake:
            self.x = randint(F_RADIUS, WIDTH - F_RADIUS) // S_THICK * S_THICK + F_RADIUS
            self.y = randint(F_RADIUS, HEIGHT - F_RADIUS) // S_THICK * S_THICK + F_RADIUS
        self.display('white')

    def display(self, color):
        self.pg.draw.circle(self.screen, self.pg.Color(color), (self.x, self.y), F_RADIUS)


class Snake():

    init_length = 10

    def __init__(self, x, y, pg, screen):
        self.x = x
        self.y = y
        self.pg = pg
        self.screen = screen
        self.head = (self.x, self.y)
        self.vx = 1
        self.vy = 0
        self.body = [self.head]

        for i in range(1, self.init_length):
            x = self.x - (i * S_THICK * self.vx)
            y = self.y - (i * S_THICK * self.vy)
            self.body.append((x, y))

    def display(self, color='white', body=None):
        if body is None:
            for coord in self.body:
                x = coord[0]
                y = coord[1]
                self.pg.draw.rect(self.screen, self.pg.Color(color),
                                  (x, y, S_THICK, S_THICK)
                                  )
            return

        x = body[0]
        y = body[1]
        self.pg.draw.rect(self.screen, self.pg.Color(color),
                          (x, y, S_THICK, S_THICK)
                          )

    def move_snake(self):
        if self.vx == 0 and self.vy == 0:
            return

        self.display(color='black', body=self.body.pop())
        self.x += self.vx * S_THICK
        self.y += self.vy * S_THICK
        self.head = (self.x, self.y)
        self.body.insert(0, self.head)
        self.display(body=self.head)

    def change_direction(self, dir):
        # restrict moving in the opposite direction to current direction
        if self.vx == -dir[0] or self.vy == -dir[1]:
            return
        self.vx = dir[0]
        self.vy = dir[1]

    def check_eat(self, foodx, foody):
        if self.x + F_RADIUS == foodx and self.y + F_RADIUS == foody:
            return True

    def eat(self):
        self.body.append(self.body[-1])

    def game_over(self):
        # need to take into account the thickness of body
        if self.x < 0 or self.x + S_THICK > WIDTH or \
                self.y < 0 or self.y + S_THICK > HEIGHT or \
                self.head in self.body[1:]:
            self.vx, self.vy = (0, 0)
            return True
