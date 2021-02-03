#breakout

import pygame
import sys
import math
import random
from pygame.constants import K_x, WINDOWHITTEST

from pygame.cursors import sizer_y_strings
from pygame.math import enable_swizzling

pygame.init()
pygame.display.set_caption("Backgammon v0.1")
clock = pygame.time.Clock()

#pixel 4 1792 x 828
WIDTH = 1792
HEIGHT = 828

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255,0,0)
BLUE = (0,0,255)



# todo
# handle render when there are more than 6 pips in a position
# add player endgame status checking
# decide where error checking is.  On the UI, like can't select a blank position?  On the move()?
# do I even need the board object if I only ever have one instance?  Could move all those functions out to root?


#create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))

#create classes
#Sprite, Pip, Dice, Doubling Cube, Buttons


class Pip(pygame.sprite.Sprite):
    def __init__(self, player):
        pygame.sprite.Sprite.__init__(self)
        self.x = 0  
        self.y = 0
        self.diameter = 50
        self.player = player
        self.color = player.color 
        self.rect = pygame.rect.Rect(0,0,self.diameter,self.diameter)
        self.position = 0
    
    # def render(self,x, y):   from when the pip assignment was determined every render
    #     self.x = x
    #     self.y = y
    #     print("pipx:  ",self.x,"  pipy:  ",self.y)
    #     pygame.draw.circle(screen,self.color,(self.x, self.y),self.diameter/2.0, width=0)
    #     pass

    def render(self):
        pygame.draw.circle(screen,self.color,(self.x, self.y),self.diameter/2.0, width=0)
        #print("render pipx:  ",self.x,"  pipy:  ",self.y)
        self.rect.center = (self.x,self.y)



class Board():
    def __init__(self, startx, starty):
        self.positions = [[] for i in range(25)]
        self.startx = startx
        self.starty = starty
        self.positionwidth = 70
        self.positiongap = 5
        self.centerwidth = 70
        #for x in range(24):
        #    self.positions.append([])

    def assignpipsxy(self):
        #for each position, assign the pips the proper xy to be rendered.
        #this means we can re-calc positions as necessary, not on every main loop

        for position in range(1,25):
            for spot in range(len(self.positions[position])):
                self.positions[position][spot].position = position

        #top row
        x = self.startx
        for position in range(1,13):
            y = self.starty
            for spot in range(len(self.positions[position])):
                self.positions[position][spot].x = x
                self.positions[position][spot].y = y
                #self.positions[position][spot].render()
                #print("within board render; x:  ",x,"   y:  ",y)
                y += self.positions[position][spot].diameter + self.positiongap
            if position == 6:  #if we're at the center, skip the center
                x -= (self.centerwidth + self.positionwidth)
            else:
                x -= self.positionwidth
        
        #bottom row
        x = self.startx - ((self.positionwidth * 11) + self.centerwidth)
        for position in range(13,25):
            y = self.starty + 680  #come back here to set a scalable board height
            for spot in range(len(self.positions[position])):
                self.positions[position][spot].x = x
                self.positions[position][spot].y = y
                #self.positions[position][spot].render()
                y -= self.positions[position][spot].diameter + self.positiongap
            if position == 18:
                x += (self.centerwidth + self.positionwidth)
            else:
                x += self.positionwidth

            

    
    def checkdestination(self,player,destinationindex):
        if player.name=="top" and destinationindex > 24:
            return 0
        if player.name=="bottom" and destinationindex < 1:
            return 0

        if not self.positions[destinationindex]:
            return 1
        if self.positions[destinationindex][0].player.name == player.name:
            return 1
        return 0



    def ismovevalid(self,position,player,value):
        #print("\n\nposition:                                         ", position)
        #print("self.positions[position]:                         ", self.positions[position])
        #print("value:                                            ", value)
        #print("self.positions[position+value]:                   ", self.positions[position+value])
        #print("self.positions[position+value][0].player.name:    ", self.positions[position+value][0].player.name)
        #print("player.name:                                      ", player.name)
        
        if not self.positions[position]:  # shouldn't need this -- only allow moves that start on sprites
            return "position has no pips to move" #position is empty -- nothing to move
        
        if not player.name == self.positions[position][0].player.name:
            return "position has other player's pips" #position has pips from the other player

        # find the destination, return 0 if it's off the board       <---  move this to move(), change this function to accept source, destination
        if player.name == "top":
            destination = position + value
            if destination > 24:
                return "top tried to move off the board"
        elif player.name == "bottom":
            destination = position - value
            if destination < 1:
                return "bottom tried to move off the board"
        else:
            return "unknown player name"

        if self.positions[destination]:
            print("test part a - destination position IS NOT empty")
            if self.positions[destination][0].player.name == player.name:
                return "OK - destination has my own pips"
            else:
                return "destination has other player's pips"
        else:
            print("test part a - destination position IS empty")
            return "OK - destination is empty"
    
    def getposition(self):
        pass #return empty, or count of pips and which player

    def move(self,source,destination):
        destination.append(source.pop())
        return 1


        
       

    def setup(self):  #deprecated after moving this to the create section.
        # a tuple of tuples with the locations and players of a standard backgammon game
        preset = ((1,2,playerA),(6,5,playerB),(8,3,playerB),(12,5,playerA),
                (13,5,playerB),(17,3,playerA),(19,5,playerA),(24,2,playerB))
        
        # place a pip of each kind in the self.positions
        for position in preset:
            print("preset position:  ",position[0])
            for spot in range(position[1]):
                self.positions[position[0]].append(Pip(position[2]))


