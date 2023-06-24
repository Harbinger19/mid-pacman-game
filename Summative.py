import pygame
from pygame.locals import *
import random
import time

xlimit = 800
ylimit = 600

# pygame setup
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((xlimit, ylimit))
clock = pygame.time.Clock()
pygame.mixer.init()

#Initializing the scenes or parts of the game
menu = True
game = False
gameover = False

pacxcoord = 400
pacycoord = 250

direction = "up"

#These are used to change the look of pacman between open mouth and closed mouth
x = 0
y = 0

#Initializing a list of numbers to use in my score
numberlist = {
    "0" : "0.png",
    "1" : "1.png",
    "2" : "2.png",
    "3" : "3.png",
    "4" : "4.png",
    "5" : "5.png",
    "6" : "6.png",
    "7" : "7.png",
    "8" : "8.png",
    "9" : "9.png",
}

#controlling what image is used for the ghost based on description
ghostlook = {
    "left":"ghostleft.png",
    "right":"ghostright.png",
    "down":"ghostdown.png",
    "up":"ghostup.png"
}

#Initializing score
score = 0
tempscore = str(score)

#Used for collisions with Pac-Man
l = 0

#All of these are referring to the ghost. Coordinates, direction to move, past direction it moves
blinkypastdirection = ""
blinkydirection = "down"

blinkypreferred = []

blinkyxcoord = 400
blinkyycoord = 320

blinkytimer = 0

#Controlling collision of the ghost
d = 1
s = 0

#Initializing collision check variables, as well as checking that it escapes the initial hallway
initialcheck = 0
blinkycollision = 0

#Loading mp3 files for use in the game
backgroundnoise = pygame.mixer.Sound("pacmangame.mp3")
maingamenoise = pygame.mixer.Sound("eat.mp3")
deathnoise = pygame.mixer.Sound("dead.mp3")

#This is a list of values for each of the pellets that will load and be displayed on the screen
pelletlist = [(18, 18, 6, 6), (18, 58, 6, 6), (18, 98, 6, 6), (18, 138, 6, 6), (18, 178, 6, 6), (18, 218, 6, 6), (18, 258, 6, 6), (18, 298, 6, 6), 
            (18, 338, 6, 6), (18, 378, 6, 6), (18, 418, 6, 6), (18, 458, 6, 6), (18, 498, 6, 6), (18, 538, 6, 6), (18, 578, 6, 6), 
              
            (18, 18, 6, 6), (58, 18, 6, 6), (98, 18, 6, 6), (138, 18, 6, 6), (178, 18, 6, 6), (218, 18, 6, 6), (258, 18, 6, 6), 
            (298, 18, 6, 6), (338, 18, 6, 6), (378, 18, 6, 6), (418, 18, 6, 6), (458, 18, 6, 6), (498, 18, 6, 6), (538, 18, 6, 6), 
            (578, 18, 6, 6), (618, 18, 6, 6), (658, 18, 6, 6), (698, 18, 6, 6), (738, 18, 6, 6), (778, 18, 6, 6), 
              
            (58, 578, 6, 6), (98, 578, 6, 6), (138, 578, 6, 6), (178, 578, 6, 6), (218, 578, 6, 6), (258, 578, 6, 6), 
            (298, 578, 6, 6), (338, 578, 6, 6), (378, 578, 6, 6), (418, 578, 6, 6), (458, 578, 6, 6), (498, 578, 6, 6), (538, 578, 6, 6), 
            (578, 578, 6, 6), (618, 578, 6, 6), (658, 578, 6, 6), (698, 578, 6, 6), (738, 578, 6, 6), (778, 578, 6, 6), 
              
            (778, 778, 6, 6), (778, 58, 6, 6), (778, 98, 6, 6), (778, 138, 6, 6), (778, 178, 6, 6), (778, 218, 6, 6), (778, 258, 6, 6), (778, 298, 6, 6), 
            (778, 338, 6, 6), (778, 378, 6, 6), (778, 418, 6, 6), (778, 458, 6, 6), (778, 498, 6, 6), (778, 538, 6, 6), 
              
            (138, 58, 6, 6), (138, 98, 6, 6), (138, 138, 6, 6), (138, 178, 6, 6), (138, 218, 6, 6), (138, 258, 6, 6), (138, 298, 6, 6), 
            (138, 338, 6, 6), (138, 378, 6, 6), (138, 418, 6, 6), (138, 458, 6, 6), (138, 498, 6, 6), (138, 538, 6, 6),
              
            (658, 58, 6, 6), (658, 98, 6, 6), (658, 138, 6, 6), (658, 178, 6, 6), (658, 218, 6, 6), (658, 258, 6, 6), (658, 298, 6, 6), 
            (658, 338, 6, 6), (658, 378, 6, 6), (658, 418, 6, 6), (658, 458, 6, 6), (658, 498, 6, 6), (658, 538, 6, 6),

            (218, 518, 6, 6), (258, 518, 6, 6), (298, 518, 6, 6), (338, 518, 6, 6), (378, 518, 6, 6), (418, 518, 6, 6),
            (458, 518, 6, 6), (498, 518, 6, 6), (538, 518, 6, 6), (578, 518, 6, 6), 

            (218, 68, 6, 6), (258, 68, 6, 6), (298, 68, 6, 6), (338, 68, 6, 6), (378, 68, 6, 6), (418, 68, 6, 6), (458, 68, 6, 6), 
            (498, 68, 6, 6), (538, 68, 6, 6), (578, 68, 6, 6), 

            (198, 38, 6, 6), (198, 68, 6, 6), (198, 98, 6, 6), (198, 138, 6, 6), (198, 178, 6, 6), (198, 218, 6, 6), (198, 258, 6, 6), (198, 298, 6, 6), 
            (198, 338, 6, 6), (198, 378, 6, 6), (198, 418, 6, 6), (198, 458, 6, 6), (198, 488, 6, 6), (198, 518, 6, 6), (198, 548, 6, 6), 

            (598, 38, 6, 6), (598, 68, 6, 6), (598, 98, 6, 6), (598, 138, 6, 6), (598, 178, 6, 6), (598, 218, 6, 6), (598, 258, 6, 6), (598, 298, 6, 6), 
            (598, 338, 6, 6), (598, 378, 6, 6), (598, 418, 6, 6), (598, 458, 6, 6), (598, 488, 6, 6), (598, 518, 6, 6), (598, 548, 6, 6),

            (218, 168, 6, 6), (258, 168, 6, 6), (298, 168, 6, 6), (338, 168, 6, 6), (378, 168, 6, 6), (418, 168, 6, 6), (458, 168, 6, 6), 
            (498, 168, 6, 6), (538, 168, 6, 6), (578, 168, 6, 6), 

            (218, 418, 6, 6), (258, 418, 6, 6), (298, 418, 6, 6), (338, 418, 6, 6), (378, 418, 6, 6), (418, 418, 6, 6), (458, 418, 6, 6), 
            (498, 418, 6, 6), (538, 418, 6, 6), (578, 418, 6, 6), 

            (288, 188, 6, 6), (288, 218, 6, 6), (288, 258, 6, 6), (288, 298, 6, 6), (288, 338, 6, 6), (288, 378, 6, 6), (288, 398, 6, 6),

            (508, 188, 6, 6), (508, 218, 6, 6), (508, 258, 6, 6), (508, 298, 6, 6), (508, 338, 6, 6), (508, 378, 6, 6), (508, 398, 6, 6), 
            ]

