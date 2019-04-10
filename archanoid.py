import pygame
import sys

pygame.init()

black = (0, 0, 0)
white = (255, 255, 255)
screen_height = 600
screen_width = 600
center_x = int(screen_width / 2)

screen = pygame.display.set_mode((screen_width, screen_height))

class Line:

    STATE_MOVING_LEFT = 'left'
    STATE_MOVING_RIGHT = 'right'
    STATE_STILL = 'still'

    def __init__(self):
        self.color = 190, 190, 255
        self.speed = 6
        self.state = Line.STATE_STILL
        self.rect = pygame.Rect(center_x - 35, screen_height - 10, 70, 5)


    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.rect.x, self.rect.y, self.rect.width, self.rect.height))


    def move_left(self):
        self.rect.x -= self.speed
        self.state = Line.STATE_MOVING_LEFT

    def move_right(self):
        self.rect.x += self.speed
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
    HEIGHT = 20

    def __init__(self, top_x=0, top_y=0):
        self.yellow = 255, 255, 0
        self.blue = 150, 190, 255
        self.rect = pygame.Rect(top_x, top_y, Brick.WIDTH, Brick.HEIGHT)
            

    def draw(self, screen):
        pygame.draw.rect(screen, self.yellow, ((self.rect.x, self.rect.y), (self.rect.width, self.rect.height)))
    
class BrickManager:

    def __init__(self):
        self.number_of_bricks = int(screen_width / Brick.WIDTH)

        self.bricks = []


        for column in range(self.number_of_bricks):
            brick_top_x = column * (Brick.WIDTH + 1)
            y = Brick.HEIGHT
            offset_x = Brick.WIDTH / 2
            for row in range(2):
                if row%2 == 0:
                    self.bricks.append(Brick(brick_top_x, row * (y + 1)))
                else:
                    if column < self.number_of_bricks - 1:
                        self.bricks.append(Brick(brick_top_x + offset_x, row * (y + 1)))


    def draw(self, screen):
        for b in self.bricks:
            b.draw(screen)
        

brickman = BrickManager()

class Ball:

    def __init__(self):
        self.color = white
        self.rect = pygame.Rect(center_x, screen_height - 15, 3, 3)
        self.is_moving_up = True
        self.is_inside_screen = True

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.rect.x, self.rect.y), self.rect.width)

    def move(self):
        if self.is_moving_up == True:
            self.rect.y -= 2
        if self.is_moving_up == False:
            self.rect.y +=2


    def change_state(self, state):
        if self.is_moving_up == True:
            self.is_moving_up = False
        else:
            self.is_moving_up = True


    def check_collision(self, brick):
        return self.rect.colliderect(brick.rect)

    def check_borders(self):
        if self.rect.x < 0 or self.rect.x > screen_width or self.rect.y < 0:
            self.change_state(self.is_moving_up)
            
           
ball = Ball()

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

bbm = BigBallManager()

"""
  
#import ipdb; ipdb.set_trace()mmm

all_instances = [line, key, brickman, ball]
always_moving_instances = []

while True:
    
    screen.fill(black)
    line.draw(screen)
    brickman.draw(screen)
    ball.draw(screen)
    ball.check_borders()
    
    print(ball.rect)
    
    for instance in always_moving_instances:
        instance.move()

    for item in brickman.bricks:
        if ball.check_collision(item):
            brickman.bricks.remove(item)
            ball.change_state(ball.is_moving_up)

    if ball.check_collision(line):
        ball.change_state(ball.is_moving_up)


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
            