# problem:  setup creates new pips each time.  So, we'l have to destroy the board between rounds
# to avoid using up RAM.  Or, make a new method called reset() that moves pips instead of creating?
# also: move setup() out of the class.




class Player():
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.score = 0
        self.bearingoff = 0
        self.pipstogo = 0
        self.jail = []
        self.home = []

    def update(self):
        self.injail = 0
        self.bearingoff = 0
        self.pipstogo = 0





#create fonts
font = pygame.font.SysFont("arial", 24)



#create objects


board = Board(1300,100)
playerA = Player("top", WHITE)
playerB = Player("bottom", GREEN)
players = [playerA, playerB]

pips = pygame.sprite.Group()
allsprites = pygame.sprite.Group()


preset = ((1,2,playerA),(6,5,playerB),(8,3,playerB),(12,5,playerA),
            (13,5,playerB),(17,3,playerA),(19,5,playerA),(24,2,playerB))

# create each pip and place it where it belongs in board.positions
for position in preset:
    print("preset position:  ",position[0])
    for spot in range(position[1]):
        newpip = Pip(position[2])
        pips.add(newpip)
        allsprites.add(newpip)
        board.positions[position[0]].append(newpip)
        
activeplayer = players[0]
#need to start implementing turns.  Whose turn is it?

dice=[0,0]

def roll():
    dice = [0,0]
    for i in range(0,2):
        dice[i]=random.randint(1,6)
        #print("inroll dice:  ", dice[0],dice[1])
    if dice[0]==dice[1]:
        dice.append(dice[0])
        dice.append(dice[0])
    return dice
dice = roll()
dice.sort()

print("preloop dice:  ",dice)

activedie=dice.pop()
clickedsprites=[]

#game loop

