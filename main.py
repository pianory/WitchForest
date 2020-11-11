import pygame
import random
import sys
import math
import time

# -*- coding:utf-8 -*-#

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((640, 640))

# 기본 변수
FPS = 60
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

    def show(self, playerX, playerY):
        pass


class BulletPlayer(Bullet):
    def __init__(self, timing, x, y, image, size, playerposX, playerposY, speed, startX, startY, angle):
        super().__init__(timing, x, y, image, size, angle, speed, startX, startY)
        self.playerposX, self.playerposY = playerposX, playerposY

    def show(self, playerX, playerY):
        self.angle = math.atan(
            (playerY - self.startY) / (playerX - self.startX+0.0001)) / math.pi if playerX > self.startX else (math.pi + math.atan(
            (playerY - self.startY) / (playerX - self.startX+0.0001))) / math.pi


class BulletShow:
    def __init__(self, timing, image, size, startX, startY, angle, speed, status, x, y):
        self.timing, self.image, self.size, self.startX, self.startY, self.angle, self.status = timing, image, size, startX, startY, angle, status
        self.x, self.y = x, y
        self.speed = speed

    def go(self, c):
        global FPS
        self.x = self.startX + math.cos(self.angle * math.pi) * self.speed * (c - self.timing) / 1000 * FPS
        self.y = self.startY + math.sin(self.angle * math.pi) * self.speed * (c - self.timing) / 1000 * FPS


def Circle(timing, x, y, image, size, angle, speed, shift):
    global FPS
    a = []
    i = 0
    while i < 2:
        a.append(Bullet(timing, x, y, image, size, i + shift, speed * 60 / FPS, x, y))
        i += angle
    return a


def Opener(timing, x, y, image, size, angle, speed):
    global FPS
    a = []
    speedList = list(map(float, speed.split(";")))
    for i in speedList:
        a.append(Bullet(timing, x, y, image, size, angle, i * 60 / FPS, x, y))
    return a


f = open("pattern1.ptn", "r")  # File Read
cr = 0
timingPoints = []
patterns = []
cur = []
nowLine=0
while True:
    # print(nowLine)
    line = f.readline()
    if not line: break
    p = list(map(str, line.split()))
    if cr == int(p[0]):
        if p[1] == "C":
            r, s = p[7].split(";")
            cur.extend(
                Circle(int(p[0]), float(p[2]), float(p[3]), bulletImg[int(p[4])], float(p[5]), float(r), float(p[6]),
                       float(s)))
        elif p[1] == "L":
            cur.append(Bullet(int(p[0]), float(p[2]), float(p[3]), bulletImg[int(p[4])], float(p[5]), float(p[7]),
                              float(p[6]) * 60 / FPS, float(p[2]), float(p[3])))
        elif p[1] == "E":
            cur.append(BulletPlayer(int(p[0]), float(p[2]), float(p[3]), bulletImg[int(p[4])], float(p[5]), None, None,
                                    float(p[6]) * 60 / FPS, int(p[2]), int(p[3]), 0))
        elif p[1] == "O":
            cur.extend(
                Opener(int(p[0]), float(p[2]), float(p[3]), bulletImg[int(p[4])], float(p[5]), float(p[7]), p[6]))
    else:
        if cr != 0:
            patterns.append(cur)
            timingPoints.append(cr)
        cur = []
        cr = int(p[0])
        if p[1] == "C":
            r, s = p[7].split(";")
            cur.extend(
                Circle(int(p[0]), float(p[2]), float(p[3]), bulletImg[int(p[4])], float(p[5]), float(r), float(p[6]),
                       float(s)))
        elif p[1] == "L":
            cur.append(Bullet(int(p[0]), float(p[2]), float(p[3]), bulletImg[int(p[4])], float(p[5]), float(p[7]),
                              float(p[6]) * 60 / FPS, float(p[2]), float(p[3])))
        elif p[1] == "E":
            cur.append(BulletPlayer(int(p[0]), float(p[2]), float(p[3]), bulletImg[int(p[4])], float(p[5]), None, None,
                                    float(p[6]) * 60 / FPS, int(p[2]), int(p[3]), 0))
        elif p[1] == "O":
            cur.extend(
                Opener(int(p[0]), float(p[2]), float(p[3]), bulletImg[int(p[4])], float(p[5]), float(p[7]), p[6]))
    # nowLine += 1
timingPoints.append(cr)
patterns.append(cur)
f.close()


def Text(arg1, x, y):
    font = pygame.font.Font("./fonts/HeirofLightRegular.ttf", 18)
    text = font.render("TIMING  " + str(arg1).zfill(10), True, (0, 0, 0))
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
isStart = True

i = 0
q = 0
patternNo = 0
length = len(patterns)
bullets = []
for _ in range(500):
    bullets.append(BulletShow(None, None, None, None, None, None, None, False, None, None)) # Tmg, img, siz, sx, sy, ang, spd, sta, x, y
while running and level == 1:
    if isStart:
        pygame.mixer.music.load(musics[0])
        pygame.mixer.music.play()
        start = int(round(time.time() * 1000))
        print(start)
        isStart = False
    nowTime = int(round(time.time() * 1000))
    screen.fill((255, 255, 255))  # 회색 화면
    screen.blit(background[0], (0, 0))

    Text(nowTime-start, 520, 30)
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
        if nowTime - start >= int(timingPoints[patternNo]):
            j = 0
            curr = patterns[patternNo][j]
            curr.show(x, y)
            i = 0
            while j < len(patterns[patternNo]):
                if not bullets[i].status:
                    bullets[i].timing, bullets[i].image, bullets[i].size, bullets[i].startX, bullets[i].startY, bullets[i].angle, bullets[i].speed, bullets[i].x, bullets[i].y \
                        = curr.timing, curr.image, curr.size, curr.startX, curr.startY, curr.angle, curr.speed, curr.x, curr.y
                    bullets[i].status = True
                    j += 1
                    if j >= len(patterns[patternNo]):
                        break
                    curr = patterns[patternNo][j]
                    curr.show(x, y)
                i += 1
            patternNo += 1
    for i in bullets:
        if i.status:
            i.go(nowTime - start)
            if i.x < -10 or i.x > 410 or i.y < -10 or i.y > 510:
                i.status = False
            else:
                # if (i.x - x) ** 2 + (i.y - y) ** 2 < (i.size / 2) ** 2:
                #     bullets = []
                #     for _ in range(500):
                #         bullets.append(BulletShow(None, None, None, None, None, None, None, False, None, None)) # Tmg, img, siz, sx, sy, ang, spd, sta, x, y
                #     break
                screen.blit(i.image, (int(int(i.x) - i.size / 2), int(int(i.y) - i.size / 2)))
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
