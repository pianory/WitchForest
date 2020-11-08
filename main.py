import pygame
import random
import sys
import math

# -*- coding:utf-8 -*-#

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((640, 640))

# 기본 변수
FPS = 30
fpsClock = pygame.time.Clock()
score = 0
asteroidTimer = 100
fast = 3
xMinusLimit = 5
xPlusLimit = 395
yMinusLimit = 5
yPlusLimit = 495
bullets = []
opening = True
running = False
level = 0

# 미디어 변수
bulletImg = None
playerImg = None
gameOverImg = None
x = 200
y = 480

try:
    bulletImg = [pygame.image.load("./img/15_1.png"), pygame.image.load("./img/15_2.png"),
                 pygame.image.load("./img/15_3.png"), pygame.image.load("./img/15_4.png"),
                 pygame.image.load("./img/15_5.png"), pygame.image.load("./img/25_1.png"),
                 pygame.image.load("./img/25_2.png"), pygame.image.load("./img/25_3.png"),
                 pygame.image.load("./img/25_4.png"), pygame.image.load("./img/25_5.png"),
                 ]
    playerImg = pygame.transform.scale(pygame.image.load("./img/player.png"), (37, 64))
    background = [pygame.image.load("./img/backgroundTest.jpg")]
    musics = ["./audio/Armageddon.ogg"]

except Exception as err:
    print('그림 또는 효과음 삽입에 문제가 있습니다.: ', err)
    pygame.quit()
    sys.exit(0)


class Bullet:
    def __init__(self, timing, x, y, image, size, angle, speed, startX, startY):
        self.x, self.y, self.image, self.size, self.angle, self.speed, self.timing = x, y, image, size, angle, speed, timing
        self.startX, self.startY = startX, startY

    def go(self, playerX, playerY, curr):
        self.x = self.startX + math.cos(self.angle * math.pi) * self.speed * (curr - self.timing)
        self.y = self.startY + math.sin(self.angle * math.pi) * self.speed * (curr - self.timing)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.image == other.image and self.size == other.size and self.angle == other.angle and self.speed == other.speed and self.startX == other.startX and self.startY == other.startY


class BulletPlayer:
    def __init__(self, timing, x, y, image, size, playerposX, playerposY, speed, startX, startY):
        self.x, self.y, self.image, self.size, self.playerposX, self.playerposY, self.speed = x, y, image, size, playerposX, playerposY, speed
        self.startX, self.startY, self.timing = startX, startY, timing

    def go(self, playerX, playerY, curr):
        if self.playerposX is None and self.playerposY is None:
            self.playerposX, self.playerposY = playerX, playerY
        self.x = self.startX + (curr - self.timing) * self.speed * (self.playerposX - self.startX) / (
                    ((self.playerposX - self.startX) ** 2 + (self.playerposY - self.startY) ** 2) ** 0.5)
        self.y = self.startY + (curr - self.timing) * self.speed * (self.playerposY - self.startY) / (
                    ((self.playerposX - self.startX) ** 2 + (self.playerposY - self.startY) ** 2) ** 0.5)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.image == other.image and self.size == other.size and self.angle == other.angle and self.speed == other.speed and self.startX == other.startX and self.startY == other.startY and self.timing == other.timing


def Circle(timing, x, y, image, size, angle, speed, shift):
    global FPS
    a = []
    i = 0
    while i < 2:
        a.append(Bullet(timing, x, y, image, size, i + shift, speed*60/FPS, x, y))
        i += angle
    return a


def Opener(timing, x, y, image, size, angle, speed):
    global FPS
    a = []
    speedList = list(map(float, speed.split(";")))
    for i in speedList:
        a.append(Bullet(timing, x, y, image, size, angle, i*60/FPS, x, y))
    return a


