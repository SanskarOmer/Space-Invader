import pygame as pg
import random
import math
from pygame import mixer

#initalize py game
pg.init()

#created a screen
screen=pg.display.set_mode((800,600))

#background
background=pg.image.load('background.png')

#adding background music
mixer.music.load('background.wav')
mixer.music.play(-1)

#giving title to window
pg.display.set_caption("Space Invaders")


#giving icon to window
icon=pg.image.load('spaceship.png')
pg.display.set_icon(icon)


#player
playerImg=pg.image.load('arcade-game.png')
playerX=370
playerY=480
playerChangeX=0
playerChangeY=0

#enemy 
enemyImg=[]
enemyX=[]
enemyY=[]
enemyChangeX=[]
enemyChangeY=[]
no_of_enemies=6

for i in range(no_of_enemies):
    enemyImg.append(pg.image.load('alien.png'))
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(0,100))
    enemyChangeX.append(0.5)
    enemyChangeY.append(40)


#bullet
bulletImg=pg.image.load('bullet.png')
bulletX=0
bulletY=480
bulletChangeX=0
bulletChangeY=1.7

#ready means bullet is not fired
bulletState="ready"



#score
scoreValue=0
font=pg.font.Font('freesansbold.ttf', 32)

over=pg.font.Font('freesansbold.ttf', 64)

textX=10
textY=10

def showScore(x,y):

    score= font.render("Score : " + str(scoreValue),True,(255,255,255))

    screen.blit(score,(x,y))


def gameOver():
    overText= over.render("GAME OVER",True,(255,255,255))

    screen.blit(overText,(200,250))




def player(x,y):
    screen.blit(playerImg,(x,y))


def enemy(x,y,i):
    screen.blit(enemyImg[i],(x,y))

def fireBullet(x,y):
   global bulletState
   bulletState="fired"
   screen.blit(bulletImg,(x+16,y+10))

def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance=math.sqrt((math.pow(enemyX-bulletX,2))+(math.pow(enemyY-bulletY,2)))
    if distance<27:
        return True
    else:
        return False




#Game Loop
running=True

while running:
     #filling color
    screen.fill((0,0,0))
    #background image
    screen.blit(background,(0,0))

    for event in pg.event.get():
        if event.type==pg.QUIT:
            running=False
    #if keystroke is pressed check right or left
        if event.type==pg.KEYDOWN:
    
            if event.key==pg.K_LEFT:
                playerChangeX=-1.3
            if event.key==pg.K_RIGHT:
                playerChangeX=1.3

#for up down movement
            # if event.key==pg.K_UP:
            #     playerChangeY=-1.3
            # if event.key==pg.K_DOWN:
                # playerChangeY=1.3
            if event.key==pg.K_SPACE:
               if bulletState == "ready":
                 bulletSound=mixer.Sound('laser.wav')
                 bulletSound.play()
                 bulletX=playerX
                 fireBullet(bulletX,bulletY)

        if event.type==pg.KEYUP:
            if event.key==pg.K_LEFT or event.key==pg.K_RIGHT or event.key==pg.K_UP or event.key==pg.K_DOWN: 
                playerChangeX=0
                # playerChangeY=0

   
    
    playerX+=playerChangeX
    #setting boundary at x cordinate
    if playerX<=0:
        playerX=0
    elif playerX>=736:
        playerX=736


    playerY+=playerChangeY 

#for up down movement

    #setting boundary at y coordinate
    # if playerY<=0:
    #     playerY=0
    # elif playerY>=536:
    #     playerY=536

#movement for enemy
    for i in range(no_of_enemies):
        #game over

        if enemyY[i]>440:
            for j in range(no_of_enemies):
                enemyY[j]=2000
            overSound=mixer.Sound('gameover.wav')
            # overSound.play()
            gameOver()
            break



        enemyX[i]+=enemyChangeX[i]
    
        if enemyX[i]<=0:
            enemyChangeX[i]=0.5
            enemyY[i]+=enemyChangeY[i]
        elif enemyX[i]>=736:
            enemyChangeX[i]=-0.5
            enemyY[i]+=enemyChangeY[i]


    #Collision
        collision=isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
            explosionSound=mixer.Sound('explosion.wav')
            explosionSound.play()


            bulletY=480
            bulletState="ready"
            scoreValue+=1
            
            enemyX[i]=random.randint(0,730)
            enemyY[i]=random.randint(0,100)

        enemy(enemyX[i],enemyY[i],i)

#bullet movement
    if bulletY<=0:
        bulletY=480
        bulletState="ready"
    if bulletState == "fired":
        fireBullet(bulletX,bulletY)
        bulletY-=bulletChangeY





    #apearing character
    player(playerX,playerY)
    showScore(textX,textY)
    pg.display.update()

  