#A list of rectangles that form the environment/level
screenrects = [(32, 32, 100, 50), (668, 32, 100, 50), (32, 518, 100, 50), (668, 518, 100, 50),
                (152, 32, 40, 200), (608, 32, 40, 200), (152, 368, 40, 200), (608, 368, 40, 200),
                (152, 252, 40, 96), (608, 252, 40, 96),
                (212, 32, 100, 30), (488, 32, 100, 30), (212, 528, 100, 40), (488, 528, 100, 40),
                (32, 102, 100, 70), (668, 102, 100, 70), (32, 428, 100, 70), (668, 428, 100, 70),
                (212, 82, 376, 20), (212, 488, 376, 20),
                (332, 32, 136, 30), (332, 528, 136, 40),
                (390, 82, 20, 80), (390, 428, 20, 70),
                (212, 122, 158, 40), (212, 428, 158, 40), (430, 122, 158, 40), (430, 428, 158, 40),
                (748, 192, 20, 216), (32, 192, 20, 216),
                (668, 290, 100, 20), (32, 290, 100, 20),
                (668, 192, 60, 78), (668, 330, 60, 78), (72, 192, 60, 78), (72, 330, 60, 78),
                (300, 182, 200, 58), (300, 360, 200, 48),
                (212, 182, 68, 226), (520, 182, 68, 226),
                (300, 260, 200, 10), (300, 260, 90, 10), (410, 260, 90, 10), (300, 330, 200, 10), (300, 260, 10, 80), (490, 260, 10, 80)]

#These are basically the same rectangles, except it adds the outer boundaries as extra rectangles and allows it to come out of the main central spawnpoint
ghostscreenrects = [(32, 32, 100, 50), (668, 32, 100, 50), (32, 518, 100, 50), (668, 518, 100, 50),
                (152, 32, 40, 200), (608, 32, 40, 200), (152, 368, 40, 200), (608, 368, 40, 200),
                (152, 252, 40, 96), (608, 252, 40, 96),
                (212, 32, 100, 30), (488, 32, 100, 30), (212, 528, 100, 40), (488, 528, 100, 40),
                (32, 102, 100, 70), (668, 102, 100, 70), (32, 428, 100, 70), (668, 428, 100, 70),
                (212, 82, 376, 20), (212, 488, 376, 20),
                (332, 32, 136, 30), (332, 528, 136, 40),
                (390, 82, 20, 80), (390, 428, 20, 70),
                (212, 122, 158, 40), (212, 428, 158, 40), (430, 122, 158, 40), (430, 428, 158, 40),
                (748, 192, 20, 216), (32, 192, 20, 216),
                (668, 290, 100, 20), (32, 290, 100, 20),
                (668, 192, 60, 78), (668, 330, 60, 78), (72, 192, 60, 78), (72, 330, 60, 78),
                (300, 182, 200, 58), (300, 360, 200, 48),
                (212, 182, 68, 226), (520, 182, 68, 226),
                (300, 260, 90, 10), (410, 260, 90, 10), (300, 330, 200, 10), (300, 260, 90, 80), (410, 260, 90, 80),
                (0, 0, 12, ylimit), (xlimit-12, 0, 12, ylimit), (0, 0, xlimit, 12), (0, ylimit-12, xlimit, 12)]

#Checking for collision if the player tries to change directions
k = 0