while True:
    clickedsprites = []
    clickedpip = []
    
        #calc destination
    if activeplayer.name=="top":
        if activeplayer.jail:
            destination = board.positions[activedie]
        else:
            destination = board.positions[5]
    

    
    
    
    events = pygame.event.get()   
    for event in events:
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            clickedsprites = [s for s in allsprites if s.rect.collidepoint(pos)]
    #print("events:  ",events)
    #print("allsprites:  ", allsprites)
    #print("pips:  ",pips)
    #print("clickedsprites:  ", clickedsprites)
    #mouse bindings
    if len(clickedsprites)>1: 
        print("clicked on two sprites at the same time")
    elif len(clickedsprites)==1:
        clickedpip=clickedsprites[0]
        print("pip player:  ",clickedpip.player.name," position:  ",clickedpip.position)

    print("activedie:  ",activedie)


    moved = 0
    if clickedpip:  #has a pip been clicked
        if clickedpip.player == activeplayer:  #if the clicked pip belongs to activeplayer
            if activeplayer.name=="top":  #top player
                if activeplayer.jail:  #player is in jail, can only move jailed pips
                    destination = activedie  
                    if board.checkdestination(activeplayer,destination):
                        moved = board.move(activeplayer.jail,board.positions[destination])
                elif activeplayer.bearingoff:  #player is bearing off, special rules
                    destination = activedie
                    if destination > 24:
                        moved = board.move(board.positions[clickedpip.position],player.home)
                    else:
                        if board.checkdestination(activeplayer,destination):
                            board.move(board.positions[clickedpip.position],board.positions[destination])
                else:   #regular move
                    destination = clickedpip.position+activedie
                    print(destination)
                    if board.checkdestination(activeplayer,destination):
                        moved = board.move(board.positions[clickedpip.position],board.positions[destination])

            if activeplayer.name=="bottom":
                if activeplayer.jail:
                    destination = 24-activedie
                    if board.checkdestination(activeplayer,destination):
                        moved = board.move(activeplayer.jail,board.positions[destination])
                elif activeplayer.bearingoff:
                    destination = activedie
                    if destination < 1:
                        moved = board.move(board.positions[clickedpip.position],player.home)
                    else:
                        if board.checkdestination(activeplayer,destination):
                            board.move(board.positions[clickedpip.position],board.positions[destination])
                else:
                    destination = clickedpip.position-activedie
                    print(destination)
                    if board.checkdestination(activeplayer,destination):
                        moved = board.move(board.positions[clickedpip.position],board.positions[destination])    

    if moved:
        activedie=dice.pop()    




    

    # roll
    # are there any valid moves?  if not end the turn
    # get click 
    # if clicked button, do a button
    # elif clicked pip matches activeplayer:
    #        if player in jail AND clickedpip = jail
    #             if destination valid 
    #               move(jail,destination)
    #        if player bearingoff 
    #             if destination valid 
    #               bear off(source)
    #        if destination valid
    #           move(source,destination)

    #click simulation
    


#######################################################
    # got mouse clicking working
    # new pseudocode:  assume we know whose turn it is, and they just rolled.  
    # don't get caught thinking we're going pass an index to move.  Just handle the three cases:
    # we're in jail, we're normal, or we're bearingoff
    # might have to build that "are there any valid moves" checking now
    # also: move dice to a class, to keep data and functions tidy.  
    # keep history by turn, roll, sort, activedie, etc.  
    # one option:  for player B, activedie*-1 to calc destination.   Then you can remove
    # the checking "top" player for how to handle direction
    
    # Now:  do dice and turn handling
    #     
#######################################################

    
    #todo:  figure out what we're going to pass to move -- index numbers, or lists
    #toto:  ideally:    if valid source AND valid destination: move
    #                   validsource() needs to know the source, the player status  
    #                   validdestination needs to know player status, destination
    #                   make sure to pop the current die on a valid move
    #                   Resolved:  move() must take the source and destination as lists, not indicies
    #                   Maybe make calcdestination()  ?   challenge is different destinations for regular/jail
    #       add something to the loop that checks to see if anything is in motion, and then just skips 
    #       all the logic and loops again until the motion is complete


    # print("ismovevalid checking\n") 
    # t1 = board.ismovevalid(6,playerA,1)
    # t2 = board.ismovevalid(6,playerB,2)
    # t3 = board.ismovevalid(6,playerB,5)
    # t4 = board.ismovevalid(6,playerB,6)

    
    # print("recap:")
    # print("t1:  ", t1)
    # print("t2:  ", t2)
    # print("t3:  ", t3)
    # print("t4:  ", t4)

    #print(board.move(playerA,board.positions[6],board.positions[4]))
    #print(board.move(playerB,6,1))   #wrong way, using indicies instead of lists


    #render stuff

    screen.fill(BLACK)
    

    
    #if anything is in motion update() the motion, else board.assignpipsxy()
    #read the position index of each pip and assign it an x,y 
    board.assignpipsxy()
    

    #render pips because they're not images and can't use the pygame draw() method
    for pip in pips:
        pip.render()
        #when we upgrade to images this can be removed; all sprites will render the same.

    


#    for brick in bricks:   #if the pips know their location, maybe just render them?
#        brick.render()     #that's dumb, right?  collision checking everywhere

    score_surface = font.render(f"Score: {playerA.score}", True, WHITE)
    screen.blit(score_surface, (WIDTH/2.0, 25))




    for player in players:
        player.update








    #flip the display
    pygame.display.flip()

    #set the FPS
    clock.tick(30)
