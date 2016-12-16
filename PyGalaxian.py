#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import pygame
import sys
import time
import math
import random
from pygame.locals import *

pygame.init()
#스크린 사이즈 셋업
size = (width, height) = (1024, 600)
#size = (width,height) = (1024,600)
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 155, 0)
red = (155, 0, 0)
sky = (0, 0, 0)
clock = pygame.time.Clock()
FPS = 40

maxspeed = 15
maxpower = 4

#screen = pygame.display.set_mode(size)
screen = pygame.display.set_mode(size)


#유저와 적사이의 위치에 따라 적이 자동 이동
def cpumove(cpu, target):
    if target.rect.left < cpu.rect.left:
        cpu.trigger = 1
        cpu.speed = cpu.speed -2
    elif target.rect.left > cpu.rect.left:
        cpu.trigger = 1
        cpu.speed = cpu.speed + 2
    if random.randrange(0, 30) == 1:
        cpu.fire = 5
    else:
        cpu.fire = 0

#보스와 적사이의 위치에 따라 적이 자동 이동
def bossmove(cpu, target):
    if target.rect.left < cpu.rect.left and cpu.spree == False:
        cpu.trigger = 1
        cpu.speed = -2
    elif target.rect.left > cpu.rect.left and cpu.spree == False:
        cpu.trigger = 1
        cpu.speed = 2

    if random.randrange(0, 3) == 1 and cpu.spree == False:
        cpu.bulletformation = 0
        cpu.bulletspeed = 20
        cpu.fire = 1
    else:
        cpu.fire = 0

    if cpu.spree == False and random.randrange(0, 250) == 71:
        cpu.spree = True
    else:
        pass

#이미지 로딩
def load_image(
    name,
    sizex=-1,
    sizey=-1,
    colorkey=None,
    ):

    fullname = os.path.join('Sprites', name)
    image = pygame.image.load(fullname)
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)

    if sizex != -1 or sizey != -1:
        image = pygame.transform.scale(image, (sizex, sizey))

    return (image, image.get_rect())

#체력 바
def showhealthbar(
    health,
    barcolor,
    pos,
    unit,
    ):

    healthbar = pygame.Surface((health * unit, 10), pygame.SRCALPHA, 32)
    healthbar = healthbar.convert_alpha()
    pygame.draw.rect(screen, barcolor, pos)

#게임내 텍스트 처리 타이틀,로고,메뉴
def displaytext(
    text,
    fontsize,
    x,
    y,
    color,
    ):

    font = pygame.font.SysFont('sawasdee', fontsize, True)
    text = font.render(text, 1, color)
    textpos = text.get_rect(centerx=x, centery=y)
    screen.blit(text, textpos)

#플레이어 움직임 계산
def moveplayer(Player):
    if Player.isautopilot == False:
        if Player.rect.left >= 0 and Player.rect.right <= width:
            if Player.trigger == 1:
                Player.movement[0] = Player.movement[0] + Player.speed
                if Player.movement[0] < -maxspeed:
                    Player.movement[0] = -maxspeed
                elif Player.movement[0] > maxspeed:
                    Player.movement[0] = maxspeed
            elif Player.movement[0] >= -maxspeed and Player.movement[0] \
                < 0 and Player.trigger == 2:
                Player.movement[0] += math.fabs(Player.movement[0] / 20)
                if Player.movement[0] > 0:
                    Player.movement[0] = 0
            elif Player.movement[0] <= maxspeed and Player.movement[0] \
                > 0 and Player.trigger == 1:
                Player.movement[0] -= math.fabs(Player.movement[0] / 20)
                if Player.movement[0] < 0:
                    Player.movement[0] = 0          
        if Player.rect.top >= 0 and Player.rect.top <= height-100:
            if Player.trigger == 3:
                Player.movement[1] = Player.movement[1] + Player.speed
                if Player.movement[1] < -maxspeed:
                    Player.movement[1] = -maxspeed
                elif Player.movement[1] > maxspeed:
                    Player.movement[1] = maxspeed
            elif Player.movement[1] >= -maxspeed and Player.movement[1] \
                < 0 and Player.trigger == 3:
                Player.movement[1] += math.fabs(Player.movement[1] / 20)
                if Player.movement[1] > 0:
                    Player.movement[1] = 0
            elif Player.movement[1] <= maxspeed and Player.movement[1] \
                > 0 and Player.trigger == 3:
                Player.movement[1] -= math.fabs(Player.movement[1] / 20)
                if Player.movement[1] < 0:
                    Player.movement[1] = 0
    else:
        Player.autopilot()

#게임 시나리오 한 웨이브 당 적 등장 횟수
def storyboard(wavecounter):
    if wavecounter >= 0 and wavecounter <= 100:  # enemy
        return 0
    elif wavecounter > 100 and wavecounter <= 200:
                                                     # saucer
        return 1
    elif wavecounter > 200 and wavecounter <= 300:

                                                     # drone

        return 2
    elif wavecounter > 300 and wavecounter <= 400:

                                                     # station

        return 3
    elif wavecounter > 400 and wavecounter <= 500:

                                                     # drone

        return 4
    elif wavecounter > 500 and wavecounter <= 600:

                                                     # enemy and saucer

        return 5
    elif wavecounter > 600 and wavecounter <= 700:

                                                     # enemy

        return 6
    elif wavecounter > 700 and wavecounter <= 800:

                                                     # drone and saucer

        return 7
    elif wavecounter > 800 and wavecounter <= 900:

                                                     # saucer

        return 8
    elif wavecounter > 900 and wavecounter <= 1000:

                                                     # enemy and drones

        return 9
    elif wavecounter > 1000 and wavecounter <= 5000:

                                                     # station

        return 10
    elif wavecounter > 5000:

                             # boss

        return 11

#배경 별모양 셋팅
class stars:

    def __init__(self,radius,color,nofstars,speed=5):
        self.radius = radius
        self.color = color
        self.speed = speed
        self.nofstars = nofstars
        self.starpos = [[0 for j in range(2)] for i in range(self.nofstars)]
        for x in range(self.nofstars):
            self.starpos[x][0] = random.randrange(0, width)
            self.starpos[x][1] = random.randrange(0, height)

    def drawstars(self):
        for x in range(self.nofstars):
            #pygame.draw.rect(screen, color, [self.starpos[x][0],
            #                 self.starpos[x][1], 2, 2])
            pygame.draw.circle(screen,self.color,(self.starpos[x][0],self.starpos[x][1]),self.radius)
        self.movestars()

    def movestars(self):
        for x in range(self.nofstars):
            self.starpos[x][1] += self.speed
            if self.starpos[x][1] > height:
                self.starpos[x][1] = 0


