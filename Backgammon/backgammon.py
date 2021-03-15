#backgammon

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


    def assignpipsxy(self):
        #error checking -- move all pips to 50,50 first and then put them where they go.  Any pips left here = trouble
        for pip in pips:  
            pip.x=50
            pip.y=50
        
        
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
                x -= (self.centerwidth + self.positionwidth + self.positiongap)
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

        #homes
        x=1500
        y=650
        for homepip in playerA.home:
            homepip.position="home"
            homepip.x = x
            homepip.y = y
            y += homepip.diameter/5 
        
        y=250
        for homepip in playerB.home:
            homepip.position="home"
            homepip.x = x
            homepip.y = y
            y += homepip.diameter/5 

        #jails
        x = 880
        y = 150
        for jailedpip in playerA.jail:
            jailedpip.position="jail"
            jailedpip.x = x
            jailedpip.y = y
            y += jailedpip.diameter + self.positiongap

        y = 550
        for jailedpip in playerB.jail:
            jailedpip.position="jail"
            jailedpip.x = x
            jailedpip.y = y
            y += jailedpip.diameter + self.positiongap





    
    def checkdestination(self,player,destinationindex):
        #return 0 for no good, 1 for ok
        if player.name=="top" and destinationindex > 24:
            print("checkdestination: top player moving off board")
            return 0
        if player.name=="bottom" and destinationindex < 1:
            print("checkdestination: bottom player moving off board")
            return 0
        if not self.positions[destinationindex]:
            print("checkdestination: destination empty")
            return 1
        if self.positions[destinationindex][0].player.name == player.name:
            print("checkdestination: destination contains friendly pips")
            return 1
        else: #must contain enemy pips, so
            if len(self.positions[destinationindex])==1:
                print("checkdestination: destination contains one lonely enemy pip")
                return 1
            else:
                print("checkdestination: destination contains more than one enemy pip")
                return 0
        

    def move(self,player,otherplayer,source,destination):
        print("move(player,otherplayer,source,destination):  ",player.name,",",otherplayer.name,",",source,",",destination)
        if not destination:
            destination.append(source.pop())
        elif destination[0].player==player:
            destination.append(source.pop())
        else:
            otherplayer.jail.append(destination.pop())
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
playerA = Player("top", GREEN)
playerB = Player("bottom", WHITE)
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
effectivedice=[]
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
        print("from mousebindings:clickedsprite:       ",clickedsprite)
        if isinstance(clickedsprite,Pip):
            clickedpip = clickedsprite
            print("from mousebindings:clickedpip:  ",clickedpip)
        if isinstance(clickedsprite,Button):
            clickedbutton = clickedsprite

    
    if dice.turn==0:
        effectivedice=[[],[],[],[]]
        print("\n***if dice.turn==0")
        activeplayer = dice.whogoesfirst(playerA,playerB)
        if activeplayer==playerA:
            otherplayer=playerB
        else:
            otherplayer=playerA
        dice.turn+=1
        print("^^^incrementing dice.turn from the rolloff")
        dice.inturn=1
        activedice=dice.dicelog[dice.turn][:]
        #add used flags to activedice
        for i in range(len(activedice)):
            activedice[i]=[activedice[i],0]
        
        #now get effective dice
        for i in range(len(activedice)):
            effectivedice[i]=[activedice[i][0],i] #come back here to add flags to effective dice if we need it, but try hard not to need it
        
        #sort the effective dice so it's high to low
        effectivedice.sort(reverse=True)
        
        if not effectivedice[3]:   #if dice 3 is empty, it's not doubles, pop last two empty dice
            effectivedice.pop()
            effectivedice.pop()

        #if activeplayer is bottom, neg the dice values
        if activeplayer==playerB:
            for i in range(len(effectivedice)):
                effectivedice[i][0] *= -1
                
#len(effectivedice)>1 and 
        #for i in range(len(effectivedice)):


