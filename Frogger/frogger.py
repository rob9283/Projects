#frogger
#by Rob

import turtle
import math
import time
import random

wn = turtle.Screen()
wn.title("Frogger by Rob")
wn.setup(600,800)
wn.bgcolor("black")
wn.tracer(0)
wn.cv._rootwindow.resizable(False,False)   #prevent window resizing

#Register Shape
shapes = ["frog.gif", "car_left.gif", "car_right.gif", "log_full.gif", "turtle_left.gif",
    "turtle_right.gif", "turtle_left_half.gif","turtle_right_half.gif", "turtle_submerged.gif",
    "goal.gif", "frog_home.gif"]
for shape in shapes:
    wn.register_shape(shape)

pen = turtle.Turtle()
pen.speed(0)
pen.hideturtle()
pen.penup()


# Create Classes

class Sprite():
    def __init__(self, x, y, width, height, image):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = image

    def render(self, pen):
        pen.goto(self.x, self.y)
        pen.shape(self.image)
        pen.stamp()

    def is_collision(self, other):
        #axis-alligned bounding box, stolen from stack overflow
        x_collision = (math.fabs(self.x - other.x) * 2) < (self.width + other.width)
        y_collision = (math.fabs(self.y - other.y) * 2) < (self.height + other.height)
        return (x_collision and y_collision)

    def update(self):
        pass


class Player(Sprite):
    def __init__(self, x, y, width, height,image):
        Sprite.__init__(self, x, y, width, height,image)
        self.dx = 0

    def up(self):
        self.y += 50

    def down(self):
        self.y -= 50

    def left(self):
        self.x -= 50

    def right(self):
        self.x += 50

    def update(self):
        self.x += player.dx

        #border checking
        if self.x < -320 or self.x > 320:
            self.x=0
            self.y=-300

class Home(Sprite):
    def __init__(self, x, y, width, height,image):
        Sprite.__init__(self, x, y, width, height,image)
    




class Car(Sprite):
    def __init__(self, x, y, width, height, image, dx):
        Sprite.__init__(self, x, y, width, height,image,)
        self.dx = dx

    def update(self):
        self.x += self.dx

        #border checking
        if self.x < -400:
            self.x = 400

        if self.x > 400:
            self.x = -400


class Log(Sprite):
    def __init__(self, x, y, width, height, image, dx):
        Sprite.__init__(self, x, y, width, height,image,)
        self.dx = dx

    def update(self):
        self.x += self.dx

        #border checking
        if self.x < -400:
            self.x = 400

        if self.x > 400:
            self.x = -400


class Turtle(Sprite):
    def __init__(self, x, y, width, height, image, dx):
        Sprite.__init__(self, x, y, width, height,image,)
        self.dx = dx
        self.state = "full" #half, submerged
        self.full_time = random.randint(5,10)
        self.half_time = 3
        self.submerged_time = random.randint(4,6)
        self.start_time = time.time()

    def update(self):
        self.x += self.dx

        #border checking
        if self.x < -400:
            self.x = 400

        if self.x > 400:
            self.x = -400

        if self.state=="full":
            if self.dx > 0:
                self.image = "turtle_right.gif"
            else:
                self.image = "turtle_left.gif"
        elif self.state == "halfup" or self.state == "halfdown":
            if self.dx > 0:
                self.image = "turtle_right_half.gif"
            else:
                self.image = "turtle_left_half.gif"
        elif self.state == "submerged":
            self.image = "turtle_submerged.gif"

            

        #timer stuff
        if self.state == "full" and time.time() - self.start_time > self.full_time:
            self.state = "halfdown"
            self.start_time = time.time()
        elif self.state == "halfdown" and time.time() - self.start_time > self.half_time:
            self.state = "submerged"
            self.start_time = time.time()
        elif self.state == "submerged" and time.time() - self.start_time > self.submerged_time:
            self.state = "halfup"
            self.start_time = time.time()
        elif self.state == "halfup" and time.time() - self.start_time > self.half_time:
            self.state = "full"
            self.start_time = time.time()



#Create Objects
player = Player(0, -300, 40, 40, "frog.gif")
car_left = Car(0, -250, 121, 40, "car_left.gif", -.07)
car_right = Car(0, -200, 121, 40, "car_right.gif", .09)
car_left2 = Car(0, -150, 121, 40, "car_left.gif", -.08)
car_right2 = Car(0, -100, 121, 40, "car_left.gif", -.06)
car_left3 = Car(0, -50, 121, 40, "car_left.gif", -.09)
log_left = Log(0, 50, 121, 40, "log_full.gif", -.1)
log_left2 = Log(250, 50, 121, 40, "log_full.gif", -.1)
turtle_right = Turtle(0, 100, 155, 40, "turtle_right.gif", .15)
turtle_right2 = Turtle(200, 100, 155, 40, "turtle_right.gif", .15)
log_left3 = Log(0, 150, 121, 40, "log_full.gif", -.2)
log_left4 = Log(200, 150, 121, 40, "log_full.gif", -.2)
turtle_right3 = Turtle(0, 200, 155, 40, "turtle_left.gif", .08)
turtle_right4 = Turtle(200, 200, 155, 40, "turtle_left.gif", .08)

goal1 = Home(-200, 250, 50, 50, "goal.gif")
goal2 = Home(-100, 250, 50, 50, "goal.gif")
goal3 = Home(0, 250, 50, 50, "goal.gif")
goal4 = Home(100, 250, 50, 50, "goal.gif")
goal5 = Home(200, 250, 50, 50, "goal.gif")


#list sprites
sprites = [car_left, car_right, car_left2, car_right2, car_left3, log_left, log_left2, log_left3, log_left4, turtle_right, turtle_right2, turtle_right3, turtle_right4, goal1, goal2, goal3, goal4, goal5, player]  
#player should be last so renders on top


#keyboard binding
wn.listen()
wn.onkeypress(player.up, "Up")
wn.onkeypress(player.down, "Down")
wn.onkeypress(player.left, "Left")
wn.onkeypress(player.right, "Right")


while True:
    #render
    for sprite in sprites:
        sprite.render(pen)
        sprite.update()
    
    player.dx=0 #reset player moving if was on log or unsubmerged turtle
    for sprite in sprites:
        if player.is_collision(sprite):
            if isinstance(sprite, Car):
                player.x = 0
                player.y = -300
                break
            elif isinstance(sprite,Log):
                player.dx = sprite.dx
                break
            elif isinstance(sprite,Turtle) and sprite.state != "submerged":
                player.dx = sprite.dx
                break
            elif isinstance(sprite, Home):
                player.x=0
                player.y=-300
                sprite.image = "frog_home.gif"
                break
    
            elif player.y > 0:
                player.x = 0
                player.y = -300

    

    #update screen
    wn.update()

    #clear the pen
    pen.clear()