#Drawing the entire game screen defined as a function
def drawcourse():
    pygame.draw.rect(screen, "blue", (11, 11, 778, 578), 1, 10)

    pygame.draw.rect(screen, "blue", (32, 32, 100, 50), 1, 10)
    pygame.draw.rect(screen, "blue", (668, 32, 100, 50), 1, 10)
    pygame.draw.rect(screen, "blue", (32, 518, 100, 50), 1, 10)
    pygame.draw.rect(screen, "blue", (668, 518, 100, 50), 1, 10)

    pygame.draw.rect(screen, "blue", (152, 32, 40, 200), 1, 10)
    pygame.draw.rect(screen, "blue", (608, 32, 40, 200), 1, 10)
    pygame.draw.rect(screen, "blue", (152, 368, 40, 200), 1, 10)
    pygame.draw.rect(screen, "blue", (608, 368, 40, 200), 1, 10)

    pygame.draw.rect(screen, "blue", (152, 252, 40, 96), 1, 10)
    pygame.draw.rect(screen, "blue", (608, 252, 40, 96), 1, 10)

    pygame.draw.rect(screen, "blue", (212, 32, 100, 30), 1, 10)
    pygame.draw.rect(screen, "blue", (488, 32, 100, 30), 1, 10)
    pygame.draw.rect(screen, "blue", (212, 528, 100, 40), 1, 10)
    pygame.draw.rect(screen, "blue", (488, 528, 100, 40), 1, 10)

    pygame.draw.rect(screen, "blue", (32, 102, 100, 70), 1, 10)
    pygame.draw.rect(screen, "blue", (668, 102, 100, 70), 1, 10)
    pygame.draw.rect(screen, "blue", (32, 428, 100, 70), 1, 10)
    pygame.draw.rect(screen, "blue", (668, 428, 100, 70), 1, 10)

    pygame.draw.rect(screen, "blue", (212, 82, 376, 20), 1, 10)
    pygame.draw.rect(screen, "blue", (212, 488, 376, 20), 1, 10)

    pygame.draw.rect(screen, "blue", (332, 32, 136, 30), 1, 10)
    pygame.draw.rect(screen, "blue", (332, 528, 136, 40), 1, 10)

    pygame.draw.rect(screen, "blue", (390, 82, 20, 80), 1, 10)
    pygame.draw.rect(screen, "blue", (390, 428, 20, 70), 1, 10)

    pygame.draw.circle(screen, "black", (400, 94), 12)
    pygame.draw.line(screen, "blue", (390, 82), (410, 82))
    pygame.draw.circle(screen, "black", (400, 495), 12)
    
    pygame.draw.rect(screen, "blue", (212, 122, 158, 40), 1, 10)
    pygame.draw.rect(screen, "blue", (212, 428, 158, 40), 1, 10)
    pygame.draw.rect(screen, "blue", (430, 122, 158, 40), 1, 10)
    pygame.draw.rect(screen, "blue", (430, 428, 158, 40), 1, 10)

    pygame.draw.rect(screen, "blue", (748, 192, 20, 216), 1, 10)
    pygame.draw.rect(screen, "blue", (32, 192, 20, 216), 1, 10)

    pygame.draw.rect(screen, "blue", (668, 290, 100, 20), 1, 10)
    pygame.draw.rect(screen, "blue", (32, 290, 100, 20), 1, 10)

    pygame.draw.circle(screen, "black", (44, 300), 12)
    pygame.draw.line(screen, "blue", (32, 290), (32, 310))
    pygame.draw.circle(screen, "black", (756, 300), 12)
    pygame.draw.line(screen, "blue", (767, 290), (767, 310))

    pygame.draw.rect(screen, "blue", (668, 192, 60, 78), 1, 10)
    pygame.draw.rect(screen, "blue", (668, 330, 60, 78), 1, 10)
    pygame.draw.rect(screen, "blue", (72, 192, 60, 78), 1, 10)
    pygame.draw.rect(screen, "blue", (72, 330, 60, 78), 1, 10)

    pygame.draw.rect(screen, "blue", (300, 182, 200, 58), 1, 10)
    pygame.draw.rect(screen, "blue", (300, 360, 200, 48), 1, 10)

    pygame.draw.rect(screen, "blue", (212, 182, 68, 226), 1, 10)
    pygame.draw.rect(screen, "blue", (520, 182, 68, 226), 1, 10)

    pygame.draw.rect(screen, "black", (300, 260, 200, 10))
    pygame.draw.rect(screen, "blue", (300, 260, 90, 10), 1, 10)
    pygame.draw.rect(screen, "blue", (410, 260, 90, 10), 1, 10)
    pygame.draw.rect(screen, "blue", (300, 330, 200, 10), 1, 10)
    pygame.draw.rect(screen, "blue", (300, 260, 10, 80), 1, 10)
    pygame.draw.rect(screen, "blue", (490, 260, 10, 80), 1, 10)

    pygame.draw.circle(screen, "black", (306, 266), 5)
    pygame.draw.circle(screen, "black", (494, 266), 5)
    pygame.draw.circle(screen, "black", (306, 334), 5)
    pygame.draw.circle(screen, "black", (494, 334), 5)


#This controls how pacman looks on the screen and is affected by the direction Pac-Man is facing and whether it's mouth is open or not
#It draws a circle and a triangle or a line, depending on whether Pac-Man's mouth is open or closed
def drawpacman():
    if x == 0 and direction == "right":
        pygame.draw.rect(screen, "yellow", (pacxcoord-10, pacycoord-10, 20, 20), 0, 10)
        pygame.draw.polygon(screen, "black", ((pacxcoord, pacycoord), (pacxcoord+9, pacycoord+10), (pacxcoord+9, pacycoord-10)))
    elif x == 1 and direction == "right":
        pygame.draw.rect(screen, "yellow", (pacxcoord-10, pacycoord-10, 20, 20), 0, 10)
        pygame.draw.line(screen, "black", (pacxcoord, pacycoord), (pacxcoord+10, pacycoord))

    if x == 0 and direction == "left":
        pygame.draw.rect(screen, "yellow", (pacxcoord-10, pacycoord-10, 20, 20), 0, 10)
        pygame.draw.polygon(screen, "black", ((pacxcoord, pacycoord), (pacxcoord-10, pacycoord+10), (pacxcoord-10, pacycoord-10)))
    elif x == 1 and direction == "left":
        pygame.draw.rect(screen, "yellow", (pacxcoord-10, pacycoord-10, 20, 20), 0, 10)
        pygame.draw.line(screen, "black", (pacxcoord, pacycoord), (pacxcoord-10, pacycoord))

    if x == 0 and direction == "up":
        pygame.draw.rect(screen, "yellow", (pacxcoord-10, pacycoord-10, 20, 20), 0, 10)
        pygame.draw.polygon(screen, "black", ((pacxcoord, pacycoord), (pacxcoord-10, pacycoord-10), (pacxcoord+10, pacycoord-10)))
    elif x == 1 and direction == "up":
        pygame.draw.rect(screen, "yellow", (pacxcoord-10, pacycoord-10, 20, 20), 0, 10)
        pygame.draw.line(screen, "black", (pacxcoord, pacycoord), (pacxcoord, pacycoord-10))
    
    if x == 0 and direction == "down":
        pygame.draw.circle(screen, "yellow", (pacxcoord, pacycoord), 10)
        pygame.draw.polygon(screen, "black", ((pacxcoord, pacycoord), (pacxcoord+10, pacycoord+9), (pacxcoord-10, pacycoord+9)))
    elif x == 1 and direction == "down":
        pygame.draw.circle(screen, "yellow", (pacxcoord, pacycoord), 10)
        pygame.draw.line(screen, "black", (pacxcoord, pacycoord), (pacxcoord, pacycoord+10))



