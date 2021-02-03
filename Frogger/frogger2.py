#frogger
#by Rob

import turtle
import math
import time
import random

#setup the window, specifc for Turtle module
wn = turtle.Screen()
wn.title("Frogger by Rob")
wn.setup(600,800)
wn.bgcolor("black")
wn.tracer(0)
wn.cv._rootwindow.resizable(False,False)   #prevent window resizing

#Register Shape
shapes = ["frog.gif", "car_left.gif", "car_right.gif", "log_full.gif", "turtle_left.gif",
    "turtle_right.gif", "turtle_left_half.gif","turtle_right_half.gif", "turtle_submerged.gif",
    "goal.gif", "frog_home.gif", "frog_small.gif"]
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
        self.lives=4
        self.frogsathome=0
        self.time_remaining=60
        self.max_time = 60
        self.start_time = time.time()

    def up(self):
        self.y += 50

    def down(self):
        self.y -= 50

    def left(self):
        self.x -= 50

    def right(self):
        self.x += 50
    
    def go_home(self):
        self.dx = 0
        self.x = 0
        self.y = -300

    def dies(self):
        self.go_home()
        self.time_remaining = 60
        self.start_time = time.time()
        self.lives -= 1
    
    def update(self):
        self.x += player.dx

        #border checking
        if self.x < -320 or self.x > 320:
            self.dies()
        if self.y < -325:
            self.go_home()
            

        self.time_remaining = self.max_time - round(time.time() - self.start_time)
        #print(self.y)

        if self.time_remaining <= 0:
            self.dies()

    
    

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
        self.submerged_time = random.randint(1,3)
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

            

        #timer stuff for the turtles to go up and down
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

class Timer():
    def __init__(self, max_time):
        self.x = 200
        self.y = -375
        self.max_time = max_time
        self.width = 200

    def render(self, time, pen):
        pen.color("green")
        pen.pensize(5)
        pen.penup()
        pen.goto(self.x, self.y)
        pen.pendown()
        percent = time/self.max_time
        dx = percent * self.width
        pen.goto(self.x-dx, self.y)
        pen.penup()

#Create Objects

# programatically create list of cars.  create a blank list, then loop by appending car objects.  This
# creates 5 cars.  'x' loop index determines the y height on screen.  
cars = []
for x in range (0,5):
    rowspeed = random.randint(15,30)/100       # each row has its own random speed
    rowstart = random.randint(-250,150)     # start each row at a random x position
    rowgap = random.randint(200,300)
    if x % 2 == 1:  #for even numbered rows, create left-facing cars with -negative rowspeed
        cars.append(Car(rowstart,(x*-50)-50, 121,40, "car_left.gif", -rowspeed))
        cars.append(Car(rowstart+rowgap,(x*-50)-50, 121,40, "car_left.gif", -rowspeed))
    else:   #odd numbered rows, right-facing cars
        cars.append(Car(rowstart,(x*-50)-50, 121,40, "car_right.gif", rowspeed))
        cars.append(Car(rowstart+rowgap,(x*-50)-50, 121,40, "car_right.gif", rowspeed))


player = Player(0, -300, 40, 40, "frog.gif")
timer = Timer(60)

river = []
for x in range (0,5):
    rowspeed = random.randint(40,60)/100       # each row has its own random speed
    rowstart = random.randint(-250,150)     # start each row at a random x position
    rowgap = random.randint(200,300)
    if x % 2 == 1:
        river.append(Turtle(rowstart,x*50+50,155,40,"turtle_left.gif",-rowspeed))
        river.append(Turtle(rowstart+rowgap,x*50+50,155,40,"turtle_left.gif",-rowspeed))
    else:
        river.append(Log(rowstart,x*50+50,121, 40, "log_full.gif",rowspeed))
        river.append(Log(rowstart+rowgap,x*50+50,121, 40, "log_full.gif",rowspeed))


goals=[]
for x in range(0,5):
    goals.append(Home(((x-4)*100)+200,300,50,50, "goal.gif"))



#list sprites
sprites = cars + river + goals
sprites.append(player)
#player should be last so renders on top


#keyboard binding
wn.listen()
wn.onkeypress(player.up, "Up")
wn.onkeypress(player.down, "Down")
wn.onkeypress(player.left, "Left")
wn.onkeypress(player.right, "Right")


while player.lives>0:
    #render sprites
    for sprite in sprites:
        sprite.render(pen)
        sprite.update()

    #render countdown timer
    timer.render(player.time_remaining, pen)
    
    #render lives
    pen.goto(-280,-375)
    pen.shape("frog_small.gif")
    for life in range(player.lives):
        pen.goto(-290 + (life * 30), -375)
        pen.stamp()


    player.dx=0 #reset player moving if was on log or unsubmerged turtle
    #frog lives, dies, moves based on contact with another sprite
    for sprite in sprites:
        if player.is_collision(sprite):
            if isinstance(sprite, Car):
                player.dies()
                break
            elif isinstance(sprite,Log):
                player.dx = sprite.dx
                break
            elif isinstance(sprite,Turtle) and sprite.state != "submerged":
                player.dx = sprite.dx
                break
            elif isinstance(sprite, Home):
                player.go_home()
                sprite.image = "frog_home.gif"
                player.frogsathome += 1
                break
    
            elif player.y > 0:
                player.dies()

    if player.frogsathome == 5:   #if we won
        player.go_home
        player.frogsathome = 0
        for goal in goals:   #reset goal objects to empty house gifs
            goal.image="goal.gif"


    #update screen
    wn.update()

    #clear the pen
    pen.clear()

