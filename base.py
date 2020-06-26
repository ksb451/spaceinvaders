import pygame
import os
import time
import random

WIDTH,HEIGHT=900,600
MAX_LVL=10
WAV_PER_LVL={
    1:7,
    2:9,
    3:11,
    4:13,
    5:15,
    6:7,
    7:9,
    8:11,
    9:13,
    10:15
}

WIN=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Space Invaders")
ICON=pygame.image.load(os.path.join("assets","icon.png"))
pygame.display.set_icon(ICON)

#load assets
RED_SPACESHIP=pygame.image.load(os.path.join("assets","spaceship_red_64.png"))
GREEN_SPACESHIP=pygame.image.load(os.path.join("assets","spaceship_green_64.png"))
BLUE_SPACESHIP=pygame.image.load(os.path.join("assets","spaceship_blue_64.png"))
#player
YELLOW_SPACESHIP=pygame.image.load(os.path.join("assets","spaceship_player_64.png"))
#bullets
ENEMY_BULLET=pygame.image.load(os.path.join("assets","bullet_enemy_24.png"))
PLAYER_BULLET=pygame.image.load(os.path.join("assets","bullet_player_32.png"))

#background
BG=pygame.transform.scale(pygame.image.load(os.path.join("assets","background-black.png")),(WIDTH,HEIGHT))


class Ship(object):
    COOLDOWN = 20


    def __init__(self,x,y,health=100):
        self.x = x;
        self.y = y;
        self.health=health
        self.ship_img=None
        self.bullet_img=None
        self.bullets=[]
        self.cool_down_counter = 0

    def draw(self,window):
        for bullet in self.bullets:
            bullet.draw(WIN)
        window.blit(self.ship_img,(self.x, self.y))

    def move_lasers(self,vel,obj):
        self.cooldown()
        for bullet in self.bullets:
            bullet.move(vel)
            if bullet.off_screen(HEIGHT):
                self.bullets.remove(bullet)
            elif bullet.collison(obj):
                obj.health-=10
                self.bullets.remove(bullet)


    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter=0
        elif self.cool_down_counter > 0:
            self.cool_down_counter +=1

    def shoot(self,x,y):
        if(self.cool_down_counter == 0):
            bullet=Laser(self.x+self.ship_img.get_width()/4,self.y,self.bullet_img)
            self.bullets.append(bullet)
            self.cool_down_counter=1

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()


class Player(Ship):
    def __init__(self,x,y,health=100):
        super().__init__(x,y,health)
        #self.player_vel=5
        self.ship_img = YELLOW_SPACESHIP
        self.bullet_img= PLAYER_BULLET
        self.mask= pygame.mask.from_surface(self.ship_img)
        self.max_health = health
    
    def shoot(self):
        super().shoot(self.x+self.ship_img.get_width()/4,self.y)

    def move_lasers(self,vel,objs):
        self.cooldown()
        for bullet in self.bullets:
            bullet.move(vel)
            if bullet.off_screen(HEIGHT):
                self.bullets.remove(bullet)
            else:
                for obj in objs:
                    if bullet.collison(obj):
                        objs.remove(obj)
                        self.bullets.remove(bullet)
    
    def draw(self,window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0,255,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health), 10))

class Enemy(Ship):
    COLOR_MAP = {
                "red":(RED_SPACESHIP,ENEMY_BULLET),
                "green":(GREEN_SPACESHIP,ENEMY_BULLET),
                "blue":(BLUE_SPACESHIP,ENEMY_BULLET)
                }
    
    def __init__(self,x,y,color,health=100):
        super().__init__(x,y,health)
        self.ship_img, self.bullet_img = self.COLOR_MAP[color]
        self.mask=pygame.mask.from_surface(self.ship_img)
        self.vel_x=2
        self.vel_y=1
        self.dir=-1
    
    def shoot(self):
        super().shoot(self.x+self.ship_img.get_width()/4,self.y+2*self.ship_img.get_height())

    def move(self):
        self.y+=self.vel_y
        if(self.x<=0):
            self.dir*=-1
        if(self.x>=WIDTH):
            self.dir*=-1
        self.x+=self.dir*self.vel_x

class Laser:
    def __init__(self,x,y,img):
        self.x=x
        self.y=y
        self.img=img
        self.mask=pygame.mask.from_surface(self.img)
    
    def draw(self,window):
        window.blit(self.img,(self.x,self.y))

    def move(self,vel):
        self.y += vel

    def off_screen(self,height):
        return not(self.y <= height and self.y >= 0)

    def collison(self,obj):
        return collide(self,obj)


def collide(obj1,obj2):
    offset_x = int(obj2.x - obj1.x)
    offset_y = int(obj2.y - obj1.y)
    return obj1.mask.overlap(obj2.mask,(offset_x,offset_y)) !=None