while menu:
    #Sets the game window to have the title of Menu and play the background noise
    pygame.display.set_caption("Menu")
    pygame.mixer.Sound.play(backgroundnoise, loops = -1)

    screen.fill("black")
    #Prints LOGAN'S to the screen in big block letters
    #LOGAN'S
    pygame.draw.polygon(screen, "white", ((210+20, 80), (210+20, 140), (250+20, 140),  (250+20, 130), (220+20, 130), (220+20, 80)))
    
    pygame.draw.polygon(screen, "white", ((270+20, 80), (260+20, 90), (260+20, 130), (270+20, 140), (300+20, 140), (310+20, 130), (310+20, 90), (300+20, 80)))
    pygame.draw.polygon(screen, "black", ((275+20, 90), (270+20, 95), (270+20, 125), (275+20, 130), (295+20, 130), (300+20, 125), (300+20, 95), (295+20, 90)))
    
    pygame.draw.polygon(screen, "white", ((370+20, 100), (370+20, 90), (360+20, 80),  (330+20, 80), (320+20, 90), (320+20, 130), (330+20, 140), (360+20, 140), (368+20, 130), (368+20, 120), (375+20, 120), (375+20, 113), (355+20, 113), (355+20, 120), (362+20, 120), (362+20, 127), (357+20, 134), (335+20, 134), (327+20, 127), (327+20, 95), (335+20, 87), (357+20, 87), (362+20, 92), (362+20, 100)))
    
    pygame.draw.polygon(screen, "white", ((400+20, 80), (380+20, 140), (390+20, 140), (397+20, 120), (423+20, 120), (430+20, 140), (440+20, 140), (420+20, 80)))
    pygame.draw.polygon(screen, "black", ((405+20, 90), (415+20, 90), (420+20, 110), (400+20, 110)))
    
    pygame.draw.polygon(screen, "white", ((445+20, 80), (445+20, 140), (455+20, 140), (455+20, 95), (485+20, 140), (495+20, 140), (495+20, 80), (485+20, 80), (485+20, 125), (455+20, 80)))

    pygame.draw.polygon(screen, "white", ((500+20, 80), (500+20, 95), (510+20, 95), (510+20, 80)))

    pygame.draw.polygon(screen, "white", ((515+20, 80), (550+20, 80), (550+20, 90), (525+20, 90), (525+20, 105), (550+20, 105), (550+20, 140), (515+20, 140), (515+20, 130), (540+20, 130), (540+20, 115), (515+20, 115)))
    
    #Loading pacman image
    title = pygame.image.load("pacman.png")
    screen.blit(title, (160, 70))

    #Prints ADVENTURE to the screen in big block letters
    #ADVENTURE
    pygame.draw.polygon(screen, "white", ((167+10, 260), (380-250+27, 320), (390-250+27, 320), (397-250+27, 300), (423-250+27, 300), (430-250+27, 320), (440-250+27, 320), (420-250+27, 260)))
    pygame.draw.polygon(screen, "black", ((405-250+27, 270), (415-250+27, 270), (420-250+27, 290), (400-250+27, 290)))
    
    pygame.draw.polygon(screen, "white", ((170+52, 260), (170+52, 320), (205+52, 320), (215+52, 310), (215+52, 270), (205+52, 260)))
    pygame.draw.polygon(screen, "black", ((180+52, 270), (180+52, 310), (203+52, 310), (207+52, 305), (207+52, 275), (203+52, 270)))

    pygame.draw.polygon(screen, "white", ((220+52, 260), (245+52, 320), (255+52, 320), (280+52, 260), (270+52, 260), (250+52, 310), (230+52, 260)))

    pygame.draw.polygon(screen, "white", ((285+52, 260), (285+52, 320), (330+52, 320), (330+52, 310), (295+52, 310), (295+52, 295), (330+52, 295), (330+52, 285), (295+52, 285), (295+52, 270), (330+52, 270), (330+52, 260)))

    pygame.draw.polygon(screen, "white", ((445-58, 80+180), (445-58, 140+180), (455-58, 140+180), (455-58, 95+180), (485-58, 140+180), (495-58, 140+180), (495-58, 80+180), (485-58, 80+180), (485-58, 125+180), (455-58, 80+180)))

    pygame.draw.polygon(screen, "white", ((500-58, 80+180), (500-58, 90+180), (520-58, 90+180), (520-58, 140+180), (530-58, 140+180), (530-58, 90+180), (550-58, 90+180), (550-58, 80+180)))

    pygame.draw.polygon(screen, "white", ((555-58, 260), (555-58, 310), (565-58, 320), (585-58, 320), (595-58, 310), (595-58, 260), (585-58, 260), (585-58, 305), (580-58, 312), (570-58, 312), (565-58, 305), (565-58, 260)))

    pygame.draw.polygon(screen, "white", ((600-58, 260), (600-58, 320), (615-58, 320), (615-58, 290), (625-58, 320), (640-58, 320), (630-58, 290), (635-58, 290), (640-58, 285), (640-58, 265), (635-58, 260)))
    pygame.draw.polygon(screen, "black", ((610-58, 265), (610-58, 285), (625-58, 285), (630-58, 280), (630-58, 270), (625-58, 265)))

    pygame.draw.polygon(screen, "white", ((285+282+20, 260), (285+282+20, 320), (330+282+20, 320), (330+282+20, 310), (295+282+20, 310), (295+282+20, 295), (330+282+20, 295), (330+282+20, 285), (295+282+20, 285), (295+282+20, 270), (330+282+20, 270), (330+282+20, 260)))
    
    #Prints the box that PLAY will go in
    pygame.draw.polygon(screen, "white", ((250, 400), (250, 520), (550, 520), (550, 400)))
    pygame.draw.polygon(screen, "black", ((260, 410), (260, 510), (540, 510), (540, 410)))
    
    #Prints PLAY to the screen in big block letters
    #PLAY
    pygame.draw.polygon(screen, "white", ((280, 420), (280, 500), (290, 500), (290, 465), (310, 465), (320, 455), (320, 430), (310, 420)))
    pygame.draw.polygon(screen, "black", ((290, 430), (290, 455), (305, 455), (310, 450), (310, 435), (305, 430)))

    pygame.draw.polygon(screen, "white", ((340, 420), (340, 500), (385, 500), (385, 490), (350, 490), (350, 420)))

    pygame.draw.polygon(screen, "white", ((175+250, 420), (155+250, 500), (165+250, 500), (172+250, 480), (198+250, 480), (205+250, 500), (215+250, 500), (195+250, 420)))
    pygame.draw.polygon(screen, "black", ((185+250, 430), (177+250, 470), (193+250, 470), (185+250, 430)))

    pygame.draw.polygon(screen, "white", ((475, 420), (495, 460), (495, 500), (505, 500), (505, 460), (525, 420), (515, 420), (500, 450), (485, 420)))

    #When the user clicks the screen it will check if it's within the PLAY buttons coordinates, and stops the menu music
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            menu = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            posx, posy = pygame.mouse.get_pos()

            if posx >= 250 and posx <= 550 and posy >= 400 and posy <= 520:
                menu = False
                game = True
                pygame.mixer.Sound.stop(backgroundnoise)
                pygame.mixer.Sound.play(maingamenoise, loops = -1)
    
    pygame.display.flip()
    clock.tick(120)