#플레이어 클래스
class player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        (self.image, self.rect) = load_image('fighter1_scale.png', 72,
                72, -1)
        self.rect.top = size[1] - 100#500
        self.rect.left = size[0]/2#200

        self.speed = 0 #이동 속도
        self.fire = 0 #발싸
        self.movement = [0, 0] # 물체 좌표값
        self.trigger = 0 # 이벤트 처리 값
        self.health = 200 #체력
        self.power = 0
        self.kills = 0 #킬
        self.score = 0 # 점수
        self.shootdelay = 0 #발사 지연 시간
        self.isautopilot = False #자동 이동 여부
        self.shot = False 
        self.won = False

    def checkbounds(self):
        if self.isautopilot != True:
            if self.rect.left < 0:
                self.rect.left = 0
                self.movement[0] = 0
                self.speed = 0
            if self.rect.right > width:
                self.rect.right = width
                self.movement[0] = 0
                self.speed = 0
            if self.rect.top < 0:
                self.rect.top = 0
                self.movement[1] = 0
                self.speed = 0
            if self.rect.top > height - 100:
                self.rect.top = height - 100
                self.movement[1] = 0
                self.speed = 0    

    def update(self):
        self.rect = self.rect.move(self.movement)
        self.shootdelay += 1
        if self.fire == 1 and self.shootdelay%3 == 1:
            self.shoot()
        if self.health > 200:
            self.health = 200
    def drawplayer(self):
        screen.blit(self.image, self.rect)
#self.shot 갯수 = 발사 위치의 갯수
    def shoot(self):
        (x, y) = self.rect.center
        if self.power == 0:
            self.shot = bullet(x - 14, y, (0, 255, 0), 1)  # 총알 발싸 위치
            self.shot = bullet(x + 14, y, (0, 255, 0), 1)
        elif self.power == 1:
              # 총알 발싸 위치
            self.shot = bullet(x - 14, y, (0, 255, 0), 1)  # 총알 발싸 위치
            self.shot = bullet(x + 14, y, (0, 255, 0), 1)  
            self.shot = bullet(x + 28, y, (0, 255, 0), 1)  
            self.shot = bullet(x - 28 , y, (0, 255, 0), 1)
        elif self.power == 2:
            self.shot = bullet(x - 14, y, (0, 255, 0), 1)  # 총알 발싸 위치
            self.shot = bullet(x + 14, y, (0, 255, 0), 1)  
            self.shot = bullet(x + 28, y, (0, 255, 0), 1)  
            self.shot = bullet(x - 28 , y, (0, 255, 0), 1)
            self.shot = bullet(x + 56, y, (0, 255, 0), 1)
            self.shot = bullet(x - 56, y, (0, 255, 0), 1)
        elif self.power == 3:
            self.shot = bullet(x - 14, y, (0, 255, 0), 1)  # 총알 발싸 위치
            self.shot = bullet(x + 14, y, (0, 255, 0), 1)  
            self.shot = bullet(x + 28, y, (0, 255, 0), 1)  
            self.shot = bullet(x - 28 , y, (0, 255, 0), 1)
            self.shot = bullet(x + 56, y, (0, 255, 0), 1)
            self.shot = bullet(x - 56, y, (0, 255, 0), 1)
            self.shot = bullet(x + 112, y, (0, 255, 0), 1)
            self.shot = bullet(x - 112, y, (0, 255, 0), 1)
        elif self.power < 5:
            self.shot = bullet(x - 14, y, (0, 255, 0), 1)  # 총알 발싸 위치
            self.shot = bullet(x + 14, y, (0, 255, 0), 1)  
            self.shot = bullet(x + 28, y, (0, 255, 0), 1)  
            self.shot = bullet(x - 28 , y, (0, 255, 0), 1)
            self.shot = bullet(x + 56, y, (0, 255, 0), 1)
            self.shot = bullet(x - 56, y, (0, 255, 0), 1)
            self.shot = bullet(x + 112, y, (0, 255, 0), 1)
            self.shot = bullet(x - 112, y, (0, 255, 0), 1)
            self.shot = bullet(x + 140, y, (0, 255, 0), 1)
            self.shot = bullet(x - 140, y, (0, 255, 0), 1)
            
#player, enemy ..etc 의 autopilot 값이 True면 자동 이동
    def autopilot(self):
        if self.rect.centerx < width / 2:
            self.movement[0] = 5
        else:
            self.movement[0] = -5
        if self.rect.centerx - width / 2 < 5 and self.rect.centerx \
            - width / 2 > -5:
            self.movement[0] = 0
            self.movement[1] = -10

