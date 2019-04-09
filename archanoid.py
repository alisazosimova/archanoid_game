import pygame
import sys

pygame.init()

black = (0, 0, 0)
white = (255, 255, 255)
screen_hight = 600
screen_width = 600
center_x = int(screen_width / 2)

screen = pygame.display.set_mode((screen_width, screen_hight))

class Line:

    STATE_MOVING_LEFT = 'left'
    STATE_MOVING_RIGHT = 'right'
    STATE_STILL = 'still'

    def __init__(self):
        self.offset_x = 35
        self.offset_y = 10
        self.x1 = center_x - self.offset_x
        self.x2 = center_x + self.offset_x
        self.y = screen_hight - self.offset_y
        self.width = 5
        self.line_color = 190, 190, 255
        self.speed = 6
        self.state = Line.STATE_STILL


    def draw(self, screen):
        pygame.draw.line(screen, self.line_color, (self.x1, self.y), (self.x2, self.y), self.width)


    def move_left(self):
        self.x1 -= self.speed
        self.x2 -= self.speed
        self.state = Line.STATE_MOVING_LEFT

    def move_right(self):
        self.x1 += self.speed
        self.x2 += self.speed   
        self.state = Line.STATE_MOVING_RIGHT

line = Line()

class Key:

    def __init__(self):
        self.left = pygame.K_LEFT
        self.right = pygame.K_RIGHT
        self.down = pygame.KEYDOWN
        self.esc = pygame.K_ESCAPE
        self.space = pygame.K_SPACE

key = Key() 

class Brick:
    WIDTH = 50
    HIGHT = 20

    def __init__(self, top_x=0, top_y=0):
        self.yellow = 255, 255, 0
        self.blue = 150, 190, 255
        self.top_x = top_x
        self.top_y = top_y
            

    def draw(self, screen):
        pygame.draw.rect(screen, self.yellow, ((self.top_x, self.top_y), (Brick.WIDTH, Brick.HIGHT)))
    
class BrickManager:

    def __init__(self):
        self.number_of_bricks = int(screen_width / Brick.WIDTH)

        self.bricks = []


        for column in range(self.number_of_bricks):
            brick_top_x = column * (Brick.WIDTH + 1)
            y = Brick.HIGHT
            offset_x = Brick.WIDTH / 2
            for row in range(5):
                if row%2 == 0:
                    self.bricks.append(Brick(brick_top_x, row * (y + 1)))
                else:
                    if column < self.number_of_bricks - 1:
                        self.bricks.append(Brick(brick_top_x + offset_x, row * (y + 1)))


    def draw(self, screen):
        for b in self.bricks:
            b.draw(screen)
        

bm = BrickManager()

class BigBall:

    def __init__(self):
        self.color = white
        self.x = center_x
        self.offset_y = int(screen_hight - 15)
        self.radius = 3
        self.rect = pygame.Rect(center_x, screen_hight - 15, 3, 3)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.rect.x, self.rect.y), self.radius)

    def move(self):
        self.rect.y -= 1

ball = BigBall()

"""
#this is not working properly - ball moves after the line once it's fired

class BigBallManager:

    def move_with_line(self):
        if line.state == Line.STATE_MOVING_RIGHT:
            ball.rect.x += line.speed
        if line.state == Line.STATE_MOVING_LEFT:
            ball.rect.x -= line.speed

    def set_still(self):
        line.state = Line.STATE_STILL
"""
  
#import ipdb; ipdb.set_trace()

bbm = BigBallManager()

all_instances = [line, key, bm, ball, bbm]
always_moving_instances = []

while True:
    
    screen.fill(black)
    line.draw(screen)
    bm.draw(screen)
    ball.draw(screen)

    for instance in always_moving_instances:
        instance.move()      

    pygame.time.Clock().tick(500)
    pygame.display.update()

    keys = pygame.key.get_pressed()
    if keys[key.left]:
        line.move_left()

    elif keys[key.right]:
        line.move_right()

    elif not keys[key.left] or keys[key.right]:
        pass
      
    if keys[key.space]:
        always_moving_instances.append(ball)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == key.down:
            if event.key == key.esc:
                pygame.quit()
                sys.exit()
            