while game:
    #Add this to a channel
    
    #pygame.mixer.Sound.play(maingamenoise)

    #Checks to make sure there are still enough pellets to run the pellet eating check later
    if len(pelletlist) == 1:
        pelletlist = [(18, 18, 6, 6), (18, 58, 6, 6), (18, 98, 6, 6), (18, 138, 6, 6), (18, 178, 6, 6), (18, 218, 6, 6), (18, 258, 6, 6), (18, 298, 6, 6), 
            (18, 338, 6, 6), (18, 378, 6, 6), (18, 418, 6, 6), (18, 458, 6, 6), (18, 498, 6, 6), (18, 538, 6, 6), (18, 578, 6, 6), 
              
            (18, 18, 6, 6), (58, 18, 6, 6), (98, 18, 6, 6), (138, 18, 6, 6), (178, 18, 6, 6), (218, 18, 6, 6), (258, 18, 6, 6), 
            (298, 18, 6, 6), (338, 18, 6, 6), (378, 18, 6, 6), (418, 18, 6, 6), (458, 18, 6, 6), (498, 18, 6, 6), (538, 18, 6, 6), 
            (578, 18, 6, 6), (618, 18, 6, 6), (658, 18, 6, 6), (698, 18, 6, 6), (738, 18, 6, 6), (778, 18, 6, 6), 
              
            (58, 578, 6, 6), (98, 578, 6, 6), (138, 578, 6, 6), (178, 578, 6, 6), (218, 578, 6, 6), (258, 578, 6, 6), 
            (298, 578, 6, 6), (338, 578, 6, 6), (378, 578, 6, 6), (418, 578, 6, 6), (458, 578, 6, 6), (498, 578, 6, 6), (538, 578, 6, 6), 
            (578, 578, 6, 6), (618, 578, 6, 6), (658, 578, 6, 6), (698, 578, 6, 6), (738, 578, 6, 6), (778, 578, 6, 6), 
              
            (778, 778, 6, 6), (778, 58, 6, 6), (778, 98, 6, 6), (778, 138, 6, 6), (778, 178, 6, 6), (778, 218, 6, 6), (778, 258, 6, 6), (778, 298, 6, 6), 
            (778, 338, 6, 6), (778, 378, 6, 6), (778, 418, 6, 6), (778, 458, 6, 6), (778, 498, 6, 6), (778, 538, 6, 6), 
              
            (138, 58, 6, 6), (138, 98, 6, 6), (138, 138, 6, 6), (138, 178, 6, 6), (138, 218, 6, 6), (138, 258, 6, 6), (138, 298, 6, 6), 
            (138, 338, 6, 6), (138, 378, 6, 6), (138, 418, 6, 6), (138, 458, 6, 6), (138, 498, 6, 6), (138, 538, 6, 6),
              
            (658, 58, 6, 6), (658, 98, 6, 6), (658, 138, 6, 6), (658, 178, 6, 6), (658, 218, 6, 6), (658, 258, 6, 6), (658, 298, 6, 6), 
            (658, 338, 6, 6), (658, 378, 6, 6), (658, 418, 6, 6), (658, 458, 6, 6), (658, 498, 6, 6), (658, 538, 6, 6),

            (218, 518, 6, 6), (258, 518, 6, 6), (298, 518, 6, 6), (338, 518, 6, 6), (378, 518, 6, 6), (418, 518, 6, 6),
            (458, 518, 6, 6), (498, 518, 6, 6), (538, 518, 6, 6), (578, 518, 6, 6), 

            (218, 68, 6, 6), (258, 68, 6, 6), (298, 68, 6, 6), (338, 68, 6, 6), (378, 68, 6, 6), (418, 68, 6, 6), (458, 68, 6, 6), 
            (498, 68, 6, 6), (538, 68, 6, 6), (578, 68, 6, 6), 

            (198, 38, 6, 6), (198, 68, 6, 6), (198, 98, 6, 6), (198, 138, 6, 6), (198, 178, 6, 6), (198, 218, 6, 6), (198, 258, 6, 6), (198, 298, 6, 6), 
            (198, 338, 6, 6), (198, 378, 6, 6), (198, 418, 6, 6), (198, 458, 6, 6), (198, 488, 6, 6), (198, 518, 6, 6), (198, 548, 6, 6), 

            (598, 38, 6, 6), (598, 68, 6, 6), (598, 98, 6, 6), (598, 138, 6, 6), (598, 178, 6, 6), (598, 218, 6, 6), (598, 258, 6, 6), (598, 298, 6, 6), 
            (598, 338, 6, 6), (598, 378, 6, 6), (598, 418, 6, 6), (598, 458, 6, 6), (598, 488, 6, 6), (598, 518, 6, 6), (598, 548, 6, 6),

            (218, 168, 6, 6), (258, 168, 6, 6), (298, 168, 6, 6), (338, 168, 6, 6), (378, 168, 6, 6), (418, 168, 6, 6), (458, 168, 6, 6), 
            (498, 168, 6, 6), (538, 168, 6, 6), (578, 168, 6, 6), 

            (218, 418, 6, 6), (258, 418, 6, 6), (298, 418, 6, 6), (338, 418, 6, 6), (378, 418, 6, 6), (418, 418, 6, 6), (458, 418, 6, 6), 
            (498, 418, 6, 6), (538, 418, 6, 6), (578, 418, 6, 6), 

            (288, 188, 6, 6), (288, 218, 6, 6), (288, 258, 6, 6), (288, 298, 6, 6), (288, 338, 6, 6), (288, 378, 6, 6), (288, 398, 6, 6),

            (508, 188, 6, 6), (508, 218, 6, 6), (508, 258, 6, 6), (508, 298, 6, 6), (508, 338, 6, 6), (508, 378, 6, 6), (508, 398, 6, 6), 
            ]


    #Sets the game window to say "Pac-Man"
    pygame.display.set_caption("Pac-Man")

    #Controlling the look of the pacman
    #Every quarter of a second it will switch between open mouth and closed mouth
    y += 1
    if y == 30:
        if x == 0:
            x = 1
            y = 0
        elif x == 1:
            x = 0
            y = 0

    #Movement keys
    keys = pygame.key.get_pressed()

    #When a key is held down, if there is no rectangle on the screen that it wuld collide with when you move that way Pac-Man is allowed to go that way
    if keys[pygame.K_w]:
        for u in screenrects:
            if pygame.Rect.colliderect(Rect(pacxcoord-10, pacycoord-11, 20, 20), Rect(u)):
                k = 1
            
        if k == 0:
            direction = "up"

    if keys[pygame.K_s]:
        for u in screenrects:
            if pygame.Rect.colliderect(Rect(pacxcoord-10, pacycoord-9, 20, 20), Rect(u)):
                k = 1
        
        if k == 0:
            direction = "down"

    if keys[pygame.K_a]:
        for u in screenrects:
            if pygame.Rect.colliderect(Rect(pacxcoord-11, pacycoord-10, 20, 20), Rect(u)):
                k = 1

        if k == 0:
            direction = "left"
                
    if keys[pygame.K_d]:
        for u in screenrects:
            if pygame.Rect.colliderect(Rect(pacxcoord-9, pacycoord-10, 20, 20), Rect(u)):
                k = 1
        
        if k == 0:
            direction = "right"

    if keys[pygame.K_q]:
        game = 0

    #Resetting keys
    k = 0

    #This function checks to make sure Pac-Man doesn't go through any of the terrain, and if it doesn't it will move one pixel that direction
    if direction == "up":
        for u in screenrects:
            if pygame.Rect.colliderect(Rect(pacxcoord-10, pacycoord-11, 20, 20), Rect(u)):
                l = 1

        if l == 0:
            if pacycoord - 1 > 21:
                pacycoord -= 1

    if direction == "down":
        for u in screenrects:
            if pygame.Rect.colliderect(Rect(pacxcoord-10, pacycoord-9, 20, 20), Rect(u)):
                l = 1
        
        if l == 0:
            if pacycoord + 1 < ylimit - 21 :
                pacycoord += 1

    if direction == "left":
        for u in screenrects:
            if pygame.Rect.colliderect(Rect(pacxcoord-11, pacycoord-10, 20, 20), Rect(u)):
                l = 1

        if l == 0:
            if pacxcoord - 1 > 21 :
                pacxcoord -= 1

    if direction == "right":
        for u in screenrects:
            if pygame.Rect.colliderect(Rect(pacxcoord-9, pacycoord-10, 20, 20), Rect(u)):
                l = 1
        
        if l == 0:
            if pacxcoord + 1 < xlimit - 21 :
                pacxcoord += 1

    l = 0

    #checks to see if the user clicks the quit button on the game window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
    
    #checks to see if Pac-Man collides with any of the pellets in the pelletlist and if it does it will add 200 points to the users score and remove that pellet
    for v in range(0, len(pelletlist)):
        curpellet = pelletlist[v-2]
        if pygame.Rect.colliderect(Rect(pacxcoord-10, pacycoord-10, 20, 20), Rect(curpellet)):
            score += 200
            pelletlist.pop(v-2)


    # fill the screen with black to wipe away anything from last frame
    screen.fill("black")

    #Converting the score to a string
    tempscore = str(score)

    #This prints 0s where the score will go, and those zeros will be overwritten later
    for o in range(0, 8):
        zero = pygame.image.load("0.png")
        screen.blit(zero, (780-(6*o), 2))

    #Loads the image of the word "Score:" and blits it right before all of the zeros
    scoreimage = pygame.image.load("score.png")
    screen.blit(scoreimage, (745-(6*o), 2))

    #Takes every digit of the score string and compares it to the list of PNG files that represents digits 0-9
    for o in range(0, len(tempscore)):
        curnumber = tempscore[len(tempscore)-o-1]
        curpng = numberlist[curnumber]
        number = pygame.image.load(curpng)
        screen.blit(number, (780-(6*o), 2))
    
    #Draws everything left in the pelletlist
    for e in pelletlist:
        pygame.draw.rect(screen, "white", (e), 0, 2)

    #Calls the drawcourse and drawpacman functions we defined earlier to draw everything on the screen
    drawcourse()
    drawpacman()

    #If three seconds have passed
    if blinkytimer >= 360:
        #Resets the preferred moves that Blinky can make (Blinky is the ghost)
        blinkypreferred = []

        #compares the coordinates of Pac-Man and Blinky and updates the directions that would make Blinky get to Pac-Man
        if blinkyxcoord > pacxcoord :
            blinkypreferred.append("left")
        elif blinkyxcoord < pacxcoord:
            blinkypreferred.append("right")
        else:
            pass

        if blinkyycoord > pacycoord:
            blinkypreferred.append("up")
        elif blinkyycoord < pacycoord :
            blinkypreferred.append("down")
        else:
            pass
        
        
        #If the direction blinky would like to go is blocked by a wall, store the current direction as the past direction and go into the algorithm deciding which way it goes
        if blinkydirection == "up":
            for r in ghostscreenrects:
                if pygame.Rect.colliderect(Rect(blinkyxcoord-10, blinkyycoord-11, 20, 20), Rect(r)):
                    d = 1
                    blinkypastdirection = blinkydirection

        if blinkydirection == "down":
            for r in ghostscreenrects:
                if pygame.Rect.colliderect(Rect(blinkyxcoord-10, blinkyycoord-9, 20, 20), Rect(r)):
                    d = 1
                    blinkypastdirection = blinkydirection

        if blinkydirection == "left":
            for r in ghostscreenrects:
                if pygame.Rect.colliderect(Rect(blinkyxcoord-11, blinkyycoord-10, 20, 20), Rect(r)):
                    d = 1
                    blinkypastdirection = blinkydirection

        if blinkydirection == "right":
            for r in ghostscreenrects:
                if pygame.Rect.colliderect(Rect(blinkyxcoord-9, blinkyycoord-10, 20, 20), Rect(r)):
                    d = 1
                    blinkypastdirection = blinkydirection

        #If it has run into a wall
        if d == 1:
            #If there are more than one direction to go, make a random choice. Otherwise just choose the usable one.
            if len(blinkypreferred) > 1:
                intlist = [0, 1]
                randomint = random.choice(intlist)
            else:
                randomint = 0

            #Depending on the direction it is going, the ghost will check if it can go that way. It also will not go the opposite way, unless it can't go any other way
            #Otherwise it will go another direction that it prefers
            match blinkypreferred[randomint]:
                case "up":
                    if blinkypastdirection == "down":
                        dirlist = ["left", "right"]
                        blinkydirection = random.choice(dirlist)
                        match blinkydirection:
                            case "left":
                                for r in ghostscreenrects:
                                    if pygame.Rect.colliderect(Rect(blinkyxcoord-11, blinkyycoord-10, 20, 20), Rect(r)):
                                        s = 1
                                    
                                if s == 1:
                                    blinkydirection = "right"
                            case "right":
                                for r in ghostscreenrects:
                                    if pygame.Rect.colliderect(Rect(blinkyxcoord-9, blinkyycoord-10, 20, 20), Rect(r)):
                                        s = 1
                                    
                                if s == 1:
                                    blinkydirection = "left"
                    else:
                        blinkydirection = "up"
                   

                case "down":
                    if blinkypastdirection == "up" :
                        dirlist = ["left", "right"]
                        blinkydirection = random.choice(dirlist)
                        match blinkydirection:
                            case "left":
                                for r in ghostscreenrects:
                                    if pygame.Rect.colliderect(Rect(blinkyxcoord-11, blinkyycoord-10, 20, 20), Rect(r)):
                                        s = 1
                                    
                                if s == 1:
                                    blinkydirection = "right"
                            case "right":
                                for r in ghostscreenrects:
                                    if pygame.Rect.colliderect(Rect(blinkyxcoord-9, blinkyycoord-10, 20, 20), Rect(r)):
                                        s = 1
                                    
                                if s == 1:
                                    blinkydirection = "left"
                    else:
                        blinkydirection = "down"
                    

                case "left":
                    if blinkypastdirection == "right":
                        dirlist = ["up", "down"]
                        blinkydirection = random.choice(dirlist)
                        match blinkydirection:
                            case "up":
                                for r in ghostscreenrects:
                                    if pygame.Rect.colliderect(Rect(blinkyxcoord-10, blinkyycoord-9, 20, 20), Rect(r)):
                                        s = 1
                                    
                                if s == 1:
                                    blinkydirection = "down"
                            case "down":
                                for r in ghostscreenrects:
                                    if pygame.Rect.colliderect(Rect(blinkyxcoord-10, blinkyycoord-11, 20, 20), Rect(r)):
                                        s = 1
                                    
                                if s == 1:
                                    blinkydirection = "up"
                    else: 
                        blinkydirection = "left"

                  
                case "right":
                    if blinkypastdirection == "left":
                        dirlist = ["up", "down"]
                        blinkydirection = random.choice(dirlist)
                        match blinkydirection:
                            case "up":
                                for r in ghostscreenrects:
                                    if pygame.Rect.colliderect(Rect(blinkyxcoord-10, blinkyycoord-9, 20, 20), Rect(r)):
                                        s = 1
                                  
                                if s == 1:
                                    blinkydirection = "down"
                            case "down":
                                for r in ghostscreenrects:
                                    if pygame.Rect.colliderect(Rect(blinkyxcoord-10, blinkyycoord-11, 20, 20), Rect(r)):
                                        s = 1
                                    
                                if s == 1:
                                    blinkydirection = "up"
                    else: 
                        blinkydirection = "right"
                
        #Depending on the direction the ghost is going it will check to make sure it isn't passing through a wall
        match blinkydirection:
            case "up":
                for r in ghostscreenrects:
                    if pygame.Rect.colliderect(Rect(blinkyxcoord-10, blinkyycoord-11, 20, 20), Rect(r)):
                        blinkycollision = 1
                if blinkycollision == 0:
                    blinkyycoord -= 1
            case "down":
                for r in ghostscreenrects:
                    if pygame.Rect.colliderect(Rect(blinkyxcoord-10, blinkyycoord-9, 20, 20), Rect(r)):
                        blinkycollision = 1
                if blinkycollision == 0:
                    blinkyycoord += 1
            case "right":
                for r in ghostscreenrects:
                    if pygame.Rect.colliderect(Rect(blinkyxcoord-9, blinkyycoord-10, 20, 20), Rect(r)):
                        blinkycollision = 1
                if blinkycollision == 0:
                    blinkyxcoord += 1
            case "left":
                for r in ghostscreenrects:
                    if pygame.Rect.colliderect(Rect(blinkyxcoord-11, blinkyycoord-10, 20, 20), Rect(r)):
                        blinkycollision = 1
                if blinkycollision == 0:
                    blinkyxcoord -= 1

        #Resetting the variables
        blinkycollision = 0    
        d = 0
        s = 0

    #Finding the correct image for the direction it is going, and then printing it to the screen
    ghost = pygame.image.load(ghostlook[blinkydirection])
    screen.blit(ghost, (blinkyxcoord-10, blinkyycoord-10))

    # flip() the display to put your work on screen
    pygame.display.flip()



    #If the ghost and Pac-Man collide, stop the game, play the death noise, and transition to the game over screen
    if pygame.Rect.colliderect(Rect(blinkyxcoord-10, blinkyycoord-10, 20, 20), Rect(pacxcoord-10, pacycoord-10, 20, 20)):
        gameover = True
        pygame.mixer.Sound.stop(maingamenoise)
        pygame.mixer.Sound.play(deathnoise)
        time.sleep(2)
        pygame.mixer.Sound.stop(deathnoise)
        pygame.mixer.Sound.stop(maingamenoise)


    while gameover:
        #Sets the game window to say "Play Again?"
        pygame.display.set_caption("Play Again?")

        screen.fill("black")

        #Loading and initializing fonts, as well as what they should say
        path = pygame.font.match_font("georgia.ttf", 1)
        Font = pygame.font.Font(path, 40)

        text = Font.render("Would you like to play again?", True, "white", "black")
        text2 = Font.render("Y for yes", True, "white", "black")
        text3 = Font.render("N for no", True, "white", "black")
        text4 = Font.render("Your score was: " + str(score), True, "white", "black")

        textrect = text.get_rect()
        textrect2 = text2.get_rect()
        textrect3 = text3.get_rect()
        textrect4 = text4.get_rect()

        #Printing the text blocks
        textrect.center = (xlimit // 2, ylimit // 2-100)
        textrect2.center = (xlimit // 2 - 100, ylimit // 2)
        textrect3.center = (xlimit // 2 + 60, ylimit // 2)
        textrect4.center = (xlimit // 2 - textrect4[0] // 2, ylimit // 2 - (200 + textrect4[1]))

        screen.blit(text, textrect)
        screen.blit(text2, textrect2)
        screen.blit(text3, textrect3)
        screen.blit(text4, textrect4)

        #Checks to see if the player quits out
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameover = False
                game = False

        keys = pygame.key.get_pressed()

        #if the player hits Y, it resets all of the variables that need resetting
        if keys[pygame.K_y]:
            gameover = False

            pacxcoord = 400
            pacycoord = 250

            blinkyxcoord = 400
            blinkyycoord = 320

            blinkytimer = 0

            pelletlist = [(18, 18, 6, 6), (18, 58, 6, 6), (18, 98, 6, 6), (18, 138, 6, 6), (18, 178, 6, 6), (18, 218, 6, 6), (18, 258, 6, 6), (18, 298, 6, 6), 
            (18, 338, 6, 6), (18, 378, 6, 6), (18, 418, 6, 6), (18, 458, 6, 6), (18, 498, 6, 6), (18, 538, 6, 6), (18, 578, 6, 6), 
              
            (18, 18, 6, 6), (58, 18, 6, 6), (98, 18, 6, 6), (138, 18, 6, 6), (178, 18, 6, 6), (218, 18, 6, 6), (258, 18, 6, 6), 
            (298, 18, 6, 6), (338, 18, 6, 6), (378, 18, 6, 6), (418, 18, 6, 6), (458, 18, 6, 6), (498, 18, 6, 6), (538, 18, 6, 6), 
            (578, 18, 6, 6), (618, 18, 6, 6), (658, 18, 6, 6), (698, 18, 6, 6), (738, 18, 6, 6), (778, 18, 6, 6), 
              
            (58, 578, 6, 6), (98, 578, 6, 6), (138, 578, 6, 6), (178, 578, 6, 6), (218, 578, 6, 6), (258, 578, 6, 6), 
            (298, 578, 6, 6), (338, 578, 6, 6), (378, 578, 6, 6), (418, 578, 6, 6), (458, 578, 6, 6), (498, 578, 6, 6), (538, 578, 6, 6), 
            (578, 578, 6, 6), (618, 578, 6, 6), (658, 578, 6, 6), (698, 578, 6, 6), (738, 578, 6, 6), (778, 578, 6, 6), 
              
            (778, 778, 6, 6), (778, 58, 6, 6), (778, 98, 6, 6), (778, 138, 6, 6), (778, 178, 6, 6), (778, 218, 6, 6), (778, 258, 6, 6), (778, 298, 6, 6), 
            (778, 338, 6, 6), (778, 378, 6, 6), (778, 418, 6, 6), (778, 458, 6, 6), (778, 498, 6, 6), (778, 538, 6, 6), 
              
            (138, 58, 6, 6), (138, 98, 6, 6), (138, 138, 6, 6), (138, 178, 6, 6), (138, 218, 6, 6), (138, 258, 6, 6), (138, 298, 6, 6), 
            (138, 338, 6, 6), (138, 378, 6, 6), (138, 418, 6, 6), (138, 458, 6, 6), (138, 498, 6, 6), (138, 538, 6, 6),
              
            (658, 58, 6, 6), (658, 98, 6, 6), (658, 138, 6, 6), (658, 178, 6, 6), (658, 218, 6, 6), (658, 258, 6, 6), (658, 298, 6, 6), 
            (658, 338, 6, 6), (658, 378, 6, 6), (658, 418, 6, 6), (658, 458, 6, 6), (658, 498, 6, 6), (658, 538, 6, 6),

            (218, 518, 6, 6), (258, 518, 6, 6), (298, 518, 6, 6), (338, 518, 6, 6), (378, 518, 6, 6), (418, 518, 6, 6),
            (458, 518, 6, 6), (498, 518, 6, 6), (538, 518, 6, 6), (578, 518, 6, 6), 

            (218, 68, 6, 6), (258, 68, 6, 6), (298, 68, 6, 6), (338, 68, 6, 6), (378, 68, 6, 6), (418, 68, 6, 6), (458, 68, 6, 6), 
            (498, 68, 6, 6), (538, 68, 6, 6), (578, 68, 6, 6), 

            (198, 38, 6, 6), (198, 68, 6, 6), (198, 98, 6, 6), (198, 138, 6, 6), (198, 178, 6, 6), (198, 218, 6, 6), (198, 258, 6, 6), (198, 298, 6, 6), 
            (198, 338, 6, 6), (198, 378, 6, 6), (198, 418, 6, 6), (198, 458, 6, 6), (198, 488, 6, 6), (198, 518, 6, 6), (198, 548, 6, 6), 

            (598, 38, 6, 6), (598, 68, 6, 6), (598, 98, 6, 6), (598, 138, 6, 6), (598, 178, 6, 6), (598, 218, 6, 6), (598, 258, 6, 6), (598, 298, 6, 6), 
            (598, 338, 6, 6), (598, 378, 6, 6), (598, 418, 6, 6), (598, 458, 6, 6), (598, 488, 6, 6), (598, 518, 6, 6), (598, 548, 6, 6),

            (218, 168, 6, 6), (258, 168, 6, 6), (298, 168, 6, 6), (338, 168, 6, 6), (378, 168, 6, 6), (418, 168, 6, 6), (458, 168, 6, 6), 
            (498, 168, 6, 6), (538, 168, 6, 6), (578, 168, 6, 6), 

            (218, 418, 6, 6), (258, 418, 6, 6), (298, 418, 6, 6), (338, 418, 6, 6), (378, 418, 6, 6), (418, 418, 6, 6), (458, 418, 6, 6), 
            (498, 418, 6, 6), (538, 418, 6, 6), (578, 418, 6, 6), 

            (288, 188, 6, 6), (288, 218, 6, 6), (288, 258, 6, 6), (288, 298, 6, 6), (288, 338, 6, 6), (288, 378, 6, 6), (288, 398, 6, 6),

            (508, 188, 6, 6), (508, 218, 6, 6), (508, 258, 6, 6), (508, 298, 6, 6), (508, 338, 6, 6), (508, 378, 6, 6), (508, 398, 6, 6), 
            ]

            direction = "up"

            score = 0

            pygame.mixer.Sound.play(maingamenoise, loops = -1)

        #If they hit N, the game ends
        if keys[pygame.K_n]:
            gameover = False
            game = False

        pygame.display.flip()
        clock.tick(120)


    #Increasing the blinkytimer to count to 3 seconds
    blinkytimer += 1

    clock.tick(120)  # limits FPS to 120



pygame.quit()