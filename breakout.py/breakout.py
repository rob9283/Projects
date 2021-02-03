#breakout

import pygame
import sys
import math
import random

from pygame.cursors import sizer_y_strings

pygame.init()
pygame.display.set_caption("Breakout by Rob")
clock = pygame.time.Clock()

WIDTH = 1200
HEIGHT = 800

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255,0,0)
BLUE = (0,0,255)

#create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))

class Paddle():
    def __init__(self):
        self.x = WIDTH/2
        self.y = 700
        self.dx = 0
        self.width = 200
        self.height = 25
        self.score = 0

    def render(self):
        pygame.draw.rect(screen, WHITE, pygame.Rect(self.x-self.width/2, self.y-self.height/2, self.width,self.height))

    def left(self):
        self.dx = -12
    
    def right(self):
        self.dx = 12
        
    def move(self):
        self.x += self.dx
    
    def stop(self):
        self.dx = 0

        #border collision
        if self.x < 0 + self.width/2.0:
            self.x = 0 + self.width/2.0
            self.dx = 0
        elif self.x > WIDTH - self.width/2.0:
            self.x = WIDTH - self.width/2.0
            self.dx = 0

    def is_aabb_collision(self,other):
        x_collision = (math.fabs(self.x - other.x) *2 < self.width + other.width)
        y_collision = (math.fabs(self.y - other.y) * 2 < (self.height + other.height))
        return (x_collision and y_collision)



class Ball():
    def __init__(self):
        self.x = WIDTH/2
        self.y = HEIGHT/2
        self.dx = 6
        self.dy = -6
        self.width = 20
        self.height = 20

    def render(self):
        pygame.draw.rect(screen, WHITE, pygame.Rect(self.x-self.width/2, self.y-self.height/2, self.width,self.height))

    def left(self):
        self.dx = -12
    
    def right(self):
        self.dx = 12

    def reset(self):
        sadtrombone_sound.play()
        self.x = WIDTH/2.0
        self.y = HEIGHT/2.0
        self.dx = 6
        self.dy = -6

    def move(self):
        self.x += self.dx
        self.y += self.dy

        #border collision
        if self.x < 0 + self.width/2.0:
            self.dx = -self.dx
        elif self.x > WIDTH - self.width/2.0:
            self.dx = -self.dx
        #border collision
        if self.y < 0 + self.height/2.0:
            self.dy = -self.dy
        elif self.y > HEIGHT - self.height/2.0:
            self.reset()

    def is_aabb_collision(self,other):
        x_collision = (math.fabs(self.x - other.x) *2 < self.width + other.width)
        y_collision = (math.fabs(self.y - other.y) * 2 < (self.height + other.height))
        return (x_collision and y_collision)


class Brick():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 75
        self.height = 35
        self.color = "WHITE"

    def render(self):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.x-self.width/2, self.y-self.height/2, self.width,self.height))


#create fonts
pygame.font.init
font = pygame.font.SysFont("arial", 24)

#create sounds
bounce_sound = pygame.mixer.Sound("bounce.wav")
sadtrombone_sound = pygame.mixer.Sound("sadtrombone.wav")

#create objects
paddle = Paddle()
ball = Ball()

bricks = []
for y in range(100, 375, 36):
    color = random.choice([WHITE, GREEN, RED, BLUE])
    for x in range(25, 1200, 76):
        bricks.append(Brick(x, y))
        bricks[-1].color = color   #refers to last item, sets color because Brick class doesn't accept color as argument


#game loop

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    
    #key bindings    
    if event.type== pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            paddle.left()
        elif event.key == pygame.K_RIGHT:
            paddle.right()
    else:
        paddle.stop()

    paddle.move()
    ball.move()

 
    if ball.is_aabb_collision(paddle):
        ball.dy = -ball.dy
        ball.dx = (ball.x - paddle.x) /5
        bounce_sound.play()

    for brick in bricks:
        if ball.is_aabb_collision(brick):
            ball.dy = -ball.dy
            brick.x = 12000
            paddle.score += 10
            bounce_sound.play()

    
    screen.fill(BLACK)

    paddle.render()
    ball.render()
    for brick in bricks:
        brick.render()

    score_surface = font.render(f"Score: {paddle.score}", True, WHITE)
    screen.blit(score_surface, (WIDTH/2.0, 25))












    #flip the display
    pygame.display.flip()

    #set the FPS
    clock.tick(30)