f = open("pattern1.ptn", "r") # File Read
cr = 0
timingPoints = []
patterns = []
cur = []
while True:
    line = f.readline()
    if not line: break
    p = list(map(str, line.split()))
    if cr == int(p[0]):
        if p[1] == "C":
            r, s = p[7].split(";")
            cur.extend(Circle(int(p[0]), float(p[2]), float(p[3]), bulletImg[int(p[4])], float(p[5]), float(r), float(p[6]), float(s)))
        elif p[1] == "L":
            cur.append(Bullet(int(p[0]), float(p[2]), float(p[3]), bulletImg[int(p[4])], float(p[5]), float(p[7]), float(p[6])*60/FPS, float(p[2]), float(p[3])))
        elif p[1] == "E":
            cur.append(BulletPlayer(int(p[0]), float(p[2]), float(p[3]), bulletImg[int(p[4])], float(p[5]), None, None, float(p[6])*60/FPS, int(p[2]), int(p[3])))
        elif p[1] == "O":
            cur.extend(Opener(int(p[0]), float(p[2]), float(p[3]), bulletImg[int(p[4])], float(p[5]), float(p[7]), p[6]))
    else:
        if cr != 0:
            patterns.append(cur)
            timingPoints.append(cr)
        cur = []
        cr = int(p[0])
        if p[1] == "C":
            r, s = p[7].split(";")
            cur.extend(Circle(int(p[0]), float(p[2]), float(p[3]), bulletImg[int(p[4])], float(p[5]), float(r), float(p[6]), float(s)))
        elif p[1] == "L":
            cur.append(Bullet(int(p[0]), float(p[2]), float(p[3]), bulletImg[int(p[4])], float(p[5]), float(p[7]), float(p[6])*60/FPS, float(p[2]), float(p[3])))
        elif p[1] == "E":
            cur.append(BulletPlayer(int(p[0]), float(p[2]), float(p[3]), bulletImg[int(p[4])], float(p[5]), None, None, float(p[6])*60/FPS, int(p[2]), int(p[3])))
        elif p[1] == "O":
            cur.extend(Opener(int(p[0]), float(p[2]), float(p[3]), bulletImg[int(p[4])], float(p[5]), float(p[7]), p[6]))
timingPoints.append(cr)
patterns.append(cur)
f.close()


def Text(arg1, x, y):
    font = pygame.font.Font("./fonts/HeirofLightRegular.ttf", 18)
    text = font.render("SCORE  " + str(arg1).zfill(5), True, (0, 0, 0))
    textRect = text.get_rect()
    textRect.centerx = x
    textRect.centery = y
    screen.blit(text, textRect)


warnLine, line = [], []
while opening:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
    key = pygame.key.get_pressed()
    if key[pygame.K_SPACE]:
        opening = False
    running = True
    level = 1
currentFrame = 0
previousShoot = False

i = 0
q = 0
patternNo = 0
length = len(patterns)
while running and level == 1:
    if currentFrame == 0:
        pygame.mixer.music.load(musics[0])
        pygame.mixer.music.play()
    currentFrame += 1
    screen.fill((255, 255, 255))  # 회색 화면
    screen.blit(background[0], (0, 0))

    # Text(score, 520, 30)
    playerPos = (x - 12, y - 22)
    screen.blit(playerImg, playerPos)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
    pygame.event.pump()  # Allow pygame to handle internal actions.
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT]:
        if key[pygame.K_LSHIFT]:
            if x >= xMinusLimit:
                x -= 0.5 * fast
                if x < xMinusLimit: x = xMinusLimit
        else:
            if x >= xMinusLimit:
                x -= 1.5 * fast
                if x < xMinusLimit: x = xMinusLimit
    if key[pygame.K_RIGHT]:
        if key[pygame.K_LSHIFT]:
            if x <= xPlusLimit:
                x += 0.5 * fast
                if x > xPlusLimit: x = xPlusLimit
        else:
            if x <= xPlusLimit:
                x += 1.5 * fast
                if x > xPlusLimit: x = xPlusLimit
    if key[pygame.K_UP]:
        if key[pygame.K_LSHIFT]:
            if y >= yMinusLimit:
                y -= 0.5 * fast
                if y < yMinusLimit: y = yMinusLimit
        else:
            if y >= yMinusLimit:
                y -= 1.5 * fast
                if y < yMinusLimit: y = yMinusLimit
    if key[pygame.K_DOWN]:
        if key[pygame.K_LSHIFT]:
            if y <= yPlusLimit:
                y += 0.5 * fast
                if y > yPlusLimit: y = yPlusLimit
        else:
            if y <= yPlusLimit:
                y += 1.5 * fast
                if y > yPlusLimit: y = yPlusLimit
    if length > patternNo:
        if currentFrame == timingPoints[patternNo]:
            bullets.extend(patterns[patternNo])
            patternNo += 1

    for bullet in bullets:
        bullet.go(x, y, currentFrame)
        # if (bullet.x - x) ** 2 + (bullet.y - y) ** 2 < (bullet.size / 2) ** 2:
        #     bullets = []
        #     i = 0
        #     break
        if bullet.x < -10 or bullet.x > 410 or bullet.y < -10 or bullet.y > 510:
            bullets.remove(bullet)
        screen.blit(bullet.image, (int(bullet.x - bullet.size / 2), int(bullet.y - bullet.size / 2)))
    fpsClock.tick(FPS)
    pygame.display.flip()

screen.blit(gameOverImg, (0, 0))
Text(score, screen.get_rect().centerx, screen.get_rect().centery)
pygame.display.flip()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
