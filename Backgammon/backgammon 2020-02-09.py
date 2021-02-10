#backgammon version before rewriting move logic to handle out-of-order dice

import pygame
import sys
import math
import random
from pygame.constants import GL_CONTEXT_DEBUG_FLAG, K_x, WINDOWHITTEST

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



#create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))

#create fonts
buttonfont = pygame.font.SysFont("arial", 30)
debugfont = pygame.font.SysFont("couriernew",16)


#create classes
#Sprite, Pip, Dice, Doubling Cube, Buttons


class Dice():
    def __init__(self):
        print("initing dice")
        self.dicelog=[]
        self.turn=0
        self.inturn=0
        #self.activedice=[]
    
    #note this uses roll() but ignores doubles--good!
    def whogoesfirst(self,playerA,playerB):
        print("starting dice.whogoesfirst()")
        adice = []
        bdice = []
        while adice == bdice: #roll until it's not a tie
            adice = self.roll()
            bdice = self.roll()
            print("adice:  ",adice)
            print("bdice:  ",bdice)
        if adice[0]+adice[1] > bdice[0]+bdice[1]:
            self.dicelog=[]  #because roll() also appends to dicelog
            self.dicelog.append(bdice)
            self.dicelog.append(adice)
            return playerA
        else:
            self.dicelog=[] #because roll() also appends to dicelog
            self.dicelog.append(adice)
            self.dicelog.append(bdice)
            return playerB

   
    def roll(self):
        tdice = [0,0]
        for i in range(0,2):
            tdice[i]=random.randint(1,6)
            #print("in dice.roll():  ", dice[0],dice[1])
        if tdice[0]==tdice[1]:  #if doubles, make two more 
            tdice.append(tdice[0])
            tdice.append(tdice[0])
        return tdice
    
    # def getactivedice(self):
    #     tdice=[]
    #     for i in range(0,len(self.dicelog[self.turn])):
    #         tdice[i]=int(self.dicelog[self.turn][i])
    #     return tdice

class Button(pygame.sprite.Sprite):
    def __init__(self,text,pos,font,color):
        self.text = text
        self.font = font
        self.color = color
        self.surface = self.font.render(self.text, 1, self.color)
        self.rect = self.surface.get_rect(topleft=pos)
        pygame.sprite.Sprite.__init__(self)

    def draw(self):
        # print("button.draw()")
        # print("self.image:        ",self.surface)
        # print("self.rect:         ",self.rect)
        # print("self.color:         ",self.color)
        # print("self.font:         ",self.font)
        # print("self.rect:         ",self.rect)
        screen.blit(self.surface,self.rect)


class DisplayDice(pygame.sprite.Sprite):
    def __init__(self):
        self.size=50
        self.rect = pygame.rect.Rect(0,0,self.size,self.size)       


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
                y -= self.positions[position][spot].diameter + self.positiongap
            if position == 18:
                x += (self.centerwidth + self.positionwidth)
            else:
                x += self.positionwidth

    
    def checkdestination(self,player,destinationindex):
        #return 0 for no good, 1 for ok, and 2 for bump
        if player.name=="top" and destinationindex > 24:
            return 0
        if player.name=="bottom" and destinationindex < 1:
            return 0
        if not self.positions[destinationindex]:
            return 1
        if self.positions[destinationindex][0].player.name == player.name:
            return 1
        else:
            if len(self.positions[destinationindex])==1:
                return 2
            else:
                return "error--shouldn't get here"
        

    def move(self,source,destination):
        print("move(source,destination):  ",source,",",destination)
        destination.append(source.pop())
        return 1

    def movebump(self,source,destination,jail):
        print("movebump(source,destination,jail):  ",source,",",destination,",",jail)
        jail.append(destination.pop())
        destination.append(source.pop())
        return 1


    def setup(self):  #deprecated after moving this to the create section.
        #destroy old pips
        for player in players:
            player.jail=[]
        for position in self.positions:
            self.positions[position]=[]
        

        # a tuple of tuples with the locations and players of a standard backgammon game
        preset = ((1,2,playerA),(6,5,playerB),(8,3,playerB),(12,5,playerA),
                (13,5,playerB),(17,3,playerA),(19,5,playerA),(24,2,playerB))
        
        # place a pip of each kind in the self.positions
        for position in preset:
            print("preset position:  ",position[0])
            for spot in range(position[1]):
                self.positions[position[0]].append(Pip(position[2]))


# problem:  setup() creates new pips each time.  
# So first .pop() all the pips, then create new pips


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
        self.bearingoff = 0
        self.pipstogo = 0





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
    #print("preset position:  ",position[0])
    for spot in range(position[1]):
        newpip = Pip(position[2])
        pips.add(newpip)
        allsprites.add(newpip)
        board.positions[position[0]].append(newpip)

dice=Dice()
activedice=[]
activeplayer=playerA

#game loop

#allsprites.add(Button("roll",buttonfont,WHITE,400,400))
RollButton = Button("Roll",(700,HEIGHT/2),buttonfont,WHITE)
# RollButton.draw(screen)
allsprites.add(RollButton)

# sys.exit()

def printdebug():
        try:
            print("activeplayer:   ",activeplayer.name,"  inTurn:   ",dice.inturn,"   Turn:   ",dice.turn,"    activedice:   ",activedice)
            print("checkdestination:  ", board.checkdestination(activeplayer,destination))
        except Exception:
            print("some bullshit exception from printdebug()")