#보스 클래스
class boss(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        (self.image, self.rect) = load_image('boss.png', 200, 400, -1)#125, 250, -1)
        self.rect = self.image.get_rect()
        self.rect.top = 100
        self.rect.left = random.randrange(0, width - 72)

        self.speed = 0
        self.fire = 0
        self.movement = [0, 0]
        self.trigger = 0
        self.health = 600
        self.bulletformation = 0
        self.bulletspeed = 20
        self.spreecount = 0
        self.spree = False
        self.shot = False
        self.isautopilot = False
        self.reloadtime = 0

    def checkbounds(self):
        if self.rect.left < 0:
            self.rect.left = 0
            self.movement[0] = 0
            self.speed = 0
        if self.rect.right > width:
            self.rect.right = width
            self.movement[0] = 0
            self.speed = 0

    def update(self):
        self.checkbounds()
        moveplayer(self)

        self.rect = self.rect.move(self.movement)

        if self.fire == 1 and self.reloadtime == 0:
            self.shoot(self.bulletformation, self.bulletspeed)

        if self.reloadtime > 0:
            self.reloadtime -= 1

        if self.health <= 0:
            self.kill()

        if self.spree == True and self.spreecount <= 70:
            self.spreecount += 1
            if self.spreecount % 5 == 1:
                self.movement[0] = 0
                self.speed = 0
                self.shoot(1, 10)
            else:
                pass
        else:
            self.spree = False
            self.spreecount = 0

    def drawplayer(self):
        screen.blit(self.image, self.rect)

    def shoot(self, bulletformation=0, bulletspeed=20):
        (x, y) = self.rect.center
        if bulletformation == 0:
            self.shot = enemybullet(x, y + self.rect.height / 2, (255,
                                    0, 255), [0, 1], bulletspeed)
            self.shot = enemybullet(x - self.rect.width / 2 + 30, y
                                    - self.rect.height / 2 + 50, (255,
                                    0, 255), [0, 1], bulletspeed)
            self.shot = enemybullet(x + self.rect.width / 2 - 30, y
                                    - self.rect.height / 2 + 50, (255,
                                    0, 255), [0, 1], bulletspeed)
        elif bulletformation == 1:
            self.shot = enemybullet(x, y, (255, 0, 255), [1.5, 1],
                                    bulletspeed)
            self.shot = enemybullet(x, y, (255, 0, 255), [-1.5, 1],
                                    bulletspeed)
            self.shot = enemybullet(x, y, (255, 0, 255), [1.2, 1],
                                    bulletspeed)
            self.shot = enemybullet(x, y, (255, 0, 255), [-1.2, 1],
                                    bulletspeed)
            self.shot = enemybullet(x, y, (255, 0, 255), [0, 1],
                                    bulletspeed)
            self.shot = enemybullet(x, y, (255, 0, 255), [0.9, 1],
                                    bulletspeed)
            self.shot = enemybullet(x, y, (255, 0, 255), [-0.9, 1],
                                    bulletspeed)
            self.shot = enemybullet(x, y, (255, 0, 255), [0.6, 1],
                                    bulletspeed)
            self.shot = enemybullet(x, y, (255, 0, 255), [-0.6, 1],
                                    bulletspeed)
            self.shot = enemybullet(x, y, (255, 0, 255), [0.3, 1],
                                    bulletspeed)
            self.shot = enemybullet(x, y, (255, 0, 255), [-0.3, 1],
                                    bulletspeed)

        if random.randrange(0, 10) == 4:
            enemy(random.randrange(0, 4))
        if random.randrange(0, 50) == 41:
            enemysaucer(random.randrange(0, width - 50))
        if random.randrange(0, 200) == 121:
            enemydrone(random.randrange(0, width - 50))

#적 클래스
class enemy(pygame.sprite.Sprite):

    def __init__(self, n=0):
        pygame.sprite.Sprite.__init__(self, self.containers)
        sheet = pygame.image.load('Sprites/enemy_sheet1.png')
        self.images = []

        rect = pygame.Rect((0, 0, 85, 92))
        image = pygame.Surface(rect.size)
        image.blit(sheet, (0, 0), rect)
        self.images.append(image)

        rect = pygame.Rect((86, 0, 71, 92))
        image = pygame.Surface(rect.size)
        image.blit(sheet, (0, 0), rect)
        self.images.append(image)

        rect = pygame.Rect((158, 0, 68, 92))
        image = pygame.Surface(rect.size)
        image.blit(sheet, (0, 0), rect)
        self.images.append(image)

        rect = pygame.Rect((227, 0, 65, 92))
        image = pygame.Surface(rect.size)
        image.blit(sheet, (0, 0), rect)
        self.images.append(image)

        self.image = self.images[n]
        self.image = self.image.convert()
        colorkey = -1
        colorkey = self.image.get_at((10, 10))
        self.image.set_colorkey(colorkey, RLEACCEL)

        self.image = pygame.transform.scale(self.image, (36, 36))
        self.rect = self.image.get_rect()

        self.image = pygame.transform.rotate(self.image, 180)
        self.rect.top = 0
        self.rect.left = random.randrange(0, width - 72)

        self.speed = 0
        self.fire = 0
        self.movement = [0, 0]
        self.trigger = 0
        self.health = 2
        self.isautopilot = False

        self.explosion_sound = \
            pygame.mixer.Sound('Sprites/explosion.wav')
        self.explosion_sound.set_volume(0.1)
        self.hit_sound = \
            pygame.mixer.Sound('Sprites/hitSound.wav')
        self.hit_sound.set_volume(0.1)

        self.shot = False

    def checkbounds(self):
        if self.rect.left < 0:
            self.rect.left = 0
            self.movement[0] = 0
            self.speed = 0
        if self.rect.right > width:
            self.rect.right = width
            self.movement[0] = 0
            self.speed = 0

    def update(self):
        self.checkbounds()

        moveplayer(self)
        self.autopilot()
        self.rect = self.rect.move(self.movement)

        if self.fire == 1:
            self.shoot()

        if self.health <= 0:
            (x, y) = self.rect.center
            if pygame.mixer.get_init():
                self.explosion_sound.play(maxtime=1000)
            explosion(x, y)
            self.kill()

    def drawplayer(self):
        screen.blit(self.image, self.rect)

    def shoot(self):
        (x, y) = self.rect.center
        self.shot = enemybullet(x, y, (255, 255, 0), [0, 1], 12)

    def autopilot(self):
        if self.rect.top < height:
            self.movement[1] = 5
        else:
            self.kill()
class enemymeteor(pygame.sprite.Sprite):
    def __init__(self, n=0):
        pygame.sprite.Sprite.__init__(self, self.containers)
        sheet = pygame.image.load('Sprites/enemy_meteor.png')
        self.images = []

        rect = pygame.Rect((0, 0, 85, 105))
        image = pygame.Surface(rect.size)
        image.blit(sheet, (0, 0), rect)
        self.images.append(image)

        rect = pygame.Rect((85, 0, 71, 105))
        image = pygame.Surface(rect.size)
        image.blit(sheet, (0, 0), rect)
        self.images.append(image)

        rect = pygame.Rect((170, 0, 68, 105))
        image = pygame.Surface(rect.size)
        image.blit(sheet, (0, 0), rect)
        self.images.append(image)

        rect = pygame.Rect((255, 0, 65, 105))
        image = pygame.Surface(rect.size)
        image.blit(sheet, (0, 0), rect)
        self.images.append(image)

        self.image = self.images[n]
        self.image = self.image.convert()
        colorkey = -1
        colorkey = self.image.get_at((10, 10))
        self.image.set_colorkey(colorkey, RLEACCEL)

        self.image = pygame.transform.scale(self.image, (36, 36))
        self.rect = self.image.get_rect()

        self.image = pygame.transform.rotate(self.image, 180)
        self.rect.top = 0
        self.rect.left = random.randrange(0, width - 72)

        self.speed = 0
        self.fire = 0
        self.movement = [0, 0]
        self.trigger = 0
        self.health = 25
        self.isautopilot = False

        self.explosion_sound = \
            pygame.mixer.Sound('Sprites/explosion.wav')
        self.explosion_sound.set_volume(0.1)

        self.shot = False

    def checkbounds(self):
        if self.rect.left < 0:
            self.rect.left = 0
            self.movement[0] = 0
            self.speed = 0
        if self.rect.right > width:
            self.rect.right = width
            self.movement[0] = 0
            self.speed = 0

    def update(self):
        self.checkbounds()

        moveplayer(self)
        self.autopilot()
        self.rect = self.rect.move(self.movement)

        if self.fire == 1:
            self.shoot()

        if self.health <= 0:
            (x, y) = self.rect.center
            if pygame.mixer.get_init():
                self.explosion_sound.play(maxtime=1000)
            explosion(x, y)
            self.kill()

    def drawplayer(self):
        screen.blit(self.image, self.rect)

    def shoot(self):
        (x, y) = self.rect.center
        self.shot = enemybullet(x, y, (255, 255, 0), [0, 1], 12)

    def autopilot(self):
        if self.rect.top < height:
            self.movement[1] = 5
        else:
            self.kill()
class starship(pygame.sprite.Sprite):

    def __init__(self, n=0):
        pygame.sprite.Sprite.__init__(self, self.containers)
        sheet = pygame.image.load('Sprites/starship_scale.png')
        self.images = []

        rect = pygame.Rect((0, 0, 260, 174))
        image = pygame.Surface(rect.size)
        image.blit(sheet, (0, 0), rect)
        self.images.append(image)

        rect = pygame.Rect((0, 0, 260, 174))
        image = pygame.Surface(rect.size)
        image.blit(sheet, (0, 0), rect)
        self.images.append(image)

        
        rect = pygame.Rect((0, 0, 260, 174))
        image = pygame.Surface(rect.size)
        image.blit(sheet, (0, 0), rect)
        self.images.append(image)

        
        rect = pygame.Rect((0, 0, 260, 174))
        image = pygame.Surface(rect.size)
        image.blit(sheet, (0, 0), rect)
        self.images.append(image)



        self.image = self.images[n]
        self.image = self.image.convert()
        colorkey = -1
        colorkey = self.image.get_at((10, 10))
        self.image.set_colorkey(colorkey, RLEACCEL)

        self.image = pygame.transform.scale(self.image, (36, 36))
        self.rect = self.image.get_rect()

        self.image = pygame.transform.rotate(self.image, 180)
        self.rect.top = 0
        self.rect.left = random.randrange(0, width - 1)

        self.speed = 0
        self.fire = 0
        self.movement = [0, 0]
        self.trigger = 0
        self.health = 2
        self.isautopilot = False

        self.explosion_sound = \
            pygame.mixer.Sound('Sprites/explosion.wav')
        self.explosion_sound.set_volume(0.1)
        self.hit_sound = \
            pygame.mixer.Sound('Sprites/hitSound.wav')
        self.hit_sound.set_volume(0.1)

        self.shot = False

    def checkbounds(self):
        if self.rect.left < 0:
            self.rect.left = 0
            self.movement[0] = 0
            self.speed = 0
        if self.rect.right > width:
            self.rect.right = width
            self.movement[0] = 0
            self.speed = 0

    def update(self):
        self.checkbounds()

        moveplayer(self)
        self.autopilot()
        self.rect = self.rect.move(self.movement)

        if self.fire == 1:
            self.shoot()

        if self.health <= 0:
            (x, y) = self.rect.center
            if pygame.mixer.get_init():
                self.explosion_sound.play(maxtime=1000)
            explosion(x, y)
            self.kill()

    def drawplayer(self):
        screen.blit(self.image, self.rect)

    def shoot(self):
        (x, y) = self.rect.center
        self.shot = enemybullet(x, y, (255, 255, 0), [0, 1], 12)

    def autopilot(self):
        if self.rect.top < height:
            self.movement[1] = 5
        else:
            self.kill()



class enemydrone(pygame.sprite.Sprite):#749 x 354

    def __init__(self, x):
        pygame.sprite.Sprite.__init__(self, self.containers)
        (self.image, self.rect) = load_image('enemydrone.png',150, 150, -1)
        self.rect.top = -self.rect.height
        self.rect.left = x

        self.speed = 0
        self.fire = 1
        self.movement = [0, 0]
        self.health = 20

        self.shot = True
        self.waitTime = 0
        self.explosion_sound = \
            pygame.mixer.Sound('Sprites/explosion.wav')
        self.explosion_sound.set_volume(0.1)
        self.hit_sound = \
            pygame.mixer.Sound('Sprites/hitSound.wav')
        self.hit_sound.set_volume(0.1)

    def checkbounds(self):
        if self.rect.left < 0:
            self.rect.left = 0
            self.movement[0] = 0
            self.speed = 0
        if self.rect.right > width:
            self.rect.right = width
            self.movement[0] = 0
            self.speed = 0

    def update(self):
        self.checkbounds()
        self.autopilot()
        self.rect = self.rect.move(self.movement)

        if self.fire == 1 and self.waitTime % 10 == 1:
            self.shoot()

        if self.health <= 0:
            (x, y) = self.rect.center
            if pygame.mixer.get_init():
                self.explosion_sound.play(maxtime=1000)
            explosion(x, y,100)
            self.kill()

    def drawplayer(self):
        screen.blit(self.image, self.rect)

    def shoot(self):
        (x, y) = self.rect.center
        self.shot = enemybullet(x, y + self.rect.height / 2, (255, 0,
                                0), [0, 1], 10)
        self.shot = enemybullet(x, y + self.rect.height / 2, (255, 0,
                                0), [-0.5, 1], 10)
        self.shot = enemybullet(x, y + self.rect.height / 2, (255, 0,
                                0), [0.5, 1], 10)
        self.shot = enemybullet(x, y + self.rect.height / 2, (255, 0,
                                0), [-1, 1], 10)
        self.shot = enemybullet(x, y + self.rect.height / 2, (255, 0,
                                0), [1, 1], 10)

    def autopilot(self):
        if self.rect.top < height - 1:
            self.movement[1] = 3
        elif self.rect.top > height - 500 and self.waitTime < 1000:
            self.movement[1] = 0
            self.waitTime += 1

        if self.waitTime >= 150:
            self.movement[1] = 5

        if self.rect.top > height:
            self.kill()

#원형 비행기
class enemysaucer(pygame.sprite.Sprite):

    def __init__(self, x):
        pygame.sprite.Sprite.__init__(self, self.containers)
        sheet = pygame.image.load('Sprites/enemy_saucer1.png')
        self.images = []

        for i in range(0, 672, 96):
            rect = pygame.Rect((i, 0, 96, 96))
            image = pygame.Surface(rect.size)
            image = image.convert()
            colorkey = -1
            colorkey = image.get_at((10, 10))
            image.set_colorkey(colorkey, RLEACCEL)
            image.blit(sheet, (0, 0), rect)
            image = pygame.transform.scale(image, (48, 48))
            self.images.append(image)

        self.image = self.images[0]
        self.index = 0
        self.rect = self.image.get_rect()
        self.rect.center = (x, -self.rect.height)
        self.health = 10
        self.waitTime = 0
        self.fire = 1
        self.movement = [0, 0]
        self.haltpos = random.randrange(300, 510)
        self.shot = False
        self.explosion_sound = \
            pygame.mixer.Sound('Sprites/explosion.wav')
        self.explosion_sound.set_volume(0.1)
        self.hit_sound = \
            pygame.mixer.Sound('Sprites/hitSound.wav')
        self.hit_sound.set_volume(0.1)

    def checkbounds(self):
        if self.rect.left < 0:
            self.rect.left = 0
            self.movement[0] = 0
            self.speed = 0
        if self.rect.right > width:
            self.rect.right = width
            self.movement[0] = 0
            self.speed = 0

    def update(self):
        self.checkbounds()
        self.autopilot()
        self.rect = self.rect.move(self.movement)

        if self.fire == 1 and self.waitTime % 10 == 1:
            self.shoot()

        if self.health <= 0:
            (x, y) = self.rect.center
            if pygame.mixer.get_init():
                self.explosion_sound.play(maxtime=1000)
            explosion(x, y,75)
            self.kill()
        self.index += 1
        self.index = self.index % 7
        self.image = self.images[self.index]
        self.image = pygame.transform.rotate(self.image, 90)
        self.images[self.index] = self.image

    def drawplayer(self):
        screen.blit(self.image, self.rect)

    def shoot(self):
        (x, y) = self.rect.center
        self.shot = enemybullet(x, y, (0, 0, 255), [0, 1], 18)

    def autopilot(self):
        if self.rect.top < height - self.haltpos:
            self.movement[1] = 3
        elif self.rect.top > height - self.haltpos and self.waitTime \
            < 1000:
            self.movement[1] = 0
            self.waitTime += 1

        if self.waitTime >= 150:
            self.movement[1] = 5

        if self.rect.top > height:
            self.kill()


#######--------------------#################
#회전형 비행기
class enemystation(pygame.sprite.Sprite):

    def __init__(self, x):
        pygame.sprite.Sprite.__init__(self, self.containers)
        (self.image, self.rect) = load_image('spacestation_scale.png',
                150, 150, -1)

        self.rect.center = (x, -self.rect.height)
        self.health = 60
        self.waitTime = 0
        self.fire = 1
        self.movement = [0, 0]
        self.shot = False
        self.explosion_sound = \
            pygame.mixer.Sound('Sprites/explosion.wav')
        self.explosion_sound.set_volume(0.1)
        self.hit_sound = \
            pygame.mixer.Sound('Sprites/hitSound.wav')
        self.hit_sound.set_volume(0.1)
        self.rotation = 10

    def checkbounds(self):
        if self.rect.left < 0:
            self.rect.left = 0
            self.movement[0] = 0
            self.speed = 0
        if self.rect.right > width:
            self.rect.right = width
            self.movement[0] = 0
            self.speed = 0

    def update(self):
        self.checkbounds()
        self.autopilot()
        self.rect = self.rect.move(self.movement)

        if self.fire == 1 and self.waitTime % 10 == 1:
            self.shoot()

        if self.health <= 0:
            (x, y) = self.rect.center
            if pygame.mixer.get_init():
                self.explosion_sound.play(maxtime=1000)
            explosion(x, y,150)
            self.kill()

        if self.waitTime > 0:
            self.image = pygame.transform.rotate(self.image, 90)

    def drawplayer(self):
        screen.blit(self.image, self.rect)

    def shoot(self):
        (x, y) = self.rect.center
        for j in range(-12, 12):
            self.shot = enemybullet(x, y, (0, 255, 0), [j / 3.0, 1], 10)
        if self.waitTime % 2 == 1:
            enemy(random.randrange(0, 4))

        if self.waitTime % 12 == 1:
            enemysaucer(random.randrange(0, width - 50))

    def autopilot(self):
        if self.rect.top < height - 500:
            self.movement[1] = 3
        elif self.rect.top > height - 500 and self.waitTime < 1000:
            self.movement[1] = 0
            self.waitTime += 1

        if self.waitTime >= 150:
            self.movement[1] = 5

        if self.rect.top > height:
            self.kill()

#힐링팩 아이템
class healthpack(pygame.sprite.Sprite):

    def __init__(self,x,y,health,):

        pygame.sprite.Sprite.__init__(self, self.containers)
        self.health = health
        (self.image, self.rect) = load_image('healthpack.png', 40, 40, -1)
        self.rect.left = x
        self.rect.top = y
        self.movement = [3, 0]
        self.maxleft = self.rect.left - 20
        self.maxright = self.rect.right + 20

    def checkbounds(self):
        if self.rect.left < 0:
            self.rect.left = 0
            self.movement[0] = 0
            self.speed = 0
        if self.rect.right > width:
            self.rect.right = width
            self.movement[0] = 0
            self.speed = 0

    def update(self):
        self.checkbounds()
        self.autopilot()
        self.rect = self.rect.move(self.movement)

        if self.health <= 0 or self.rect.top > height:
            self.kill()

    def drawplayer(self):
        screen.blit(self.image, self.rect)

    def autopilot(self):
        if self.rect.right > self.maxright:
            self.movement[0] = -3
        elif self.rect.left < self.maxleft:
            self.movement[0] = 3

        self.movement[1] = 5
        
class powerpack(pygame.sprite.Sprite):
    def __init__(self,x,y,health,):

        pygame.sprite.Sprite.__init__(self, self.containers)
        (self.image, self.rect) = load_image('speed.png', 40, 40, -1)
        self.health = health
        self.rect.left = x
        self.rect.top = y
        self.power = 1
        self.movement = [3, 0]
        self.maxleft = self.rect.left - 20
        self.maxright = self.rect.right + 20

    def checkbounds(self):
        if self.rect.left < 0:
            self.rect.left = 0
            self.movement[0] = 0
            self.speed = 0
        if self.rect.right > width:
            self.rect.right = width
            self.movement[0] = 0
            self.speed = 0

    def update(self):
        self.checkbounds()
        self.autopilot()
        self.rect = self.rect.move(self.movement)
        if self.health <= 0 or self.rect.top > height:
            self.kill()

    def drawplayer(self):
        screen.blit(self.image, self.rect)

    def autopilot(self):
        if self.rect.right > self.maxright:
            self.movement[0] = -3
        elif self.rect.left < self.maxleft:
            self.movement[0] = 3

        self.movement[1] = 5
#총알
class bullet(pygame.sprite.Sprite):

    def __init__(
        self,
        x,
        y,
        color,
        direction=1,
        ):

        pygame.sprite.Sprite.__init__(self, self.containers)
        """self.image = pygame.Surface((2, 18), pygame.SRCALPHA, 32)

        self.image = self.image.convert_alpha()
        pygame.draw.rect(self.image, color, (0, 0, 2, 18))  # (12,225,15)
        self.rect = self.image.get_rect()
        """
        self.image,self.rect = load_image('lazer.png',5,25,-1)
        self.rect.center = (x, y - direction * 20)
        self.direction = direction

    def update(self):
        (x, y) = self.rect.center
        y -= self.direction * 20
        self.rect.center = (x, y)
        if y <= 0 or y >= height:
            self.kill()
#적 총알
class enemybullet(pygame.sprite.Sprite):

    def __init__(
        self,
        x,
        y,
        color,
        direction,
        speed,
        ):

        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = pygame.Surface((10, 10), pygame.SRCALPHA, 32)
        self.image = self.image.convert_alpha()
        self.col = list(color)
        for i in range(5, 0, -1):
            self.col[0] = color[0] * float(i) / 5
            self.col[1] = color[1] * float(i) / 5
            self.col[2] = color[2] * float(i) / 5
            pygame.draw.circle(self.image, tuple(self.col), (5, 5), i,
                               0)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)  # + direction[1]*20)
        self.direction = direction
        self.speed = speed

    def update(self):
        (x, y) = self.rect.center
        y += self.direction[1] * self.speed
        x += self.direction[0] * self.speed
        self.rect.center = (x, y)
        if y <= 0 or y >= height or x <= 0 or x >= width:
            self.kill()

