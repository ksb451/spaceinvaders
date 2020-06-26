import pygame
import os
import time
import random
from base import *
pygame.init()
pygame.font.init()

def main():
    run=True
    lost =False
    lost_count=0
    FPS=60
    level = 1
    lives = 5
    main_font=pygame.font.SysFont("comicsans", 50, bold=False, italic=False)
    lost_font=pygame.font.SysFont("comicsans", 100, bold=False, italic=False)
    
    enemies = []
    wave_length = 5

    #enemy_vel=1
    laser_vel=10
    player_vel=5

    player=Player(375,450)

    clock=pygame.time.Clock()

    def redraw_window():
        WIN.blit(BG,(0,0))
        #draw test
        lives_lable=main_font.render("Lives: "+str(lives),1,(255,255,255))
        level_lable=main_font.render("Level: "+str(level),1,(255,255,255))

        WIN.blit(lives_lable,(10,10))
        WIN.blit(level_lable,(WIDTH-level_lable.get_width()-10,10))
        
        for enemy in enemies:
            enemy.draw(WIN)

        player.draw(WIN)

        if lost:
            lost_label= lost_font.render("You Lost!!",1,(255, 0, 0))
            WIN.blit(lost_label, (WIDTH/2-lost_label.get_width()/2,300))

        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()

        if lives <=0 or player.health <= 0:
            lost=True
            lost_count+=1

        if lost:
            if lost_count> FPS*3:
                run=False
            else:
                continue

        if(len(enemies)==0):
            level+=1
            wave_length+=5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50,WIDTH-100),random.randrange(-1500,-100),random.choice(["red","blue", "green"]))
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                    run=False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player_vel > 0 :
            player.x-=player_vel
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH :
            player.x+=player_vel
        if keys[pygame.K_w] and player.y - player_vel > 0 :
            player.y-=player_vel
        if keys[pygame.K_s] and player.y + player_vel + player.get_height() +20 < HEIGHT :
            player.y+=player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()

 
        for enemy in enemies:
            enemy.move()
            enemy.move_lasers(laser_vel, player)

            if level>=1:
                if random.randrange(0,3*FPS)==1:
                    enemy.shoot()

            if collide(enemy, player):
                player.health-=10
                enemies.remove(enemy)

            elif(enemy.y+enemy.get_height() > HEIGHT):
                lives-=1
                enemies.remove(enemy)
            
            
        player.move_lasers(-laser_vel, enemies)


def main_menu():
    title_font = pygame.font.SysFont("comicsans", 70)
    run=True
    while run:
        WIN.blit(BG, (0,0))
        title_label = title_font.render("Press the mouse to begin...", 1, (255,255,255))
        WIN.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 350))
        pygame.display.update() 
        for event in pygame.event.get():
            if event.type== pygame.QUIT:
                run= False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()


main_menu()

