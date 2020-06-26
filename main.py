import random
import math
import pygame
from pygame import mixer

#Intitalize pygame
pygame.init()

#creating the screen
screen=pygame.display.set_mode((800,600))

#creating background
background=pygame.image.load("background.png")
#background sound
#mixer.music.load("background.wav")
#mixer.music.play(-1)
#title and icon

pygame.display.set_caption("Space Invaders")
icon=pygame.image.load("spaceship.png")
pygame.display.set_icon(icon)

#ENEMYICON
enemyImg=[]
enemyX=[]
enemyY=[]
enemyX_change=[]
enemyY_change=[]
num_of_enemies=6
for i in range (num_of_enemies):
    enemyImg.append(pygame.image.load("ufo.png"))
    enemyX.append(random.randint(0,800))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(2)
    enemyY_change.append(.2)

def enemy(x, y,):
    screen.blit(enemyImg[1], (x,y), area=None, special_flags = 0)

#playericon

playerImg=pygame.image.load("spaceship(1).png")
PlayerX=370
PlayerY=480
PlayerX_change = 0
PlayerY_change = 0

#bullet
bulletImg=pygame.image.load("bullet.png")
bulletX=0
bulletY=0
bulletX_change=0
bulletY_change=10
bullet_state="ready"

#score
score_value=0;
textX=10
textY=10
font = pygame.font.Font('freesansbold.ttf',32)
over_font=pygame.font.Font('freesansbold.ttf',48)
def show_score(x,y):
    score=font.render("Score: "+ str(score_value),True, (255,255,255))
    screen.blit(score,(x,y))

gameoverstatus=False

def game_over_text():
    over=over_font.render("Game Over",True,(255,255,255))
    screen.blit(over,(300,280))

def fire_bullet(x,y):
    global bullet_state
    bullet_state="fire"
    screen.blit(bulletImg,(x+16,y+5))

#collison

def inCollison(enemyX,enemyY,bulletX,bulletY):
    distance=math.sqrt((math.pow(enemyX-bulletX,2)) + (math.pow(enemyY-bulletY,2)))
    if distance<27:
        return True
    else:
        return False

def distrancebw(PlayerX,PlayerY,enemyX,enemyY):
    return math.sqrt((math.pow(enemyX-PlayerX,2)) + (math.pow(enemyY-PlayerY,2)))

#draw the player onto the screen
def player(x,y):
    screen.blit(playerImg, (x,y), area=None, special_flags = 0)


#game loop
running = True
while running:
    #rgb values
    screen.fill((0,0,22))
    screen.blit(background,(0,0))

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running = False

        #if keystroke is pressed chaeck which key is pressed
        if event.type==pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                PlayerX_change = -5
            if event.key == pygame.K_RIGHT:
                PlayerX_change = 5
            if event.key == pygame.K_UP:
                PlayerY_change = -5
            if event.key == pygame.K_DOWN:
                PlayerY_change = 5
            if event.key == pygame.K_SPACE and bullet_state=="ready":
                #bullet_sound=mixer.Sound('laser.wav')
                #bullet_sound.play()
                bulletX=PlayerX
                bulletY=PlayerY
                fire_bullet(bulletX,bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT :
                PlayerX_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                PlayerY_change=0
    if gameoverstatus==False:
        #the player
        PlayerY+= PlayerY_change
        if PlayerY >= 480:
            PlayerY = 480
        elif PlayerY <= 300:
            PlayerY = 300
        PlayerX += PlayerX_change
        if PlayerX <= 0:
            PlayerX = 0
        elif PlayerX >= 736:
            PlayerX = 736
        #enemy movement
        for i in range (num_of_enemies):

            #gameover

            if(distrancebw(PlayerX,PlayerY,enemyX[i],enemyY[i])<=20):
                for j in range(num_of_enemies):
                    enemyY[j]=2000
                game_over_text()
                gameoverstatus=True
                break


            enemyX[i]+=enemyX_change[i]
            enemyY[i] += enemyY_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = 2
                #enemyY+=enemyY_change
            elif enemyX[i] >= 736:
                enemyX_change[i] = -2
                #enemyY+=enemyY_change
            
            #collison
            collison=inCollison(enemyX[i],enemyY[i],bulletX,bulletY)
            if collison:
                #expolsionsound=mixer.Sound('explosion.wav')
                #expolsionsound.play()
                bulletY=0
                bullet_state="ready"
                score_value+=1
                enemyX[i]=random.randint(100,700)
                enemyY[i]=random.randint(50,150)
            
            enemy(enemyX[i],enemyY[i])
        #bullet movement
        if bullet_state=="fire":
            fire_bullet(bulletX,bulletY)
            bulletY-=bulletY_change
        if(bulletY<=0):
            bullet_state="ready"
        player(PlayerX,PlayerY)
    else:
        game_over_text()
    show_score(textX,textY)
    #update command after every change
    pygame.display.update()