#폭파  이벤트 처리
class explosion(pygame.sprite.Sprite):

    def __init__(self, x, y,radius=-1):
        pygame.sprite.Sprite.__init__(self, self.containers)
        sheet = pygame.image.load('Sprites/enemy_explode.png')
        self.images = []
        for i in range(0, 768, 48):
            rect = pygame.Rect((i, 0, 48, 48))
            image = pygame.Surface(rect.size)
            image = image.convert()
            colorkey = -1
            colorkey = image.get_at((10, 10))
            image.set_colorkey(colorkey, RLEACCEL)

            image.blit(sheet, (0, 0), rect)
            if radius != -1:
                image = pygame.transform.scale(image,(radius,radius))
            self.images.append(image)

        self.image = self.images[0]
        self.index = 0
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.image = self.images[self.index]
        self.index += 1
        if self.index >= len(self.images):
            self.kill()

##메인
def main():
    gameOver = False
    menuExit = False
    stageStart = False
    bossStage = False
    gameOverScreen = False

    menuselect = -1
    menuhighlight = 0

    wavecounter = 0
    wave = 0
## 맵
    starfield1 = stars(1,white,50,5)
    starfield2 = stars(1,(150,150,150),75,3)
    starfield3 = stars(1,(75,75,75),200,1)