#for each roll, including the first one:
#roll the dice, put in dicelog[turn]
#set activedice to be dicelog, and add used flags
#set effective dice to be sorted, with used flags, with index in activedice, and negatived for bottom
#do displaydice based on activedice 
#do moves based on effectivedice, write the usedflag in both effective and active

#maybe get rid of dice.turn, and use len(dicelog)-1?  Always the same, right?



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
        #turn handling
        dice.turn += 1  
        dice.inturn=1
        #make the correct player active
        if activeplayer == players[0]:
            activeplayer = players[1]
            otherplayer = players[0]
        else:
            activeplayer = players[0]
            otherplayer = players[1]

        #actually roll the fucking dice, add it to dicelog
        dice.dicelog.append(dice.roll())
        activedice=dice.dicelog[dice.turn][:]

        #add used flags to activedice
        for i in range(len(activedice)):
            activedice[i]=[activedice[i],0]
        
        #now get effective dice
        effectivedice=[[],[],[],[]] #always start with four blank dice
        for i in range(len(activedice)):
            effectivedice[i]=[activedice[i][0],i] #come back here to add flags to effective dice if we need it, but try hard not to need it
        
        #sort the effective dice so it's high to low
        effectivedice.sort(reverse=True)
        
        if not effectivedice[3]:   #if dice 3 is empty, it's not doubles, pop last two empty dice
            effectivedice.pop()
            effectivedice.pop()

        #if activeplayer is bottom, neg the dice values
        if activeplayer==playerB:
            for i in range(len(effectivedice)):
                effectivedice[i][0] *= -1

        




    moved = 0
    if dice.inturn and clickedpip and clickedpip.player==activeplayer:  #****** TODO has a pip been clicked (why can't I .player==activeplayer)
        print("\n*****MAIN MOVE LOGIC*****")

        print("clickedpip.player.name:    ",clickedpip.player.name)
        print("clickedpip.position:  ",clickedpip.position)
        print("effectivedice:        ",effectivedice)
        print("len(effectivedice):   ",len(effectivedice))

        if activeplayer.jail and clickedpip:
            validmoves=0

        if activeplayer.bearingoff:
            pass
        
        # regular move
        # are there any valid moves?
        validmoves=0
        for i in range(len(effectivedice)):  #for when largest die is not valid move for that pip
            print("i:         ",i)
            print("len(effectivedice):   ",len(effectivedice))
            print("checking:  ",board.checkdestination(activeplayer,effectivedice[i][0]+clickedpip.position))
            if board.checkdestination(activeplayer,effectivedice[i][0]+clickedpip.position):
                moved = board.move(activeplayer,otherplayer,board.positions[clickedpip.position],board.positions[clickedpip.position+effectivedice[i][0]])
                activedice[effectivedice[i][1]][1]=1
                effectivedice.pop(i)
                break






    if not effectivedice:   #no more effectice dice, turn is over
        dice.inturn = 0


        


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
    dtext.append("activeplayer:   "+str(activeplayer.name)+" "+str(activeplayer.color))
    dtext.append("otherplayer:    "+str(otherplayer.name))
    dtext.append("dicelog:        "+str(dice.dicelog))
    dtext.append("activedice:     "+str(activedice))
    dtext.append("effectivedice:  "+str(effectivedice))
    dxpos=1000
    dypos=380
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

Fixed bugs in checking who can move, and bumping seems to work properly
Running into trouble that sometimes I check for "playerA" and sometimes for =="top"

Next try more testing to make sure all regular moves handled ok




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
        Are there any valid moves at all?
            Player clicks
                valid move with dice, highest to lowest, do the move


********TODO:  jump to line 382, figure out how to handle 
are there any moves at all?  (pass turn if not)
is the clicked move valid on the highest die?  next highest?  do the move



combine movebump and move(), because we'll test valid moves in move logic?
like, if there's a piece in destination from the opposite player, bump to jail
So, always pass activeplayer, otherplayer to move()



# todo
# handle render when there are more than 6 pips in a position
# do I even need the board object if I only ever have one instance?  Could move all those functions out to root?
# if we're forcing players to move largest die first, need to check if there even are any valid moves after each roll






"""