while True:
    # print("*****LOOP START*****")

    clickedsprites = []
    clickedpip = []
    clickedbutton = []

    events = pygame.event.get()   
    for event in events:
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            clickedsprites = [s for s in allsprites if s.rect.collidepoint(pos)]


    #mouse bindings
    if len(clickedsprites)>1: 
        print("WARNING: clicked on two sprites at the same time")
    elif len(clickedsprites)==1:
        clickedsprite=clickedsprites[0]
        print("clickedsprite:       ",clickedsprite)
        if isinstance(clickedsprite,Pip):
            clickedpip = clickedsprite
        if isinstance(clickedsprite,Button):
            clickedbutton = clickedsprite




    if dice.turn==0:
        print("\n***if dice.turn==0")
        activeplayer = dice.whogoesfirst(playerA,playerB)
        dice.turn+=1
        print("^^^incrementing dice.turn from the rolloff")
        dice.inturn=1
        activedice=dice.dicelog[dice.turn][:]



    #UI Render:
    #display menu
    if dice.inturn:
        #display activedice
        pass
    else:
        #display roll button
        pass


    if not dice.inturn and clickedbutton == RollButton:
        print("\n*****ROLLING DICE*****")
        dice.dicelog.append(dice.roll())
        dice.turn += 1  
        activedice=dice.dicelog[dice.turn][:]   #this funky syntax makes a copy, instead of a reference
        dice.inturn=1
        if activeplayer == players[0]:
            activeplayer = players[1]
        else:
            activeplayer = players[0]

        
#if activeplayer=bottom: effective dice = -activedice






    moved = 0
    if dice.inturn and clickedpip:  #has a pip been clicked
        print("\n*****MAIN MOVE LOGIC*****")
        activedie=activedice[-1]
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
                    # print(destination)
                    if board.checkdestination(activeplayer,destination)==1:
                        moved = board.move(board.positions[clickedpip.position],board.positions[destination])
                    if board.checkdestination(activeplayer,destination)==2:
                        moved = board.movebump(board.positions[clickedpip.position],board.positions[destination],activeplayer.jail)


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
                    # print(destination)
                    if board.checkdestination(activeplayer,destination)==1:
                        moved = board.move(board.positions[clickedpip.position],board.positions[destination])    
                    if board.checkdestination(activeplayer,destination)==2:
                        moved = board.movebump(board.positions[clickedpip.position],board.positions[destination],activeplayer.jail)



    if moved:
        # print("\n***if moved")
        if activedice:
            activedice.pop()
        if not activedice:
            dice.inturn = 0
            #also change players

        


#######################################################
    # keep history by turn, roll, sort, activedie, etc.  

    # handle bumping        
    # render jail and home
    #****** handle bumping -- checkdestination got a "should never get here" -- but maybe outside of a regular check?  like, when it shouldn't have been checking anyway?
    # important:  figure out if highest die first even works.  If it's blocked, do lower die?
    #             how did that weird old Palm game work?

    # movebump is being passed the wrong jail
    # maybe set "otherplayer" as well as "activeplayer"
 

#######################################################


    #calc isbearingoff (could move this to inside "if moved:" to save some CPU
    for player in players:
        player.bearingoff = 1
    for i in range(1,25):
        if board.positions[i]:
            if i < 18 and board.positions[i][0].player==playerA:
                playerA.bearingoff = 0
            if i > 6 and board.positions[i][0].player==playerB:
                playerB.bearingoff = 0









    #render stuff

    screen.fill(BLACK)

    dtext=[]
    dtext.append("dice.inturn:    "+str(dice.inturn))
    dtext.append("dice.turn:      "+str(dice.turn))
    dtext.append("activeplayer:   "+str(activeplayer.name))
    dtext.append("activedice:     "+str(activedice))
    dtext.append("dicelog:        "+str(dice.dicelog))
    dxpos=1000
    dypos=400
    for line in range(len(dtext)):
        dsurface = debugfont.render(dtext[line],1,WHITE)
        screen.blit(dsurface,(dxpos,dypos+(line*15)))




    if not dice.inturn:
        RollButton.draw()
    
    #if anything is in motion update() the motion, else board.assignpipsxy()
    #read the position index of each pip and assign it an x,y 
    board.assignpipsxy()
    

    #render pips because they're not images and can't use the pygame draw() method
    for pip in pips:
        pip.render()
        #when we upgrade to images this can be removed; all sprites will render the same.

    


#    for brick in bricks:   #if the pips know their location, maybe just render them?
#        brick.render()     #that's dumb, right?  collision checking everywhere

    # score_surface = font.render(f"Score: {playerA.score}", True, WHITE)
    # screen.blit(score_surface, (WIDTH/2.0, 25))




    for player in players:  #might not need this if it's handled elsewhere
        player.update()








    #flip the display
    pygame.display.flip()

    #set the FPS
    clock.tick(30)



"""
TKTKTKTKTKTKTKTKTK

Move Log
    turn number, move number, source, destination


Roll Dice
    Player in Jail?
        Any valid moves from jail?
            Player clicks
                valid move with dice, highest to lowest, do the move
        No valid moves, pass the turn.
    Player Bearing Off?
        Any valid moves including to home?
            Player clicks
                valid move with dice, highest to lowest, do the move
        No valid moves, pass the turn
    Player moving normally
        Player clicks
            valid move with dice, highest to lowest, do the move






combine movebump and move(), because we'll test valid moves in move logic?
like, if there's a piece in destination from the opposite player, bump to jail
So, always pass activeplayer, otherplayer to move()



# todo
# handle render when there are more than 6 pips in a position
# do I even need the board object if I only ever have one instance?  Could move all those functions out to root?
# if we're forcing players to move largest die first, need to check if there even are any valid moves after each roll






"""