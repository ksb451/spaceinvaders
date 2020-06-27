import pygame
import os
import time
import random
from base import *
from button import *

pygame.init()
pygame.font.init()

def main():
    run=True
    lost =False
    FPS=60
    level = 0
    lives = 10
    score=0
    main_font=pygame.font.SysFont("comicsans", 30, bold=False, italic=False)
    #lost_font=pygame.font.SysFont("comicsans", 100, bold=False, italic=False)
    
    enemies = []
    wave_length = 0

    #enemy_vel=1
    laser_vel=10
    player_vel=7

    player=Player(375,450)

    clock=pygame.time.Clock()

    def redraw_window():
        WIN.blit(BG,(0,0))
        #draw test
        score_label=main_font.render("Score: "+str(score),1,(255,255,255))
        lives_lable=main_font.render("Lives: "+str(lives),1,(255,255,255))
        level_lable=main_font.render("Level: "+str(level),1,(255,255,255))

        WIN.blit(lives_lable,(10,10))
        WIN.blit(score_label,(10,10+lives_lable.get_height()))
        WIN.blit(level_lable,(WIDTH-level_lable.get_width()-10,10))
        
        for enemy in enemies:
            enemy.draw(WIN)

        player.draw(WIN)

        # if lost:
        #     lost_label= lost_font.render("You Lost!!",1,(255, 0, 0))
        #     WIN.blit(lost_label, (WIDTH/2-lost_label.get_width()/2,300))

        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()

        if lives <=0 or player.health <= 0:
            lost=True

        if lost:
            game_over_menu(score)
        
        if(len(enemies)==0):
            level+=1
            if level <=6:
                wave_length=WAV_PER_LVL[level%3]
            else:
                wave_length=random.randint(13,17)
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50,WIDTH-100),random.randrange(-1000,-100),random.choice(["red","blue", "green"]),level)
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                    run=False
                    exit()

        keys = pygame.key.get_pressed()
        if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and player.x - player_vel > 0 :
            player.x-=player_vel
        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and player.x + player_vel + player.get_width() < WIDTH :
            player.x+=player_vel
        if (keys[pygame.K_w] or keys[pygame.K_UP]) and player.y - player_vel > 0 :
            player.y-=player_vel
        if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and player.y + player_vel + player.get_height() +20 < HEIGHT :
            player.y+=player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()

 
        for enemy in enemies:
            enemy.move()
            enemy.move_lasers(laser_vel, player)

            if level>=4:
                shoot_speed=3
                if level>8:
                    shoot_speed=2
                if random.randrange(0,shoot_speed*FPS)==1:
                    enemy.shoot()

            if collide(enemy, player):
                player.health-=10
                enemies.remove(enemy)

            elif(enemy.y+enemy.get_height() > HEIGHT):
                lives-=1
                enemies.remove(enemy)
            
            
        if player.move_lasers(-laser_vel, enemies):
            score+=1


def main_menu():
    title_font = pygame.font.SysFont("comicsans", 70)
    rule_font = pygame.font.SysFont("comicsans",40)
    run=True
    while run:
        WIN.blit(BG, (0,0))
        WIN.blit(YELLOW_SPACESHIP,(200-ICON.get_width()/2,101))
        name_label = title_font.render("Space Invaders", 1, (0,0,255))
        WIN.blit(name_label, (200+ICON.get_width()+30,105))
        rule_label_1 = rule_font.render("W,A,S,D or UP,DOWN,LEFT,RIGHT to move", 1,(0,255,0))
        rule_label_2 = rule_font.render("SPACE to Shoot", 1,(0,255,0))
        rule_label_3 = rule_font.render("Dont let more than 10 enemies get away", 1,(0,255,0))
        WIN.blit(rule_label_1,(WIDTH/2-rule_label_1.get_width()/2,200))
        WIN.blit(rule_label_2,(WIDTH/2-rule_label_2.get_width()/2,250))
        WIN.blit(rule_label_3,(WIDTH/2-rule_label_3.get_width()/2,300))
        title_label = title_font.render("Press the mouse to begin...", 1, (255,255,255))
        WIN.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 450))
        pygame.display.update() 
        for event in pygame.event.get():
            if event.type== pygame.QUIT:
                run= False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()

def game_over_menu(score):
    restart_button=Button((0,255,0), WIDTH/2, HEIGHT-100, 150, 50, "Play Again", (255,255,255))
    score_font= pygame.font.SysFont("comicsans", 50)
    run = True
    while run:
        WIN.blit(BG,(0,0))
        score_label= score_font.render("Your Score: "+str(score),1,(0,255,0))
        WIN.blit(GAMEOVER_TEXT,(WIDTH/2-GAMEOVER_TEXT.get_width()/2,HEIGHT/2-GAMEOVER_TEXT.get_height()/2-score_label.get_height()))
        WIN.blit(score_label, (WIDTH/2-score_label.get_width()/2,HEIGHT/2+GAMEOVER_TEXT.get_height()/2-score_label.get_height()))
        restart_button.draw(WIN, (255,0,0))
        pygame.display.update()

        for event in pygame.event.get():
            pos=pygame.mouse.get_pos()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.isOver(pos):
                    print("clicked the button")
                    main()
            if event.type == pygame.QUIT:
                run=False
                exit()
            if event.type == pygame.MOUSEMOTION:
                if restart_button.isOver(pos):
                    restart_button.color=(0,0,255)
                else:
                    restart_button.color=(0,255,0)

main_menu()