##Sprite
    bullets = pygame.sprite.Group()
    meteors = pygame.sprite.Group()
    enemybullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    explosions = pygame.sprite.Group()
    shields = pygame.sprite.Group()
    drones = pygame.sprite.Group()
    saucers = pygame.sprite.Group()
    station = pygame.sprite.Group()
    healthpacks = pygame.sprite.Group()
    powerpacks = pygame.sprite.Group()
    starships = pygame.sprite.Group()
##유닛
    enemymeteor.containers=meteors
    bullet.containers = bullets
    enemybullet.containers = enemybullets
    enemy.containers = enemies
    explosion.containers = explosions
    enemydrone.containers = drones
    enemysaucer.containers = saucers
    enemystation.containers = station
    starship.containers=starships
    healthpack.containers = healthpacks
    powerpack.containers = powerpacks
##사용자 셋팅 및 sprites파일 매핑
    user = player()
    pygame.display.set_caption('PyGalaxian')
    bg_music = pygame.mixer.Sound('Sprites/bg_music.ogg')
    boss_music = pygame.mixer.Sound('Sprites/boss_music.ogg')

    (logoimage, logorect) = load_image('gamelogo.png', -1, -1, -1)
    logorect.left = width / 2 - logorect.width / 2
    logorect.top = height / 2 - logorect.height * 5 / 4
    
