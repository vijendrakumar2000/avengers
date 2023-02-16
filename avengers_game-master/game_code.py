# IMPORTING IMPORTANT LIBRARY
import pygame
import random
import math

# INTIALIZING PYGAME LIBRBAY
pygame.init()
# CREATING A GAME SCREEN

screen = pygame.display.set_mode((600, 600))
# SETTING A CAPTION
pygame.display.set_caption("FIGHT FOR THE PLANET TITAN")

# SETTING ICON
icon = pygame.image.load("1.png")
pygame.display.set_icon(icon)
# SETTING BACKGROUND IMAGE
background = pygame.image.load("back.jpeg")

# ADDING BACKGROUND MUSIC
from pygame import mixer
mixer.music.load('The Avengers Theme Song.mp3')
mixer.music.play(-1)

# CREATING ENEMIES

enemyimg = []
enemy_x = []
enemy_y = []
enemy_x_change=[]
enemy_y_change=[]
num_enemy=3
for i in range (num_enemy):

    enemyimg.append(pygame.image.load("thanos.png"))
    enemy_x.append( random.randint(0, 600))
    enemy_y.append( random.randint(30, 40))
    enemy_x_change.append(0.2)
    enemy_y_change.append(0)

# CREATING A BULLET
bulletimg = pygame.image.load("bullet.png")
bullet_x = 0
bullet_y = 500
bulletx_change = 0
bullety_change = 0.30
bullet_state = "ready"


# CREATING OUR HERO
playerimg = pygame.image.load('ironman.png')
playerx = 250
playery = 500
playerx_change = 0
playery_change = 0

# SETTING FONT
font=pygame.font.Font('docktrin.ttf',24)
text_x=10
text_y=570
over_text=pygame.font.Font('docktrin.ttf',50)

# GAME OVER FUNCTION
def game_over():
    over = over_text.render("AVENGERS LOST" , True, (0, 255, 255))
    screen.blit(over, (130, 240))



# SCORE FUNCTION

def s_score(x,y):
    score=font.render("BRING ME THANOS:"+str(score_value),True ,(0,255,255))
    screen.blit(score, (x, y))

# PLAYER FUNCTION

def player(x, y):
    screen.blit(playerimg, (x, y))

# ENMENY FUNCTION
def enemy(x, y,i):
    screen.blit(enemyimg[i], ((x, y)))

# BULLET FUNCTION
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg, (x + 15, y))

# CHECKING COLLISON

def iscollison(enemy_x, enemy_y, bullet_x, bullet_y):
    dis = math.sqrt((math.pow(enemy_x - bullet_x, 2)) + (math.pow(enemy_y - bullet_y, 2)))
    if dis < 30:
        return True
    else:
        return False


score_value=0

running = True
# THIS IS AN INFINITE LOOP WHERE OUR GAME RUNS
while running:
    # ADDING AN BACKGROUND BACKGROUND IMAGE


    screen.blit(background, ((0, 0)))
    # SO THIS ARE WHERE OUR EVENTS TAKE PLACE
    for event in pygame.event.get():
        # THIS IS TO QUIT THE GAME
        if event.type == pygame.QUIT:
            running = False


        # CHECKING IF KEYS ARE  PRESSED AND ASSIGNING PLAYER MOVEMENT


        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerx_change = -0.3
            if event.key == pygame.K_RIGHT:
                playerx_change = +0.3


        # ASSIGNING THE SPACE TO FIRE BULLET
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound= mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bullet_x = playerx
                fire_bullet(bullet_x, bullet_y)


# CHECKING THE KEY IS RELEASED
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerx_change = 0.0
# ASSIGING THE UPWARD & DOWNWARD MOVEMENT

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                playery_change = -0.1
            if event.key == pygame.K_DOWN:
                playery_change = +0.1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playery_change = 0.0

    playery += playery_change
    playerx += playerx_change
#DECIDING THE BOUNDARIES IN WHICH PLAYER CAN MOVE
    if playery <= 0:
        playery = 0
    if playery > 540:
        playery = 540

    if playerx <= 0:
        playerx = 0
    if playerx > 540:
        playerx = 540

# MULTIPLE BULLET
    if bullet_y <= 0:
        bullet_y = 480
        bullet_state = "ready"


# ENEMY MOVEMENT
    for i in range(num_enemy):
        # HERE IF ENEMY TOUCHES THE PLAYER GAME SHOULD BE OVER
        if enemy_y[i]>440:
            for j in range(num_enemy):
                enemy_y[j]=1000
            game_over()
        # ENEMY MOVING CONTINOUSLY
        enemy_x[i] += enemy_x_change[i]
        enemy_y[i]+= enemy_y_change[i]
        # HERE IF THE ENEMY HIT LEFT BORDER IT WILL GO RIGHT AND WILL GO DOWN BY SOME DISTANCE
        if enemy_x[i] <= 0:
           enemy_x_change[i] = 0.2
           enemy_y_change[i] = 0.01
        # HERE IF THE ENEMY HIT RIGHT BORDER IT WILL GO LEFT AND WILL GO DOWN BY SOME DISTANCE
        if enemy_x[i]> 540:
           enemy_x_change[i] = -0.2
           enemy_y_change[i] = 0.01
        # CHECKING COLLISION
        collison = iscollison(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
        if collison:
            collison_sound=mixer.Sound('snap.wav')
            collison_sound.play()
            # IF COLLIDED RESET THE BULLET AND INCREASE THE SCORE
            bullet_y = 500
            bullet_state = "ready"
            score_value+= 10
           # IF COLLIDED RESET THE ENEMY POISTION
            enemy_x[i] = random.randint(0, 600)
            enemy_y[i] = random.randint(0, 30)
        enemy(enemy_x[i], enemy_y[i],i)

 # FIRING THE BULLET WHEN SPACE IS PRESSED
    if bullet_state is "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullety_change

 # calling the player and score function
    player(playerx, playery)
    s_score(text_x,text_y)

# most important updating the display
    pygame.display.update()