#시작
    while not gameOver:
        while not menuExit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    menuExit = True
                    gameOver = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN or event.key \
                        == pygame.K_UP:
                        menuhighlight += 1
                    elif event.key == pygame.K_RETURN:
                        menuselect = menuhighlight % 2

            if menuselect == 0:
                stageStart = True
                menuExit = True
                bg_music.play(-1)
            elif menuselect == 1:
                pygame.quit()
                quit()
            else:
                pass
            
            #화면 지우기 (0,0,0)
            screen.fill(sky)
            starfield1.drawstars() #별 그려주는 작업
            starfield2.drawstars()
            starfield3.drawstars()
            user.drawplayer()
            screen.blit(logoimage, logorect)
            
            #우측 하단 텍스트 표시
            displaytext('Play', 32, width / 2 - 20, height * 3 / 4
                        - 40, white)
            displaytext('Exit', 32, width / 2 - 20, height * 3 / 4,
                        white)
            displaytext('PyGalaxian version 1.0', 12, width - 80, height - 20,
                        white)
            displaytext('Made by: Shivam Shekhar', 12, width - 80, height - 10,
                        white)
            
            #MenuSelect Icon move
            if menuhighlight % 2 == 0:
                screen.blit(pygame.transform.scale(user.image, (25,
                            25)), [width / 2 - 100, height * 3 / 4
                            - 55, 15, 15])
            elif menuhighlight % 2 == 1:
                screen.blit(pygame.transform.scale(user.image, (25,
                            25)), [width / 2 - 100, height * 3 / 4
                            - 15, 15, 15])
            pygame.display.update()
            clock.tick(FPS)
            
#게임 시작
        while stageStart:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    stageStart = False
                    gameOver = True
                if event.type == pygame.KEYDOWN: #플레이어 이벤트 처리 버튼이 눌렸을시 이벤트 처리
                    user.trigger = 1
                    if event.key == pygame.K_LEFT:
                        user.speed = -10
                    if event.key == pygame.K_RIGHT:
                        user.speed = 10
                    if event.key == pygame.K_UP:
                        user.trigger = 3
                        user.speed = -10
                    if event.key == pygame.K_DOWN:
                        user.trigger = 3
                        user.speed = 10
                    if event.key == pygame.K_w:
                        user.fire = 1    
                    if event.key == pygame.K_ESCAPE:
                    	pygame.quit()
                    	quit()
                if event.type == pygame.KEYUP: #플레이어 이벤트 처리 Up
                    if event.key == pygame.K_LEFT or \
                       event.key == pygame.K_RIGHT or \
                       event.key == pygame.K_UP or \
                       event.key == pygame.K_DOWN:
                        user.speed = 0
                        user.trigger = 2
                    if event.key == pygame.K_w:
                        user.fire = 0
                        
                        
            #웨이브 처리 이벤트
            if wavecounter % 500 < 1000 and random.randrange(0, 2) == 1 \
                and len(healthpacks) < 1:
                healthpack(random.randrange(0, width - 50), 0, 10)
                
            if wavecounter % 500 < 1000 and random.randrange(0, 2) == 1 \
                and len(powerpacks) < 1:
                powerpack(random.randrange(0, width - 50), 0, 10)    

            if random.randrange(0, 8) == 1 and len(enemies) < 10 \
                and (wave == 0 or wave == 5 or wave == 6 or wave == 9):
                enemy(random.randrange(0, 4))
            if random.randrange(0, 8) == 1 and len(meteors) < 10 \
                and (wave == 0 or wave == 5 or wave == 6 or wave == 9):
                enemymeteor(random.randrange(0, 4))
                
            if random.randrange(0, 10) == 1 and len(starships) < 10 \
                and (wave == 1 or wave == 2 or wave == 4 or wave == 6 or wave == 8 or wave == 9):
                starship(random.randrange(0, 4))
                
            if random.randrange(0, 20) == 1 and len(saucers) < 3 \
                and (wave == 1 or wave == 5 or wave == 7 or wave == 8):
                enemysaucer(random.randrange(0, width - 50))

            if random.randrange(0, 30) == 21 and len(drones) < 2 \
                and (wave == 2 or wave == 4 or wave == 7 or wave == 9):
                if len(drones) > 0:
                    for drone in drones:
                        if drone.rect.left < width / 2:
                            enemydrone(random.randrange(width / 2 + 60,
                                    width - 60))
                        else:
                            enemydrone(random.randrange(0, width / 2
                                    - 60))
                else:
                    enemydrone(random.randrange(0, width - 60))

            if len(station) < 1 and (wave == 3 or wave == 10):
                enemystation(random.randrange(0, width - 60))

            if wave == 11 and len(enemies) == 0 and len(saucers) == 0 \
                and len(station) == 0 and len(drones) == 0:
                user.isautopilot = True
                bg_music.fadeout(6000)
                if user.rect.top <= -1*user.rect.height:
                    wave = 12

            if wave == 12:
                bossStage = True
                stageStart = False
                finalboss = boss()
                user.health += 80
                user.rect.left = width / 2
                user.rect.top = size[1] - 100
                user.isautopilot = False
                user.movement = [0, 0]
                boss_music.play(-1)
            #적기 자동 이동
            for ship in enemies:
                cpumove(ship, user)
            for ship in meteors:
                cpumove(ship, user)
            #적이 탄에 맞았을시 이벤트 처리
            for enemyhit in pygame.sprite.groupcollide(enemies,
                    bullets, 0, 1):
                enemyhit.hit_sound.play(maxtime=1000)
                enemyhit.health -= 1
                if enemyhit.health <= 0:
                    user.kills += 1
                    user.score += 1
            for meteorhit in pygame.sprite.groupcollide(meteors, bullets, 0, 1):
                meteorhit.health -= 1
                if meteorhit.health <= 0:
                    user.kills += 1
                    user.score += 15
            for starshiphit in pygame.sprite.groupcollide(starships,
                    bullets, 0, 1):
                starshiphit.health -= 1
                if starshiphit.health <= 0:
                    user.kills += 1
                    user.score += 1
            for dronehit in pygame.sprite.groupcollide(drones, bullets,
                    0, 1):
                dronehit.hit_sound.play(maxtime=1000)
                dronehit.health -= 1
                if dronehit.health <= 0:
                    user.kills += 1
                    user.score += 10

            for saucerhit in pygame.sprite.groupcollide(saucers,
                    bullets, 0, 1):
                saucerhit.hit_sound.play(maxtime=1000)
                saucerhit.health -= 1
                if saucerhit.health <= 0:
                    user.kills += 1
                    user.score += 5


            for stationhit in pygame.sprite.groupcollide(station,
                    bullets, 0, 1):
                stationhit.hit_sound.play(maxtime=1000)
                stationhit.health -= 1
                if stationhit.health <= 0:
                    user.kills += 1
                    user.score += 25
                    healthpack(stationhit.rect.centerx,
                               stationhit.rect.centery, 20)

            for firedbullet in pygame.sprite.spritecollide(user,
                    enemybullets, 1):
                user.health -= 1

            for enemycollided in enemies:
                if pygame.sprite.collide_mask(user, enemycollided):
                    user.health -= 2
                    enemycollided.health -= enemycollided.health
                    
            for enemycollided in meteors:
                if pygame.sprite.collide_mask(user, enemycollided):
                    user.health -= 2
                    enemycollided.health -= enemycollided.health
                    
            for dronecollided in drones:
                if pygame.sprite.collide_mask(user, dronecollided):
                    user.health -= 10
                    dronecollided.health -= dronecollided.health
                    
            for meteorcollided in meteors:
                if pygame.sprite.collide_mask(user, meteorcollided):
                    user.health -= 2
                    meteorcollided.health -= meteorcollided.health
                
            for saucercollided in saucers:
                if pygame.sprite.collide_mask(user, saucercollided):
                    user.health -= 4
                    saucercollided.health -= saucercollided.health

            for stationcollided in station:
                if pygame.sprite.collide_mask(user, stationcollided):
                    user.health -= 50
                    stationcollided.health -= stationcollided.health
            for starshipcollided in starships:
                if pygame.sprite.collide_mask(user, starshipcollided):
                    user.health -= 4
                    starshipcollided.health -= starshipcollided.health        
            for health_pack in healthpacks:
                if pygame.sprite.collide_mask(user, health_pack):
                    user.health += health_pack.health
                    health_pack.health -= health_pack.health
            for power_pack in powerpacks:
                if pygame.sprite.collide_mask(user, power_pack):
                    if user.power < maxpower:
                        user.power += power_pack.power
                        power_pack.health -= power_pack.health
                    else:
                        power_pack.health -= power_pack.health

            if user.health <= 0:
                gameOverScreen = True
                stageStart = False

            user.update()
            user.checkbounds()

            screen.fill(sky)
            starfield1.drawstars()
            starfield2.drawstars()
            starfield3.drawstars()

            if user.health > 0:
                showhealthbar(user.health, green, [100, height - 20,
                              user.health * 4, 10], 4)
            displaytext('HEALTH', 22, 50, height - 15, white)
            displaytext('Score:', 22, width - 100, 15, white)
            displaytext(str(user.score), 22, width - 35, 15, white)
            user.drawplayer()

            enemies.update()
            bullets.update()
            enemybullets.update()
            explosions.update()
            drones.update()
            saucers.update()
            station.update()
            healthpacks.update()
            powerpacks.update()
            starships.update()
            meteors.update()
            
            bullets.draw(screen)
            enemybullets.draw(screen)
            enemies.draw(screen)
            explosions.draw(screen)
            drones.draw(screen)
            saucers.draw(screen)
            station.draw(screen)
            healthpacks.draw(screen)
            meteors.draw(screen)
            powerpacks.draw(screen)
            starships.draw(screen)

            wave = storyboard(wavecounter)

            wavecounter += 1

            pygame.display.update()

            clock.tick(FPS)

            moveplayer(user)

            """print (
                wavecounter,
                wave,
                user.kills,
                user.health,
                user.rect.left,
                user.movement[0],
                user.rect.right,
                )"""

        while bossStage:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN: #플레이어 이벤트 처리 버튼이 눌렸을시 이벤트 처리
                    user.trigger = 1
                    if event.key == pygame.K_LEFT:
                        user.speed = -10
                    if event.key == pygame.K_RIGHT:
                        user.speed = 10
                    if event.key == pygame.K_UP:
                        user.trigger = 3
                        user.speed = -10
                    if event.key == pygame.K_DOWN:
                        user.trigger = 3
                        user.speed = 10
                    if event.key == pygame.K_w:
                        user.fire = 1    
                    if event.key == pygame.K_ESCAPE:
                    	pygame.quit()
                    	quit()
                if event.type == pygame.KEYUP: #플레이어 이벤트 처리 Up
                    if event.key == pygame.K_LEFT or \
                       event.key == pygame.K_RIGHT or \
                       event.key == pygame.K_UP or \
                       event.key == pygame.K_DOWN:
                        user.speed = 0
                        user.trigger = 2
                    if event.key == pygame.K_w:
                        user.fire = 0

            bossmove(finalboss, user)

            for ship in enemies:
                cpumove(ship, user)
                
            for ship in enemies:
                cpumove(ship, user)
                
            for userbullet in bullets:
                if pygame.sprite.collide_mask(finalboss, userbullet):
                    if finalboss.health > 2:
                        finalboss.health -= 1
                    else:
                        bossStage = False
                        gameOverScreen = True
                        user.score += 200
                        user.won = True
                    userbullet.kill()

            for enemyhit in pygame.sprite.groupcollide(enemies,
                    bullets, 0, 1):
                enemyhit.health -= 1
                if enemyhit.health <= 0:
                    user.kills += 1
                    user.score += 1

            for dronehit in pygame.sprite.groupcollide(drones, bullets,
                    0, 1):
                dronehit.health -= 1
                if dronehit.health <= 0:
                    user.kills += 1
                    user.score += 10

            for saucerhit in pygame.sprite.groupcollide(saucers,
                    bullets, 0, 1):
                saucerhit.health -= 1
                if saucerhit.health <= 0:
                    user.kills += 1
                    user.score += 5

            for firedbullet in pygame.sprite.spritecollide(user,
                    enemybullets, 1):
                user.health -= 1

            for enemycollided in enemies:
                if pygame.sprite.collide_mask(user, enemycollided):
                    user.health -= 2
                    enemycollided.health -= enemycollided.health

            for dronecollided in drones:
                if pygame.sprite.collide_mask(user, dronecollided):
                    user.health -= 10
                    dronecollided.health -= dronecollided.health

            for saucercollided in saucers:
                if pygame.sprite.collide_mask(user, saucercollided):
                    user.health -= 4
                    saucercollided.health -= saucercollided.health

            if user.health <= 0:
                gameOverScreen = True
                bossStage = False

            user.update()
            user.checkbounds()

            screen.fill(sky)
            starfield1.drawstars()
            starfield2.drawstars()
            starfield3.drawstars()

            if user.health > 0:
                showhealthbar(user.health, green, [100, height - 20,
                              user.health * 4, 10], 4)
            displaytext('HEALTH', 22, 50, height - 15, white)

            if finalboss.health > 0:
                showhealthbar(finalboss.health, red, [100, 20,
                              finalboss.health * 0.8, 10], 0.8)
            displaytext('BOSS', 22, 50, 25, white)

            displaytext('Score:', 22, width - 100, 15, white)
            displaytext(str(user.score), 22, width - 35, 15, white)

            user.drawplayer()

            enemies.update()
            bullets.update()
            enemybullets.update()
            drones.update()
            saucers.update()
            explosions.update()
            finalboss.update()

            bullets.draw(screen)
            enemybullets.draw(screen)
            enemies.draw(screen)
            drones.draw(screen)
            saucers.draw(screen)
            explosions.draw(screen)
            finalboss.drawplayer()

            pygame.display.update()
            clock.tick(FPS)
            moveplayer(user)

        while gameOverScreen:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameOverScreen = False
                    gameOver = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    gameOverScreen = False
                    gameOver = True

            screen.fill(sky)
            starfield1.drawstars()
            starfield2.drawstars()
            starfield3.drawstars()

            if user.won == False:
                displaytext('Game Over', 26, width / 2 - 30, height
                            / 2, white)
            else:
                displaytext('Congratulations! You Won!', 26, width / 2
                            - 30, height / 2, white)

            displaytext('Your score: ', 26, width / 2 - 40, height / 2
                        + 40, white)
            displaytext(str(user.score), 26, width / 2 + 50, height / 2
                        + 43, white)
            displaytext('Press Enter to exit...', 14, width / 2 - 30,
                        height / 2 + 90, white)
            pygame.display.update()
            clock.tick(FPS)

    pygame.quit()
    quit()


main()
