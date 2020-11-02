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
yPlusLimit = 500
bullets = []
opening = True
running = False
level = 0

# 미디어 변수
bulletImg = None
playerImg = None
gameOverImg = None
x = 200
y = 500

try:
    bulletImg = [pygame.image.load("./img/asteroid15_1.png"), pygame.image.load("./img/asteroid15_2.png"),
                 pygame.image.load("./img/asteroid15_3.png"), pygame.image.load("./img/asteroid15_4.png")]
    warnImg = [pygame.image.load("./img/danger25.png"), pygame.image.load("./img/danger50.png")]
    lineImg = [pygame.image.load("./img/line25.png"), pygame.image.load("./img/line50.png"),
               pygame.image.load("./img/line375.png")]
    gameOverImg = pygame.image.load("./img/gameover.jpg")
    playerImg = pygame.transform.scale(pygame.image.load("./img/player.png"), (37, 64))
    background = [pygame.image.load("./img/backgroundTest.jpg")]
    musics = ["./audio/Armageddon.ogg"]
    judge = [pygame.image.load("./img/300.png"), pygame.image.load("./img/200.png"), pygame.image.load("./img/100.png"),
             pygame.image.load("./img/50.png"), pygame.image.load("./img/0.png")]

except Exception as err:
    print('그림 또는 효과음 삽입에 문제가 있습니다.: ', err)
    pygame.quit()
    sys.exit(0)


class Bullet:
    def __init__(self, x, y, image, size, angle, speed):
        self.x, self.y, self.image, self.size, self.angle, self.speed = x, y, image, size, angle, speed

    def go(self, playerX, playerY):
        self.x += math.cos(self.angle * math.pi) * self.speed
        self.y += math.sin(self.angle * math.pi) * self.speed


class BulletPlayer:
    def __init__(self, x, y, image, size, playerposX, playerposY, speed, startX, startY):
        self.x, self.y, self.image, self.size, self.playerposX, self.playerposY, self.speed = x, y, image, size, playerposX, playerposY, speed
        self.startX, self.startY = startX, startY

    def go(self, playerX, playerY):
        if self.playerposX is None and self.playerposY is None:
            self.playerposX, self.playerposY = playerX, playerY
        self.x += self.speed * (self.playerposX - self.startX) / (
                    ((self.playerposX - self.startX) ** 2 + (self.playerposY - self.startY) ** 2) ** 0.5)
        self.y += self.speed * (self.playerposY - self.startY) / (
                    ((self.playerposX - self.startX) ** 2 + (self.playerposY - self.startY) ** 2) ** 0.5)


def Circle(x, y, image, size, angle, speed, shift):
    a = []
    i = 0
    while i <= 2:
        i += angle
        a.append(Bullet(x, y, image, size, i + shift, speed))
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
            r, s = map(float, p[7].split(";"))
            cur.extend(Circle(float(p[2]), float(p[3]), bulletImg[int(p[4])], float(p[5]), r, float(p[6]), s))
        elif p[1] == "L":
            cur.append(Bullet(float(p[2]), float(p[3]), bulletImg[int(p[4])], float(p[5]), float(p[7]), float(p[6])))
        elif p[1] == "E":
            cur.append(BulletPlayer(float(p[2]), float(p[3]), bulletImg[int(p[4])], float(p[5]), None, None, float(p[6]), int(p[2]), int(p[3])))
    else:
        if cr != 0:
            patterns.append(cur)
            timingPoints.append(cr)
        cur = []
        cr = int(p[0])
        if p[1] == "C":
            r, s = map(float, p[7].split(";"))
            cur.extend(Circle(float(p[2]), float(p[3]), bulletImg[int(p[4])], float(p[5]), r, float(p[6]), s))
        elif p[1] == "L":
            cur.append(Bullet(float(p[2]), float(p[3]), bulletImg[int(p[4])], float(p[5]), float(p[7]), float(p[6])))
        elif p[1] == "E":
            cur.append(BulletPlayer(float(p[2]), float(p[3]), bulletImg[int(p[4])], float(p[5]), None, None, float(p[6]), int(p[2]), int(p[3])))
timingPoints.append(cr)
patterns.append(cur)
f.close()


# 탄막 변수
class BulletC:
    def __init__(self, x, y, image, size, startFrame, movementX1, movementY1, first, movementX2, movementY2, second,
                 movementX3, movementY3, fin):
        self.x, self.y, self.image, self.size, self.startFrame = x, y, image, size, startFrame
        self.movementX1, self.movementY1, self.movementX2, self.movementY2, self.movementX3, self.movementY3 = movementX1, movementY1, movementX2, movementY2, movementX3, movementY3
        self.first, self.second, self.fin = first, second, fin

    def go(self, nowFrame):
        t = nowFrame - self.startFrame
        if nowFrame - self.startFrame <= self.first:
            self.x = eval(self.movementX1)
            self.y = eval(self.movementY1)

        elif nowFrame - self.startFrame <= self.second:
            self.x = eval(self.movementX2)
            self.y = eval(self.movementY2)

        elif nowFrame - self.startFrame <= self.fin:
            self.x = eval(self.movementX3)
            self.y = eval(self.movementY3)


class WarnX:
    def __init__(self, x, image, size, start, end):
        self.x, self.image, self.size = x, image, size
        self.start, self.end = start, end

    def __eq__(self, other):
        return self.x == other.x and self.size == other.size and self.start == other.start and self.end == other.end


class DangerousX:
    def __init__(self, x, image, size, start, end):
        self.x, self.image, self.size = x, image, size
        self.start, self.end = start, end

    def __eq__(self, other):
        return self.x == other.x and self.size == other.size and self.start == other.start and self.end == other.end


def Text(arg1, x, y):
    font = pygame.font.Font("./fonts/HeirofLightRegular.ttf", 18)
    text = font.render("SCORE  " + str(arg1).zfill(5), True, (0, 0, 0))
    textRect = text.get_rect()
    textRect.centerx = x
    textRect.centery = y
    screen.blit(text, textRect)


def CirclePattern(x, y, image, size, frame, angle, speed, shift):
    a = []
    i = 0
    while i <= 2:
        i += angle
        a.append(BulletC(x, y, image, size, frame,
                         str(x) + " + " + str(speed) + " * math.cos(math.pi * " + str(i + shift) + ") * t",
                         str(y) + " + " + str(speed) + " * math.sin(math.pi * " + str(i + shift) + ") * t",
                         640 // speed, 0, 0, 0, 0, 0, 0))
    return a


def LinearPattern(x, y, image, size, frame, angle, speed):
    return BulletC(x, y, image, size, frame,
                   str(x) + " + " + str(speed) + " * math.cos(math.pi * " + str(angle) + ") * t",
                   str(y) + " + " + str(speed) + " * math.sin(math.pi * " + str(angle) + ") * t", 1000, 0, 0, 0, 0, 0,
                   0)


def Pattern1Easy(frame, now, linearWarn, linear, playerX, playerY):
    bpm = 210
    offset = 589
    global FPS
    if 0 <= frame < int((offset + 25 * 60 / bpm * 1000) / (1000 / FPS)):
        if frame == int((offset + 0 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[0], 15, frame, 0.1, 15, 0))
        elif frame == int((offset + 3.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                [BulletC(400, 250, bulletImg[1], 15, frame, "400", "250", 77, "250", "250 - 15 * (t - 77)", 150, 0, 0,
                         0),
                 BulletC(400, 250, bulletImg[1], 15, frame, "360 - 40 * ((t - 43)/43) ** 3", "250", 43, "360", "250",
                         77, "360", "250 + 15 * (t - 77)", 100),
                 BulletC(400, 250, bulletImg[1], 15, frame, "320 - 80 * ((t - 43)/43) ** 3", "250", 43, "320", "250",
                         77, "320", "250 - 15 * (t - 77)", 100),
                 BulletC(400, 250, bulletImg[1], 15, frame, "280 - 120 * ((t - 43)/43) ** 3", "250", 43, "280", "250",
                         77, "280", "250 + 15 * (t - 77)", 100),
                 BulletC(400, 250, bulletImg[1], 15, frame, "240 - 160 * ((t - 43)/43) ** 3", "250", 43, "240", "250",
                         77, "240", "250 - 15 * (t - 77)", 100),
                 BulletC(400, 250, bulletImg[1], 15, frame, "200 - 200 * ((t - 43)/43) ** 3", "250", 43, "200", "250",
                         77, "200", "250 + 15 * (t - 77)", 100),
                 BulletC(400, 250, bulletImg[1], 15, frame, "160 - 240 * ((t - 43)/43) ** 3", "250", 43, "160", "250",
                         77, "160", "250 - 15 * (t - 77)", 100),
                 BulletC(400, 250, bulletImg[1], 15, frame, "120 - 280 * ((t - 43)/43) ** 3", "250", 43, "120", "250",
                         77, "120", "250 + 15 * (t - 77)", 100),
                 BulletC(400, 250, bulletImg[1], 15, frame, "80 - 250 * ((t - 43)/43) ** 3", "250", 43, "80", "250",
                         77, "80", "250 - 15 * (t - 77)", 100),
                 BulletC(400, 250, bulletImg[1], 15, frame, "40 - 360 * ((t - 43)/43) ** 3", "250", 43, "40", "250",
                         77, "40", "250 + 15 * (t - 77)", 100),
                 BulletC(400, 250, bulletImg[1], 15, frame, "0 - 400 * ((t - 43)/43) ** 3", "250", 43, "0", "250",
                         77, "0", "250 - 15 * (t - 77)", 100),
                 ])
        elif frame == int((offset + 3.75 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                [BulletC(5, 125, bulletImg[1], 15, frame, "5", "125", 69, "0", "125 - 10 * (t - 69)", 150, 0, 0, 0),
                 BulletC(5, 125, bulletImg[1], 15, frame, "45 + 40 * ((t - 43)/43) ** 3", "125", 43, "45", "125",
                         69, "45", "125 + 10 * (t - 69)", 100),
                 BulletC(5, 125, bulletImg[1], 15, frame, "85 + 80 * ((t - 43)/43) ** 3", "125", 43, "85", "125",
                         69, "85", "125 - 10 * (t - 69)", 100),
                 BulletC(5, 125, bulletImg[1], 15, frame, "125 + 120 * ((t - 43)/43) ** 3", "125", 43, "125", "125",
                         69, "125", "125 + 10 * (t - 69)", 100),
                 BulletC(5, 125, bulletImg[1], 15, frame, "165 + 160 * ((t - 43)/43) ** 3", "125", 43, "165", "125",
                         69, "165", "125 - 10 * (t - 69)", 100),
                 BulletC(5, 125, bulletImg[1], 15, frame, "205 + 200 * ((t - 43)/43) ** 3", "125", 43, "205", "125",
                         69, "205", "125 + 10 * (t - 69)", 100),
                 BulletC(5, 125, bulletImg[1], 15, frame, "245 + 240 * ((t - 43)/43) ** 3", "125", 43, "245", "125",
                         69, "245", "125 - 10 * (t - 69)", 100),
                 BulletC(5, 125, bulletImg[1], 15, frame, "285 + 280 * ((t - 43)/43) ** 3", "125", 43, "285", "125",
                         69, "285", "125 + 10 * (t - 69)", 100),
                 BulletC(5, 125, bulletImg[1], 15, frame, "325 + 320 * ((t - 43)/43) ** 3", "125", 43, "325", "125",
                         69, "325", "125 - 10 * (t - 69)", 100),
                 BulletC(5, 125, bulletImg[1], 15, frame, "365 + 360 * ((t - 43)/43) ** 3", "125", 43, "365", "125",
                         69, "365", "125 + 10 * (t - 69)", 100)
                 ])
        elif frame == int((offset + 4 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                [BulletC(5, 375, bulletImg[1], 15, frame, "5", "375", 60, "0", "375 - 10 * (t - 60)", 100, 0, 0, 0),
                 BulletC(5, 375, bulletImg[1], 15, frame, "45 + 40 * ((t - 43)/43) ** 3", "375", 43, "45", "375",
                         60, "45", "375 + 12 * (t - 60)", 100),
                 BulletC(5, 375, bulletImg[1], 15, frame, "85 + 80 * ((t - 43)/43) ** 3", "375", 43, "85", "375",
                         60, "85", "375 - 12 * (t - 60)", 100),
                 BulletC(5, 375, bulletImg[1], 15, frame, "125 + 120 * ((t - 43)/43) ** 3", "375", 43, "125", "375",
                         60, "125", "375 + 12 * (t - 60)", 100),
                 BulletC(5, 375, bulletImg[1], 15, frame, "165 + 160 * ((t - 43)/43) ** 3", "375", 43, "165", "375",
                         60, "165", "375 - 12 * (t - 60)", 100),
                 BulletC(5, 375, bulletImg[1], 15, frame, "205 + 200 * ((t - 43)/43) ** 3", "375", 43, "205", "375",
                         60, "205", "375 + 12 * (t - 60)", 100),
                 BulletC(5, 375, bulletImg[1], 15, frame, "245 + 240 * ((t - 43)/43) ** 3", "375", 43, "245", "375",
                         60, "245", "375 - 12 * (t - 60)", 100),
                 BulletC(5, 375, bulletImg[1], 15, frame, "285 + 280 * ((t - 43)/43) ** 3", "375", 43, "285", "375",
                         60, "285", "375 + 12 * (t - 60)", 100),
                 BulletC(5, 375, bulletImg[1], 15, frame, "325 + 320 * ((t - 43)/43) ** 3", "375", 43, "325", "375",
                         60, "325", "375 - 12 * (t - 60)", 100),
                 BulletC(5, 375, bulletImg[1], 15, frame, "365 + 360 * ((t - 43)/43) ** 3", "375", 43, "365", "375",
                         60, "365", "375 + 12 * (t - 60)", 100)
                 ])
        elif frame == int((offset + 7.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[0], 15, frame, 0.1, 11, 0))
        elif frame == int((offset + 8 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[0], 15, frame, 0.1, 11, 0.05))
        elif frame == int((offset + 9.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(50, 320, bulletImg[0], 15, frame, 0.1, 11, 0))
        elif frame == int((offset + 10.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(350, 320, bulletImg[0], 15, frame, 0.1, 11, 0))
        elif frame == int((offset + 11 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend([BulletC(100, 5, bulletImg[2], 15, frame,
                                "100 + 15 * (" + str(playerX) + " - 100) / math.sqrt((100 - " + str(
                                    playerX) + ") ** 2 + (5 - " + str(playerY) + ") ** 2) * t",
                                "5 + 15 * (" + str(playerY) + " - 5) / math.sqrt((100 - " + str(
                                    playerX) + ") ** 2 + (5 - " + str(playerY) + ") ** 2) * t", 100, 0, 0, 0, 0, 0, 0),
                        BulletC(300, 5, bulletImg[2], 15, frame,
                                "300 + 15 * (" + str(playerX) + " - 300) / math.sqrt((300 - " + str(
                                    playerX) + ") ** 2 + (5 - " + str(playerY) + ") ** 2) * t",
                                "5 + 15 * (" + str(playerY) + " - 5) / math.sqrt((300 - " + str(
                                    playerX) + ") ** 2 + (5 - " + str(playerY) + ") ** 2) * t", 100, 0, 0, 0, 0, 0, 0),
                        ])
        elif frame == int((offset + 11.25 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend([BulletC(100, 5, bulletImg[2], 15, frame,
                                "100 + 15 * (" + str(playerX) + " - 100) / math.sqrt((100 - " + str(
                                    playerX) + ") ** 2 + (5 - " + str(playerY) + ") ** 2) * t",
                                "5 + 15 * (" + str(playerY) + " - 5) / math.sqrt((100 - " + str(
                                    playerX) + ") ** 2 + (5 - " + str(playerY) + ") ** 2) * t", 100, 0, 0, 0, 0, 0, 0),
                        BulletC(300, 5, bulletImg[2], 15, frame,
                                "300 + 15 * (" + str(playerX) + " - 300) / math.sqrt((300 - " + str(
                                    playerX) + ") ** 2 + (5 - " + str(playerY) + ") ** 2) * t",
                                "5 + 15 * (" + str(playerY) + " - 5) / math.sqrt((300 - " + str(
                                    playerX) + ") ** 2 + (5 - " + str(playerY) + ") ** 2) * t", 100, 0, 0, 0, 0, 0, 0),
                        ])
        elif frame == int((offset + 11.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend([BulletC(100, 5, bulletImg[2], 15, frame,
                                "100 + 15 * (" + str(playerX) + " - 100) / math.sqrt((100 - " + str(
                                    playerX) + ") ** 2 + (5 - " + str(playerY) + ") ** 2) * t",
                                "5 + 15 * (" + str(playerY) + " - 5) / math.sqrt((100 - " + str(
                                    playerX) + ") ** 2 + (5 - " + str(playerY) + ") ** 2) * t", 100, 0, 0, 0, 0, 0, 0),
                        BulletC(300, 5, bulletImg[2], 15, frame,
                                "300 + 15 * (" + str(playerX) + " - 300) / math.sqrt((300 - " + str(
                                    playerX) + ") ** 2 + (5 - " + str(playerY) + ") ** 2) * t",
                                "5 + 15 * (" + str(playerY) + " - 5) / math.sqrt((300 - " + str(
                                    playerX) + ") ** 2 + (5 - " + str(playerY) + ") ** 2) * t", 100, 0, 0, 0, 0, 0, 0),
                        ])
        elif frame == int((offset + 11.75 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend([BulletC(100, 5, bulletImg[2], 15, frame,
                                "100 + 15 * (" + str(playerX) + " - 100) / math.sqrt((100 - " + str(
                                    playerX) + ") ** 2 + (5 - " + str(playerY) + ") ** 2) * t",
                                "5 + 15 * (" + str(playerY) + " - 5) / math.sqrt((100 - " + str(
                                    playerX) + ") ** 2 + (5 - " + str(playerY) + ") ** 2) * t", 100, 0, 0, 0, 0, 0, 0),
                        BulletC(300, 5, bulletImg[2], 15, frame,
                                "300 + 15 * (" + str(playerX) + " - 300) / math.sqrt((300 - " + str(
                                    playerX) + ") ** 2 + (5 - " + str(playerY) + ") ** 2) * t",
                                "5 + 15 * (" + str(playerY) + " - 5) / math.sqrt((300 - " + str(
                                    playerX) + ") ** 2 + (5 - " + str(playerY) + ") ** 2) * t", 100, 0, 0, 0, 0, 0, 0),
                        ])
        elif frame == int((offset + 12 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[0], 15, frame, 0.1, 11, 0))
        elif frame == int((offset + 12.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[0], 15, frame, 0.1, 11, 0.05))
        elif frame == int((offset + 13.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(50, 320, bulletImg[0], 15, frame, 0.1, 11, 0))
        elif frame == int((offset + 14.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(350, 320, bulletImg[0], 15, frame, 0.1, 11, 0))
        elif frame == int((offset + 15 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend([BulletC(100, 5, bulletImg[2], 15, frame,
                                "100 + 15 * (" + str(playerX) + " - 100) / math.sqrt((100 - " + str(
                                    playerX) + ") ** 2 + (5 - " + str(playerY) + ") ** 2) * t",
                                "5 + 15 * (" + str(playerY) + " - 5) / math.sqrt((100 - " + str(
                                    playerX) + ") ** 2 + (5 - " + str(playerY) + ") ** 2) * t", 100, 0, 0, 0, 0, 0, 0),
                        BulletC(300, 5, bulletImg[2], 15, frame,
                                "300 + 15 * (" + str(playerX) + " - 300) / math.sqrt((300 - " + str(
                                    playerX) + ") ** 2 + (5 - " + str(playerY) + ") ** 2) * t",
                                "5 + 15 * (" + str(playerY) + " - 5) / math.sqrt((300 - " + str(
                                    playerX) + ") ** 2 + (5 - " + str(playerY) + ") ** 2) * t", 100, 0, 0, 0, 0, 0, 0),
                        ])
        elif frame == int((offset + 15.25 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend([BulletC(100, 5, bulletImg[2], 15, frame,
                                "100 + 15 * (" + str(playerX) + " - 100) / math.sqrt((100 - " + str(
                                    playerX) + ") ** 2 + (5 - " + str(playerY) + ") ** 2) * t",
                                "5 + 15 * (" + str(playerY) + " - 5) / math.sqrt((100 - " + str(
                                    playerX) + ") ** 2 + (5 - " + str(playerY) + ") ** 2) * t", 100, 0, 0, 0, 0, 0, 0),
                        BulletC(300, 5, bulletImg[2], 15, frame,
                                "300 + 15 * (" + str(playerX) + " - 300) / math.sqrt((300 - " + str(
                                    playerX) + ") ** 2 + (5 - " + str(playerY) + ") ** 2) * t",
                                "5 + 15 * (" + str(playerY) + " - 5) / math.sqrt((300 - " + str(
                                    playerX) + ") ** 2 + (5 - " + str(playerY) + ") ** 2) * t", 100, 0, 0, 0, 0, 0, 0),
                        ])
        elif frame == int((offset + 15.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend([BulletC(100, 5, bulletImg[2], 15, frame,
                                "100 + 15 * (" + str(playerX) + " - 100) / math.sqrt((100 - " + str(
                                    playerX) + ") ** 2 + (5 - " + str(playerY) + ") ** 2) * t",
                                "5 + 15 * (" + str(playerY) + " - 5) / math.sqrt((100 - " + str(
                                    playerX) + ") ** 2 + (5 - " + str(playerY) + ") ** 2) * t", 100, 0, 0, 0, 0, 0, 0),
                        BulletC(300, 5, bulletImg[2], 15, frame,
                                "300 + 15 * (" + str(playerX) + " - 300) / math.sqrt((300 - " + str(
                                    playerX) + ") ** 2 + (5 - " + str(playerY) + ") ** 2) * t",
                                "5 + 15 * (" + str(playerY) + " - 5) / math.sqrt((300 - " + str(
                                    playerX) + ") ** 2 + (5 - " + str(playerY) + ") ** 2) * t", 100, 0, 0, 0, 0, 0, 0),
                        ])
        elif frame == int((offset + 15.75 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend([BulletC(100, 5, bulletImg[2], 15, frame,
                                "100 + 15 * (" + str(playerX) + " - 100) / math.sqrt((100 - " + str(
                                    playerX) + ") ** 2 + (5 - " + str(playerY) + ") ** 2) * t",
                                "5 + 15 * (" + str(playerY) + " - 5) / math.sqrt((100 - " + str(
                                    playerX) + ") ** 2 + (5 - " + str(playerY) + ") ** 2) * t", 100, 0, 0, 0, 0, 0, 0),
                        BulletC(300, 5, bulletImg[2], 15, frame,
                                "300 + 15 * (" + str(playerX) + " - 300) / math.sqrt((300 - " + str(
                                    playerX) + ") ** 2 + (5 - " + str(playerY) + ") ** 2) * t",
                                "5 + 15 * (" + str(playerY) + " - 5) / math.sqrt((300 - " + str(
                                    playerX) + ") ** 2 + (5 - " + str(playerY) + ") ** 2) * t", 100, 0, 0, 0, 0, 0, 0),
                        ])
        elif frame == int((offset + 16 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 12, frame, 0.2, 10, 0))
        elif frame == int((offset + 16.125 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 12, frame, 0.2, 10, 0.025))
        elif frame == int((offset + 16.25 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 12, frame, 0.2, 10, 0.05))
        elif frame == int((offset + 16.375 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 12, frame, 0.2, 10, 0.075))
        elif frame == int((offset + 16.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 12, frame, 0.2, 10, 0.1))
        elif frame == int((offset + 16.625 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 12, frame, 0.2, 10, 0.125))
        elif frame == int((offset + 16.75 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 12, frame, 0.2, 10, 0.15))
        elif frame == int((offset + 16.875 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 12, frame, 0.2, 10, 0.175))
        elif frame == int((offset + 17 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 12, frame, 0.2, 10, 0))
        elif frame == int((offset + 17.125 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 12, frame, 0.2, 10, 0.025))
        elif frame == int((offset + 17.25 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 12, frame, 0.2, 10, 0.05))
        elif frame == int((offset + 17.375 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 12, frame, 0.2, 10, 0.075))
        elif frame == int((offset + 17.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 12, frame, 0.2, 10, 0.1))
        elif frame == int((offset + 17.625 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 12, frame, 0.2, 10, 0.125))
        elif frame == int((offset + 17.75 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 12, frame, 0.2, 10, 0.15))
        elif frame == int((offset + 17.875 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 12, frame, 0.2, 10, 0.175))
        elif frame == int((offset + 18 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 12, frame, 0.2, 10, 0))
        elif frame == int((offset + 18.125 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 12, frame, 0.2, 10, 0.025))
        elif frame == int((offset + 18.25 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 12, frame, 0.2, 10, 0.05))
        elif frame == int((offset + 18.375 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 12, frame, 0.2, 10, 0.075))
        elif frame == int((offset + 18.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 12, frame, 0.2, 10, 0.1))
        elif frame == int((offset + 18.625 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 12, frame, 0.2, 10, 0.125))
        elif frame == int((offset + 18.75 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 12, frame, 0.2, 10, 0.15))
        elif frame == int((offset + 18.875 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 12, frame, 0.2, 10, 0.175))
        elif frame == int((offset + 20 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend([BulletC(0, 5, bulletImg[2], 15, frame, "0", "5 + t * 8", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(40, 5, bulletImg[2], 15, frame, "40", "5 + t * 8", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(80, 5, bulletImg[2], 15, frame, "80", "5 + t * 8", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(120, 5, bulletImg[2], 15, frame, "120", "5 + t * 8", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(160, 5, bulletImg[2], 15, frame, "160", "5 + t * 8", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(200, 5, bulletImg[2], 15, frame, "200", "5 + t * 8", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(240, 5, bulletImg[2], 15, frame, "240", "5 + t * 8", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(280, 5, bulletImg[2], 15, frame, "280", "5 + t * 8", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(320, 5, bulletImg[2], 15, frame, "320", "5 + t * 8", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(360, 5, bulletImg[2], 15, frame, "360", "5 + t * 8", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(400, 5, bulletImg[2], 15, frame, "400", "5 + t * 8", 80, 0, 0, 0, 0, 0, 0)
                        ])
        elif frame == int((offset + 21.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend([BulletC(5, 0, bulletImg[0], 15, frame, "5 + t * 5", "0", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(5, 64, bulletImg[0], 15, frame, "5 + t * 5", "64", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(5, 128, bulletImg[0], 15, frame, "5 + t * 5", "128", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(5, 192, bulletImg[0], 15, frame, "5 + t * 5", "192", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(5, 256, bulletImg[0], 15, frame, "5 + t * 5", "256", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(5, 320, bulletImg[0], 15, frame, "5 + t * 5", "320", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(5, 384, bulletImg[0], 15, frame, "5 + t * 5", "384", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(5, 448, bulletImg[0], 15, frame, "5 + t * 5", "448", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(5, 512, bulletImg[0], 15, frame, "5 + t * 5", "512", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(5, 586, bulletImg[0], 15, frame, "5 + t * 5", "586", 80, 0, 0, 0, 0, 0, 0),
                        ])
        elif frame == int((offset + 23 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend([BulletC(395, 0 + 32, bulletImg[0], 15, frame, "395 - t * 5", "0+32", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(395, 64 + 32, bulletImg[0], 15, frame, "395 - t * 5", "64+32", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(395, 128 + 32, bulletImg[0], 15, frame, "395 - t * 5", "128+32", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(395, 192 + 32, bulletImg[0], 15, frame, "395 - t * 5", "192+32", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(395, 256 + 32, bulletImg[0], 15, frame, "395 - t * 5", "256+32", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(395, 320 + 32, bulletImg[0], 15, frame, "395 - t * 5", "320+32", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(395, 384 + 32, bulletImg[0], 15, frame, "395 - t * 5", "384+32", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(395, 448 + 32, bulletImg[0], 15, frame, "395 - t * 5", "448+32", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(395, 512 + 32, bulletImg[0], 15, frame, "395 - t * 5", "512+32", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(395, 586 + 32, bulletImg[0], 15, frame, "395 - t * 5", "586+32", 80, 0, 0, 0, 0, 0, 0),
                        ])
        elif frame == int((offset + 24 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 12, frame, 0.2, 10, 0))
        elif frame == int((offset + 24.125 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 12, frame, 0.2, 10, -0.25))
        elif frame == int((offset + 24.25 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 12, frame, 0.2, 10, -0.5))
        elif frame == int((offset + 24.375 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 12, frame, 0.2, 10, -0.75))
        elif frame == int((offset + 24.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 12, frame, 0.2, 10, -1))
        elif frame == int((offset + 24.625 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 12, frame, 0.2, 10, -1.25))
        elif frame == int((offset + 24.75 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 12, frame, 0.2, 10, -1.5))
        elif frame == int((offset + 24.875 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 12, frame, 0.2, 10, -1.75))
    elif int((offset + 25 * 60 / bpm * 1000) / (1000 / FPS)) <= frame < int(
            (offset + 47 * 60 / bpm * 1000) / (1000 / FPS)):
        if frame == int((offset + 25 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 12, frame, 0.2, 10, 0))
        elif frame == int((offset + 25.125 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 12, frame, 0.2, 10, -0.25))
        elif frame == int((offset + 25.25 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 12, frame, 0.2, 10, -0.5))
        elif frame == int((offset + 25.375 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 12, frame, 0.2, 10, -0.75))
        elif frame == int((offset + 25.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 12, frame, 0.2, 10, -1))
        elif frame == int((offset + 25.625 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 12, frame, 0.2, 10, -1.25))
        elif frame == int((offset + 25.75 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 12, frame, 0.2, 10, -1.5))
        elif frame == int((offset + 25.875 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 12, frame, 0.2, 10, -1.75))
        elif frame == int((offset + 26 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 12, frame, 0.2, 10, 0))
        elif frame == int((offset + 26.125 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 12, frame, 0.2, 10, -0.25))
        elif frame == int((offset + 26.25 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 12, frame, 0.2, 10, -0.5))
        elif frame == int((offset + 26.375 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 12, frame, 0.2, 10, -0.75))
        elif frame == int((offset + 26.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 12, frame, 0.2, 10, -1))
        elif frame == int((offset + 26.625 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 12, frame, 0.2, 10, -1.25))
        elif frame == int((offset + 26.75 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 12, frame, 0.2, 10, -1.5))
        elif frame == int((offset + 26.875 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 12, frame, 0.2, 10, -1.75))
        elif frame == int((offset + 28 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend([BulletC(0, 5, bulletImg[2], 15, frame, "0", "5 + t * 8", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(40, 5, bulletImg[2], 15, frame, "40", "5 + t * 8", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(80, 5, bulletImg[2], 15, frame, "80", "5 + t * 8", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(120, 5, bulletImg[2], 15, frame, "120", "5 + t * 8", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(160, 5, bulletImg[2], 15, frame, "160", "5 + t * 8", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(200, 5, bulletImg[2], 15, frame, "200", "5 + t * 8", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(240, 5, bulletImg[2], 15, frame, "240", "5 + t * 8", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(280, 5, bulletImg[2], 15, frame, "280", "5 + t * 8", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(320, 5, bulletImg[2], 15, frame, "320", "5 + t * 8", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(360, 5, bulletImg[2], 15, frame, "360", "5 + t * 8", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(400, 5, bulletImg[2], 15, frame, "400", "5 + t * 8", 80, 0, 0, 0, 0, 0, 0)
                        ])
        elif frame == int((offset + 29.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend([BulletC(5, 0, bulletImg[0], 15, frame, "5 + t * 5", "0", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(5, 64, bulletImg[0], 15, frame, "5 + t * 5", "64", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(5, 128, bulletImg[0], 15, frame, "5 + t * 5", "128", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(5, 192, bulletImg[0], 15, frame, "5 + t * 5", "192", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(5, 256, bulletImg[0], 15, frame, "5 + t * 5", "256", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(5, 320, bulletImg[0], 15, frame, "5 + t * 5", "320", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(5, 384, bulletImg[0], 15, frame, "5 + t * 5", "384", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(5, 448, bulletImg[0], 15, frame, "5 + t * 5", "448", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(5, 512, bulletImg[0], 15, frame, "5 + t * 5", "512", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(5, 586, bulletImg[0], 15, frame, "5 + t * 5", "586", 80, 0, 0, 0, 0, 0, 0),
                        ])
        elif frame == int((offset + 31 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend([BulletC(395, 0 + 32, bulletImg[0], 15, frame, "395 - t * 5", "0+32", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(395, 64 + 32, bulletImg[0], 15, frame, "395 - t * 5", "64+32", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(395, 128 + 32, bulletImg[0], 15, frame, "395 - t * 5", "128+32", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(395, 192 + 32, bulletImg[0], 15, frame, "395 - t * 5", "192+32", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(395, 256 + 32, bulletImg[0], 15, frame, "395 - t * 5", "256+32", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(395, 320 + 32, bulletImg[0], 15, frame, "395 - t * 5", "320+32", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(395, 384 + 32, bulletImg[0], 15, frame, "395 - t * 5", "384+32", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(395, 448 + 32, bulletImg[0], 15, frame, "395 - t * 5", "448+32", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(395, 512 + 32, bulletImg[0], 15, frame, "395 - t * 5", "512+32", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(395, 586 + 32, bulletImg[0], 15, frame, "395 - t * 5", "586+32", 80, 0, 0, 0, 0, 0, 0),
                        ])
        elif frame == int((offset + 32 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 15, frame, 0.2, 10, 0))
        elif frame == int((offset + 32.125 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 15, frame, 0.2, 10, 0.025))
        elif frame == int((offset + 32.25 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 15, frame, 0.2, 10, 0.05))
        elif frame == int((offset + 32.375 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 15, frame, 0.2, 10, 0.075))
        elif frame == int((offset + 32.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 15, frame, 0.2, 10, 0.1))
        elif frame == int((offset + 32.625 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 15, frame, 0.2, 10, 0.125))
        elif frame == int((offset + 32.75 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 15, frame, 0.2, 10, 0.15))
        elif frame == int((offset + 32.875 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 15, frame, 0.2, 10, 0.175))
        elif frame == int((offset + 33 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 15, frame, 0.2, 10, 0))
        elif frame == int((offset + 33.125 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 15, frame, 0.2, 10, 0.025))
        elif frame == int((offset + 33.25 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 15, frame, 0.2, 10, 0.05))
        elif frame == int((offset + 33.375 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 15, frame, 0.2, 10, 0.075))
        elif frame == int((offset + 33.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 15, frame, 0.2, 10, 0.1))
        elif frame == int((offset + 33.625 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 15, frame, 0.2, 10, 0.125))
        elif frame == int((offset + 33.75 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 15, frame, 0.2, 10, 0.15))
        elif frame == int((offset + 33.875 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 15, frame, 0.2, 10, 0.175))
        elif frame == int((offset + 34 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 15, frame, 0.2, 10, 0))
        elif frame == int((offset + 34.125 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 15, frame, 0.2, 10, 0.025))
        elif frame == int((offset + 34.25 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 15, frame, 0.2, 10, 0.05))
        elif frame == int((offset + 34.375 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 15, frame, 0.2, 10, 0.075))
        elif frame == int((offset + 34.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 15, frame, 0.2, 10, 0.1))
        elif frame == int((offset + 34.625 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 15, frame, 0.2, 10, 0.125))
        elif frame == int((offset + 34.75 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 15, frame, 0.2, 10, 0.15))
        elif frame == int((offset + 34.875 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 15, frame, 0.2, 10, 0.175))
        elif frame == int((offset + 36 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend([BulletC(0, 5, bulletImg[2], 15, frame, "0", "5 + t * 8", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(40, 5, bulletImg[2], 15, frame, "40", "5 + t * 8", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(80, 5, bulletImg[2], 15, frame, "80", "5 + t * 8", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(120, 5, bulletImg[2], 15, frame, "120", "5 + t * 8", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(160, 5, bulletImg[2], 15, frame, "160", "5 + t * 8", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(200, 5, bulletImg[2], 15, frame, "200", "5 + t * 8", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(240, 5, bulletImg[2], 15, frame, "240", "5 + t * 8", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(280, 5, bulletImg[2], 15, frame, "280", "5 + t * 8", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(320, 5, bulletImg[2], 15, frame, "320", "5 + t * 8", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(360, 5, bulletImg[2], 15, frame, "360", "5 + t * 8", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(400, 5, bulletImg[2], 15, frame, "400", "5 + t * 8", 80, 0, 0, 0, 0, 0, 0)
                        ])
        elif frame == int((offset + 37.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend([BulletC(5, 0, bulletImg[0], 15, frame, "5 + t * 5", "0", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(5, 64, bulletImg[0], 15, frame, "5 + t * 5", "64", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(5, 128, bulletImg[0], 15, frame, "5 + t * 5", "128", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(5, 192, bulletImg[0], 15, frame, "5 + t * 5", "192", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(5, 256, bulletImg[0], 15, frame, "5 + t * 5", "256", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(5, 320, bulletImg[0], 15, frame, "5 + t * 5", "320", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(5, 384, bulletImg[0], 15, frame, "5 + t * 5", "384", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(5, 448, bulletImg[0], 15, frame, "5 + t * 5", "448", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(5, 512, bulletImg[0], 15, frame, "5 + t * 5", "512", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(5, 586, bulletImg[0], 15, frame, "5 + t * 5", "586", 80, 0, 0, 0, 0, 0, 0),
                        ])
        elif frame == int((offset + 39 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend([BulletC(395, 0 + 32, bulletImg[0], 15, frame, "395 - t * 5", "0+32", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(395, 64 + 32, bulletImg[0], 15, frame, "395 - t * 5", "64+32", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(395, 128 + 32, bulletImg[0], 15, frame, "395 - t * 5", "128+32", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(395, 192 + 32, bulletImg[0], 15, frame, "395 - t * 5", "192+32", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(395, 256 + 32, bulletImg[0], 15, frame, "395 - t * 5", "256+32", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(395, 320 + 32, bulletImg[0], 15, frame, "395 - t * 5", "320+32", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(395, 384 + 32, bulletImg[0], 15, frame, "395 - t * 5", "384+32", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(395, 448 + 32, bulletImg[0], 15, frame, "395 - t * 5", "448+32", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(395, 512 + 32, bulletImg[0], 15, frame, "395 - t * 5", "512+32", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(395, 586 + 32, bulletImg[0], 15, frame, "395 - t * 5", "586+32", 80, 0, 0, 0, 0, 0, 0),
                        ])
        elif frame == int((offset + 40 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 15, frame, 0.2, 10, 0))
        elif frame == int((offset + 40.125 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 15, frame, 0.2, 10, -0.25))
        elif frame == int((offset + 40.25 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 15, frame, 0.2, 10, -0.5))
        elif frame == int((offset + 40.375 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 15, frame, 0.2, 10, -0.75))
        elif frame == int((offset + 40.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 15, frame, 0.2, 10, -1))
        elif frame == int((offset + 40.625 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 15, frame, 0.2, 10, -1.25))
        elif frame == int((offset + 40.75 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 15, frame, 0.2, 10, -1.5))
        elif frame == int((offset + 40.875 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 15, frame, 0.2, 10, -1.75))
        elif frame == int((offset + 41 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 15, frame, 0.2, 10, 0))
        elif frame == int((offset + 41.125 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 15, frame, 0.2, 10, -0.25))
        elif frame == int((offset + 41.25 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 15, frame, 0.2, 10, -0.5))
        elif frame == int((offset + 41.375 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 15, frame, 0.2, 10, -0.75))
        elif frame == int((offset + 41.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 15, frame, 0.2, 10, -1))
        elif frame == int((offset + 41.625 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 15, frame, 0.2, 10, -1.25))
        elif frame == int((offset + 41.75 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 15, frame, 0.2, 10, -1.5))
        elif frame == int((offset + 41.875 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 15, frame, 0.2, 10, -1.75))
        elif frame == int((offset + 42 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 15, frame, 0.2, 10, 0))
        elif frame == int((offset + 42.125 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 15, frame, 0.2, 10, -0.25))
        elif frame == int((offset + 42.25 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 15, frame, 0.2, 10, -0.5))
        elif frame == int((offset + 42.375 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 15, frame, 0.2, 10, -0.75))
        elif frame == int((offset + 42.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 15, frame, 0.2, 10, -1))
        elif frame == int((offset + 42.625 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 15, frame, 0.2, 10, -1.25))
        elif frame == int((offset + 42.75 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 15, frame, 0.2, 10, -1.5))
        elif frame == int((offset + 42.875 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 15, frame, 0.2, 10, -1.75))
        elif frame == int((offset + 44 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend([BulletC(0, 5, bulletImg[2], 15, frame, "0", "5 + t * 8", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(40, 5, bulletImg[2], 15, frame, "40", "5 + t * 8", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(80, 5, bulletImg[2], 15, frame, "80", "5 + t * 8", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(120, 5, bulletImg[2], 15, frame, "120", "5 + t * 8", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(160, 5, bulletImg[2], 15, frame, "160", "5 + t * 8", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(200, 5, bulletImg[2], 15, frame, "200", "5 + t * 8", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(240, 5, bulletImg[2], 15, frame, "240", "5 + t * 8", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(280, 5, bulletImg[2], 15, frame, "280", "5 + t * 8", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(320, 5, bulletImg[2], 15, frame, "320", "5 + t * 8", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(360, 5, bulletImg[2], 15, frame, "360", "5 + t * 8", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(400, 5, bulletImg[2], 15, frame, "400", "5 + t * 8", 80, 0, 0, 0, 0, 0, 0)
                        ])
        elif frame == int((offset + 45.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend([BulletC(20, 5, bulletImg[2], 15, frame, "20", "5 + t * 8", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(60, 5, bulletImg[2], 15, frame, "60", "5 + t * 8", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(100, 5, bulletImg[2], 15, frame, "100", "5 + t * 8", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(140, 5, bulletImg[2], 15, frame, "140", "5 + t * 8", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(180, 5, bulletImg[2], 15, frame, "180", "5 + t * 8", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(220, 5, bulletImg[2], 15, frame, "220", "5 + t * 8", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(260, 5, bulletImg[2], 15, frame, "260", "5 + t * 8", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(300, 5, bulletImg[2], 15, frame, "300", "5 + t * 8", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(340, 5, bulletImg[2], 15, frame, "340", "5 + t * 8", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(380, 5, bulletImg[2], 15, frame, "380", "5 + t * 8", 80, 0, 0, 0, 0, 0, 0)
                        ])
        elif frame == int((offset + 46.8 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend([BulletC(0, 5, bulletImg[2], 15, frame, "0", "5 + t * 8", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(40, 5, bulletImg[2], 15, frame, "40", "5 + t * 8", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(80, 5, bulletImg[2], 15, frame, "80", "5 + t * 8", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(120, 5, bulletImg[2], 15, frame, "120", "5 + t * 8", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(160, 5, bulletImg[2], 15, frame, "160", "5 + t * 8", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(200, 5, bulletImg[2], 15, frame, "200", "5 + t * 8", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(240, 5, bulletImg[2], 15, frame, "240", "5 + t * 8", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(280, 5, bulletImg[2], 15, frame, "280", "5 + t * 8", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(320, 5, bulletImg[2], 15, frame, "320", "5 + t * 8", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(360, 5, bulletImg[2], 15, frame, "360", "5 + t * 8", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(400, 5, bulletImg[2], 15, frame, "400", "5 + t * 8", 80, 0, 0, 0, 0, 0, 0)
                        ])
    elif int((offset + 47 * 60 / bpm * 1000) / (1000 / FPS)) <= frame < int(
            (offset + 75 * 60 / bpm * 1000) / (1000 / FPS)):
        if int((offset + 48 * 60 / bpm * 1000) / (1000 / FPS)) <= frame < int(
                (offset + 56 * 60 / bpm * 1000) / (1000 / FPS)) and frame % 10 == 0:
            now.extend([BulletC(random.randint(0, 400), 5, bulletImg[random.randint(0, 2)], 15, frame, "self.x",
                                "5 + t * 8", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(random.randint(0, 400), 5, bulletImg[random.randint(0, 2)], 15, frame, "self.x",
                                "5 + t * 8", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(random.randint(0, 400), 5, bulletImg[random.randint(0, 2)], 15, frame, "self.x",
                                "5 + t * 8", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(random.randint(0, 400), 5, bulletImg[random.randint(0, 2)], 15, frame, "self.x",
                                "5 + t * 8", 80, 0, 0, 0, 0, 0, 0)])
        elif int((offset + 56 * 60 / bpm * 1000) / (1000 / FPS)) <= frame < int(
                (offset + 59 * 60 / bpm * 1000) / (1000 / FPS)) and frame % 5 == 0:
            now.extend([BulletC(random.randint(0, 400), 5, bulletImg[random.randint(0, 2)], 15, frame, "self.x",
                                "5 + t * 8", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(random.randint(0, 400), 5, bulletImg[random.randint(0, 2)], 15, frame, "self.x",
                                "5 + t * 8", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(random.randint(0, 400), 5, bulletImg[random.randint(0, 2)], 15, frame, "self.x",
                                "5 + t * 8", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(random.randint(0, 400), 5, bulletImg[random.randint(0, 2)], 15, frame, "self.x",
                                "5 + t * 8", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(random.randint(0, 400), 5, bulletImg[random.randint(0, 2)], 15, frame, "self.x",
                                "5 + t * 8", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(random.randint(0, 400), 5, bulletImg[random.randint(0, 2)], 15, frame, "self.x",
                                "5 + t * 8", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(random.randint(0, 400), 5, bulletImg[random.randint(0, 2)], 15, frame, "self.x",
                                "5 + t * 8", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(random.randint(0, 400), 5, bulletImg[random.randint(0, 2)], 15, frame, "self.x",
                                "5 + t * 8", 80, 0, 0, 0, 0, 0, 0)])
        elif int((offset + 59 * 60 / bpm * 1000) / (1000 / FPS)) <= frame < int(
                (offset + 60.3 * 60 / bpm * 1000) / (1000 / FPS)) and frame % 3 == 0:
            now.extend([BulletC(random.randint(0, 400), 5, bulletImg[random.randint(0, 2)], 15, frame, "self.x",
                                "5 + t * 8", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(random.randint(0, 400), 5, bulletImg[random.randint(0, 2)], 15, frame, "self.x",
                                "5 + t * 8", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(random.randint(0, 400), 5, bulletImg[random.randint(0, 2)], 15, frame, "self.x",
                                "5 + t * 8", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(random.randint(0, 400), 5, bulletImg[random.randint(0, 2)], 15, frame, "self.x",
                                "5 + t * 8", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(random.randint(0, 400), 5, bulletImg[random.randint(0, 2)], 15, frame, "self.x",
                                "5 + t * 8", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(random.randint(0, 400), 5, bulletImg[random.randint(0, 2)], 15, frame, "self.x",
                                "5 + t * 8", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(random.randint(0, 400), 5, bulletImg[random.randint(0, 2)], 15, frame, "self.x",
                                "5 + t * 8", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(random.randint(0, 400), 5, bulletImg[random.randint(0, 2)], 15, frame, "self.x",
                                "5 + t * 8", 80, 0, 0, 0, 0, 0, 0)])
        elif frame == int((offset + 61.5 * 60 / bpm * 1000) / (1000 / FPS)):
            del now[:]
        elif frame == int((offset + 64 * 60 / bpm * 1000) / (1000 / FPS)):
            linearWarn.append(WarnX(0, warnImg[0], 25, frame, 8))
        elif frame == int((offset + 64.5 * 60 / bpm * 1000) / (1000 / FPS)):
            linearWarn.append(WarnX(100, warnImg[0], 25, frame, 8))
        elif frame == int((offset + 65 * 60 / bpm * 1000) / (1000 / FPS)):
            linearWarn.append(WarnX(200, warnImg[0], 25, frame, 8))
        elif frame == int((offset + 65.5 * 60 / bpm * 1000) / (1000 / FPS)):
            linearWarn.append(WarnX(300, warnImg[0], 25, frame, 8))
        elif frame == int((offset + 66 * 60 / bpm * 1000) / (1000 / FPS)):
            linearWarn.append(WarnX(25, warnImg[0], 25, frame, 8))
        elif frame == int((offset + 66.5 * 60 / bpm * 1000) / (1000 / FPS)):
            linearWarn.append(WarnX(125, warnImg[0], 25, frame, 8))
        elif frame == int((offset + 67 * 60 / bpm * 1000) / (1000 / FPS)):
            linearWarn.append(WarnX(225, warnImg[0], 25, frame, 8))
        elif frame == int((offset + 67.5 * 60 / bpm * 1000) / (1000 / FPS)):
            linearWarn.append(WarnX(325, warnImg[0], 25, frame, 8))
        elif frame == int((offset + 68 * 60 / bpm * 1000) / (1000 / FPS)):
            linearWarn.append(WarnX(50, warnImg[0], 25, frame, 8))
        elif frame == int((offset + 68.5 * 60 / bpm * 1000) / (1000 / FPS)):
            linearWarn.append(WarnX(150, warnImg[0], 25, frame, 8))
        elif frame == int((offset + 69 * 60 / bpm * 1000) / (1000 / FPS)):
            linearWarn.append(WarnX(250, warnImg[0], 25, frame, 8))
        elif frame == int((offset + 69.5 * 60 / bpm * 1000) / (1000 / FPS)):
            linearWarn.append(WarnX(350, warnImg[0], 25, frame, 8))
        elif frame == int((offset + 70 * 60 / bpm * 1000) / (1000 / FPS)):
            linearWarn.append(WarnX(75, warnImg[0], 25, frame, 8))
        elif frame == int((offset + 70.5 * 60 / bpm * 1000) / (1000 / FPS)):
            linearWarn.append(WarnX(175, warnImg[0], 25, frame, 8))
        elif frame == int((offset + 71 * 60 / bpm * 1000) / (1000 / FPS)):
            linearWarn.append(WarnX(275, warnImg[0], 25, frame, 8))
        elif frame == int((offset + 72 * 60 / bpm * 1000) / (1000 / FPS)):
            linearWarn.extend([WarnX(75, warnImg[0], 25, frame, 8),
                               WarnX(175, warnImg[0], 25, frame, 8),
                               WarnX(275, warnImg[0], 25, frame, 8)])
        elif frame == int((offset + 72.5 * 60 / bpm * 1000) / (1000 / FPS)):
            linearWarn.extend([WarnX(0, warnImg[0], 25, frame, 8),
                               WarnX(100, warnImg[0], 25, frame, 8),
                               WarnX(200, warnImg[0], 25, frame, 8),
                               WarnX(300, warnImg[0], 25, frame, 8)])
        elif frame == int((offset + 73 * 60 / bpm * 1000) / (1000 / FPS)):
            linearWarn.extend([WarnX(25, warnImg[0], 25, frame, 8),
                               WarnX(125, warnImg[0], 25, frame, 8),
                               WarnX(225, warnImg[0], 25, frame, 8),
                               WarnX(325, warnImg[0], 25, frame, 8)])
        elif frame == int((offset + 73.5 * 60 / bpm * 1000) / (1000 / FPS)):
            linearWarn.extend([WarnX(50, warnImg[0], 25, frame, 8),
                               WarnX(150, warnImg[0], 25, frame, 8),
                               WarnX(250, warnImg[0], 25, frame, 8),
                               WarnX(350, warnImg[0], 25, frame, 8)])
        elif frame == int((offset + 74 * 60 / bpm * 1000) / (1000 / FPS)):
            linearWarn.extend([WarnX(75, warnImg[0], 25, frame, 8),
                               WarnX(175, warnImg[0], 25, frame, 8),
                               WarnX(275, warnImg[0], 25, frame, 8)])
        elif frame == int((offset + 74.5 * 60 / bpm * 1000) / (1000 / FPS)):
            linearWarn.extend([WarnX(0, warnImg[0], 25, frame, 8),
                               WarnX(100, warnImg[0], 25, frame, 8),
                               WarnX(200, warnImg[0], 25, frame, 8),
                               WarnX(300, warnImg[0], 25, frame, 8)])
        elif frame == int((offset + 75 * 60 / bpm * 1000) / (1000 / FPS)):
            linear.append(DangerousX(0, lineImg[2], 375, frame, 4))
    elif int((offset + 75 * 60 / bpm * 1000) / (1000 / FPS)) <= frame < int(
            (offset + 100 * 60 / bpm * 1000) / (1000 / FPS)):
        if frame == int((offset + 75 * 60 / bpm * 1000) / (1000 / FPS)):
            linear.append(DangerousX(0, lineImg[2], 375, frame, 4))
        elif frame == int((offset + 75.5 * 60 / bpm * 1000) / (1000 / FPS)):
            linear.append(DangerousX(0, lineImg[2], 375, frame, 4))
        elif frame == int((offset + 76 * 60 / bpm * 1000) / (1000 / FPS)):
            linear.append(DangerousX(0, lineImg[2], 375, frame, 4))
        elif frame == int((offset + 76.5 * 60 / bpm * 1000) / (1000 / FPS)):
            linear.append(DangerousX(0, lineImg[2], 375, frame, 4))
        elif frame == int((offset + 77 * 60 / bpm * 1000) / (1000 / FPS)):
            linear.append(DangerousX(0, lineImg[2], 375, frame, 4))
        elif frame == int((offset + 77.5 * 60 / bpm * 1000) / (1000 / FPS)):
            linear.append(DangerousX(0, lineImg[2], 375, frame, 4))
        elif frame == int((offset + 78 * 60 / bpm * 1000) / (1000 / FPS)):
            linear.append(DangerousX(0, lineImg[2], 375, frame, 4))
        elif frame == int((offset + 78.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 79 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 79.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 80 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 80.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 81 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 81.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 82 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 82.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 83 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 83.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 84 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 84.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 85 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 85.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 86 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 86.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 87 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 87.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 88 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 88.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 89 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 89.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 90 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 90.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 91 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 91.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 92 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 92.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 93 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 93.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 94 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 94.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 95 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 95.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 96 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 96.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 97 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 97.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 98 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 98.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 99 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 99.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
    elif int((offset + 100 * 60 / bpm * 1000) / (1000 / FPS)) <= frame < int(
            (offset + 124.5 * 60 / bpm * 1000) / (1000 / FPS)):
        if frame == int((offset + 100 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 100.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 101 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 101.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 102 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 102.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 103 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 103.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 104 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 105.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[0], 15, frame, 0.05, 11, 0))
        elif frame == int((offset + 105.75 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 15, frame, 0.06, 11, 0.01))
        elif frame == int((offset + 106 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[2], 15, frame, 0.07, 11, 0.02))
        elif frame == int((offset + 106.25 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[0], 15, frame, 0.08, 11, 0.03))
        elif frame == int((offset + 106.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 15, frame, 0.09, 11, 0.04))
        elif frame == int((offset + 106.75 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[2], 15, frame, 0.08, 11, 0.05))
        elif frame == int((offset + 107 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[0], 15, frame, 0.07, 11, 0.06))
        elif frame == int((offset + 107.25 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 15, frame, 0.06, 11, 0.07))
        elif frame == int((offset + 107.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[2], 15, frame, 0.05, 11, 0))
        elif frame == int((offset + 107.75 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[0], 15, frame, 0.06, 11, 0.01))
        elif frame == int((offset + 108 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 15, frame, 0.07, 11, 0.02))
        elif frame == int((offset + 108.25 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[2], 15, frame, 0.08, 11, 0.03))
        elif frame == int((offset + 108.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[0], 15, frame, 0.09, 11, 0.04))
        elif frame == int((offset + 108.75 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 15, frame, 0.08, 11, 0.05))
        elif frame == int((offset + 109 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[2], 15, frame, 0.07, 11, 0.06))
        elif frame == int((offset + 109.25 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[0], 15, frame, 0.06, 11, 0.07))
        elif frame == int((offset + 109.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 109 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 110 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 110.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 111 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 111.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 112 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 112.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 113 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 113.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 114 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 114.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 115 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 115.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 116 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 116.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 117 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 117.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 118 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 118.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 119 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 119.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 120 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 120.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 121 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 121.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 122 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 122.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 123 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 123.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 124 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
    elif int((offset + 124.5 * 60 / bpm * 1000) / (1000 / FPS)) <= frame < int(
            (offset + 132.5 * 60 / bpm * 1000) / (1000 / FPS)):
        if frame == int((offset + 124.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 125 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 125.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 126 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 126.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 127 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 127.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 128 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 128.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 129 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 129.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 130 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 130.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 131 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 131.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 132 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
    elif int((offset + 132.5 * 60 / bpm * 1000) / (1000 / FPS)) <= frame < int(
            (offset + 149.5 * 60 / bpm * 1000) / (1000 / FPS)):
        if frame == int((offset + 132.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 133 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 133.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 134 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 134.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 135 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 135.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 136 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(
                CirclePattern(random.randint(0, 400), random.randint(0, 60), bulletImg[random.randint(0, 2)], 15, frame,
                              0.1, random.randint(3, 8), 0))
        elif frame == int((offset + 137.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[0], 15, frame, 0.05, 11, 0))
        elif frame == int((offset + 137.75 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 15, frame, 0.06, 11, 0.01))
        elif frame == int((offset + 138 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[2], 15, frame, 0.07, 11, 0.02))
        elif frame == int((offset + 138.25 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[0], 15, frame, 0.08, 11, 0.03))
        elif frame == int((offset + 138.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[0], 15, frame, 0.05, 11, 0))
        elif frame == int((offset + 138.75 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 15, frame, 0.06, 11, 0.01))
        elif frame == int((offset + 139 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[2], 15, frame, 0.07, 11, 0.02))
        elif frame == int((offset + 139.25 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[0], 15, frame, 0.08, 11, 0.03))
        elif frame == int((offset + 139.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 15, frame, 0.09, 11, 0.04))
        elif frame == int((offset + 139.75 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[2], 15, frame, 0.08, 11, 0.05))
        elif frame == int((offset + 140 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[0], 15, frame, 0.07, 11, 0.06))
        elif frame == int((offset + 140.25 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 15, frame, 0.06, 11, 0.07))
        elif frame == int((offset + 140.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[2], 15, frame, 0.05, 11, 0))
        elif frame == int((offset + 140.75 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[0], 15, frame, 0.06, 11, 0.01))
        elif frame == int((offset + 141 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 15, frame, 0.07, 11, 0.02))
        elif frame == int((offset + 141.25 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[2], 15, frame, 0.08, 11, 0.03))
        elif frame == int((offset + 141.5 * 60 / bpm * 1000) / (1000 / FPS)):
            linearWarn.extend([WarnX(0, warnImg[0], 25, frame, 86),
                               WarnX(350, warnImg[0], 25, frame, 86),
                               WarnX(200, warnImg[0], 25, frame, 86),
                               WarnX(50, warnImg[0], 25, frame, 86)])
        elif frame == int((offset + 142.1667 * 60 / bpm * 1000) / (1000 / FPS)):
            linearWarn.extend([WarnX(125, warnImg[0], 25, frame, 61),
                               WarnX(275, warnImg[0], 25, frame, 61),
                               WarnX(25, warnImg[0], 25, frame, 61),
                               WarnX(100, warnImg[0], 25, frame, 61)])
        elif frame == int((offset + 143 * 60 / bpm * 1000) / (1000 / FPS)):
            linearWarn.extend([WarnX(225, warnImg[0], 25, frame, 49),
                               WarnX(325, warnImg[0], 25, frame, 49),
                               WarnX(75, warnImg[0], 25, frame, 49),
                               WarnX(250, warnImg[0], 25, frame, 49)])
        elif frame == int((offset + 143.8333 * 60 / bpm * 1000) / (1000 / FPS)):
            linearWarn.extend([WarnX(150, warnImg[0], 25, frame, 36),
                               WarnX(300, warnImg[0], 25, frame, 36),
                               WarnX(375, warnImg[0], 25, frame, 36)])
        elif frame == int((offset + 145.5 * 60 / bpm * 1000) / (1000 / FPS)):
            linear.extend([DangerousX(0, lineImg[0], 25, frame, 8),
                           DangerousX(350, lineImg[0], 25, frame, 8),
                           DangerousX(200, lineImg[0], 25, frame, 8)])
        elif frame == int((offset + 145.8333 * 60 / bpm * 1000) / (1000 / FPS)):
            linear.extend([DangerousX(100, lineImg[0], 25, frame, 8),
                           DangerousX(250, lineImg[0], 25, frame, 8),
                           DangerousX(50, lineImg[0], 25, frame, 8)])
        elif frame == int((offset + 146.1666 * 60 / bpm * 1000) / (1000 / FPS)):
            linear.extend([DangerousX(125, lineImg[0], 25, frame, 8),
                           DangerousX(275, lineImg[0], 25, frame, 8),
                           DangerousX(25, lineImg[0], 25, frame, 8)])
        elif frame == int((offset + 146.5 * 60 / bpm * 1000) / (1000 / FPS)):
            linear.extend([DangerousX(225, lineImg[0], 25, frame, 8),
                           DangerousX(325, lineImg[0], 25, frame, 8),
                           DangerousX(75, lineImg[0], 25, frame, 8)])
        elif frame == int((offset + 146.8333 * 60 / bpm * 1000) / (1000 / FPS)):
            linear.extend([DangerousX(150, lineImg[0], 25, frame, 8),
                           DangerousX(300, lineImg[0], 25, frame, 8),
                           DangerousX(375, lineImg[0], 25, frame, 8)])
        elif frame == int((offset + 147.1666 * 60 / bpm * 1000) / (1000 / FPS)):
            linear.extend([DangerousX(0, lineImg[0], 25, frame, 8),
                           DangerousX(350, lineImg[0], 25, frame, 8),
                           DangerousX(200, lineImg[0], 25, frame, 8)])
        elif frame == int((offset + 147.5 * 60 / bpm * 1000) / (1000 / FPS)):
            linear.extend([DangerousX(100, lineImg[0], 25, frame, 8),
                           DangerousX(250, lineImg[0], 25, frame, 8),
                           DangerousX(50, lineImg[0], 25, frame, 8)])
        elif frame == int((offset + 147.8333 * 60 / bpm * 1000) / (1000 / FPS)):
            linear.extend([DangerousX(125, lineImg[0], 25, frame, 8),
                           DangerousX(275, lineImg[0], 25, frame, 8),
                           DangerousX(25, lineImg[0], 25, frame, 8)])
        elif frame == int((offset + 148.1666 * 60 / bpm * 1000) / (1000 / FPS)):
            linear.extend([DangerousX(225, lineImg[0], 25, frame, 8),
                           DangerousX(325, lineImg[0], 25, frame, 8),
                           DangerousX(75, lineImg[0], 25, frame, 8)])
        elif frame == int((offset + 148.5 * 60 / bpm * 1000) / (1000 / FPS)):
            linear.extend([DangerousX(150, lineImg[0], 25, frame, 8),
                           DangerousX(300, lineImg[0], 25, frame, 8),
                           DangerousX(375, lineImg[0], 25, frame, 8)])
        elif frame == int((offset + 148.8333 * 60 / bpm * 1000) / (1000 / FPS)):
            linear.extend([DangerousX(225, lineImg[0], 25, frame, 8),
                           DangerousX(325, lineImg[0], 25, frame, 8),
                           DangerousX(75, lineImg[0], 25, frame, 8)])
        elif frame == int((offset + 149.1666 * 60 / bpm * 1000) / (1000 / FPS)):
            linear.extend([DangerousX(150, lineImg[0], 25, frame, 8),
                           DangerousX(300, lineImg[0], 25, frame, 8),
                           DangerousX(375, lineImg[0], 25, frame, 8)])
    elif int((offset + 149.5 * 60 / bpm * 1000) / (1000 / FPS)) <= frame < int(
            (offset + 160 * 60 / bpm * 1000) / (1000 / FPS)):
        if frame == int((offset + 149.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 50, bulletImg[0], 15, frame, 0.2, 8, 0))
        elif frame == int((offset + 149.625 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 50, bulletImg[1], 15, frame, 0.2, 8, 0.02))
        elif frame == int((offset + 149.75 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 50, bulletImg[2], 15, frame, 0.2, 8, 0.04))
        elif frame == int((offset + 149.875 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 50, bulletImg[0], 15, frame, 0.2, 8, 0.06))
        elif frame == int((offset + 150 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 50, bulletImg[1], 15, frame, 0.2, 8, 0.08))
        elif frame == int((offset + 150.125 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 50, bulletImg[2], 15, frame, 0.2, 8, 0.1))
        elif frame == int((offset + 150.25 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 50, bulletImg[0], 15, frame, 0.2, 8, 0.12))
        elif frame == int((offset + 150.375 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 50, bulletImg[1], 15, frame, 0.2, 8, 0.14))
        elif frame == int((offset + 150.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 50, bulletImg[2], 15, frame, 0.2, 8, 0.16))
        elif frame == int((offset + 151 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(5, 5, bulletImg[0], 15, frame, 0.05, 7, 0))
        elif frame == int((offset + 151.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(5, 5, bulletImg[0], 15, frame, 0.05, 7, 0))
        elif frame == int((offset + 152 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(395, 5, bulletImg[0], 15, frame, 0.05, 7, 0))
        elif frame == int((offset + 152.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(395, 5, bulletImg[0], 15, frame, 0.05, 7, 0))
        elif frame == int((offset + 153 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(5, 5, bulletImg[1], 15, frame, 0.05, 7, 0))
        elif frame == int((offset + 153.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(5, 5, bulletImg[1], 15, frame, 0.05, 7, 0))
        elif frame == int((offset + 154 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(395, 5, bulletImg[1], 15, frame, 0.05, 7, 0))
        elif frame == int((offset + 154.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(395, 5, bulletImg[1], 15, frame, 0.05, 7, 0))
        elif frame == int((offset + 155 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend([BulletC(0, 5, bulletImg[2], 15, frame, "0", "5 + t * 8", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(40, 5, bulletImg[2], 15, frame, "40", "5 + t * 8", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(80, 5, bulletImg[2], 15, frame, "80", "5 + t * 8", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(120, 5, bulletImg[2], 15, frame, "120", "5 + t * 8", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(160, 5, bulletImg[2], 15, frame, "160", "5 + t * 8", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(200, 5, bulletImg[2], 15, frame, "200", "5 + t * 8", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(240, 5, bulletImg[2], 15, frame, "240", "5 + t * 8", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(280, 5, bulletImg[2], 15, frame, "280", "5 + t * 8", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(320, 5, bulletImg[2], 15, frame, "320", "5 + t * 8", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(360, 5, bulletImg[2], 15, frame, "360", "5 + t * 8", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(400, 5, bulletImg[2], 15, frame, "400", "5 + t * 8", 80, 0, 0, 0, 0, 0, 0)
                        ])
        elif frame == int((offset + 155.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend([BulletC(20, 5, bulletImg[2], 15, frame, "20", "5 + t * 8", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(60, 5, bulletImg[2], 15, frame, "60", "5 + t * 8", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(100, 5, bulletImg[2], 15, frame, "100", "5 + t * 8", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(140, 5, bulletImg[2], 15, frame, "140", "5 + t * 8", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(180, 5, bulletImg[2], 15, frame, "180", "5 + t * 8", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(220, 5, bulletImg[2], 15, frame, "220", "5 + t * 8", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(260, 5, bulletImg[2], 15, frame, "260", "5 + t * 8", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(300, 5, bulletImg[2], 15, frame, "300", "5 + t * 8", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(340, 5, bulletImg[2], 15, frame, "340", "5 + t * 8", 80, 0, 0, 0, 0, 0, 0),
                        BulletC(380, 5, bulletImg[2], 15, frame, "380", "5 + t * 8", 80, 0, 0, 0, 0, 0, 0)
                        ])
        elif frame == int((offset + 156 * 60 / bpm * 1000) / (1000 / FPS)):
            for i in range(0, 425, 25):
                now.append(BulletC(i, 5, bulletImg[1], 15, frame,
                                   str(i) + " + 9.5 * (" + str(playerX) + " - " + str(i) + ") / math.sqrt((" + str(i) +
                                   " - " + str(playerX) + ") ** 2 + (5 - " + str(playerY) + ") ** 2) * t",
                                   "5 + 9.5 * (" + str(playerY) + " - 5) / math.sqrt((" + str(i) + " - " + str(
                                       playerX) +
                                   ") ** 2 + (5 - " + str(playerY) + ") ** 2) * t", 100, 0, 0, 0, 0, 0, 0))
        elif frame == int((offset + 157 * 60 / bpm * 1000) / (1000 / FPS)):
            for i in range(0, 425, 25):
                now.append(BulletC(i, 5, bulletImg[0], 15, frame,
                                   str(i) + " + 9.5 * (" + str(playerX) + " - " + str(i) + ") / math.sqrt((" + str(i) +
                                   " - " + str(playerX) + ") ** 2 + (5 - " + str(playerY) + ") ** 2) * t",
                                   "5 + 9.5 * (" + str(playerY) + " - 5) / math.sqrt((" + str(i) + " - " + str(
                                       playerX) +
                                   ") ** 2 + (5 - " + str(playerY) + ") ** 2) * t", 100, 0, 0, 0, 0, 0, 0))
        elif frame == int((offset + 158 * 60 / bpm * 1000) / (1000 / FPS)):
            p = [-1, 1]
            now.extend([BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(400, 415)) + " - 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(400, 415)) + " - 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(400, 415)) + " - 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(400, 415)) + " - 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0)
                        ])
        elif frame == int((offset + 158.5 * 60 / bpm * 1000) / (1000 / FPS)):
            p = [-1, 1]
            now.extend([BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(400, 415)) + " - 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(400, 415)) + " - 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(400, 415)) + " - 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(400, 415)) + " - 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0)
                        ])
        elif frame == int((offset + 159 * 60 / bpm * 1000) / (1000 / FPS)):
            p = [-1, 1]
            now.extend([BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(400, 415)) + " - 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(400, 415)) + " - 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(400, 415)) + " - 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(400, 415)) + " - 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0)
                        ])
        elif frame == int((offset + 159.5 * 60 / bpm * 1000) / (1000 / FPS)):
            p = [-1, 1]
            now.extend([BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(400, 415)) + " - 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(400, 415)) + " - 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(400, 415)) + " - 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(400, 415)) + " - 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0)
                        ])
    elif int((offset + 160 * 60 / bpm * 1000) / (1000 / FPS)) <= frame < int(
            (offset + 168 * 60 / bpm * 1000) / (1000 / FPS)):
        if frame == int((offset + 160 * 60 / bpm * 1000) / (1000 / FPS)):
            p = [-1, 1]
            now.extend([BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(400, 415)) + " - 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(400, 415)) + " - 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(400, 415)) + " - 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(400, 415)) + " - 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0)
                        ])
        elif frame == int((offset + 160.25 * 60 / bpm * 1000) / (1000 / FPS)):
            p = [-1, 1]
            now.extend([BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(400, 415)) + " - 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(400, 415)) + " - 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(400, 415)) + " - 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(400, 415)) + " - 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0)
                        ])
        elif frame == int((offset + 160.5 * 60 / bpm * 1000) / (1000 / FPS)):
            p = [-1, 1]
            now.extend([BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(400, 415)) + " - 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(400, 415)) + " - 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(400, 415)) + " - 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(400, 415)) + " - 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0)
                        ])
        elif frame == int((offset + 160.75 * 60 / bpm * 1000) / (1000 / FPS)):
            p = [-1, 1]
            now.extend([BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(400, 415)) + " - 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(400, 415)) + " - 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(400, 415)) + " - 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(400, 415)) + " - 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0)
                        ])
        elif frame == int((offset + 161 * 60 / bpm * 1000) / (1000 / FPS)):
            for i in range(0, 425, 25):
                now.append(BulletC(i, 5, bulletImg[1], 15, frame,
                                   str(i) + " + 9.5 * (" + str(playerX) + " - " + str(i) + ") / math.sqrt((" + str(i) +
                                   " - " + str(playerX) + ") ** 2 + (5 - " + str(playerY) + ") ** 2) * t",
                                   "5 + 9.5 * (" + str(playerY) + " - 5) / math.sqrt((" + str(i) + " - " + str(
                                       playerX) +
                                   ") ** 2 + (5 - " + str(playerY) + ") ** 2) * t", 100, 0, 0, 0, 0, 0, 0))
        elif frame == int((offset + 162 * 60 / bpm * 1000) / (1000 / FPS)):
            for i in range(0, 425, 25):
                now.append(BulletC(i, 5, bulletImg[0], 15, frame,
                                   str(i) + " + 9.5 * (" + str(playerX) + " - " + str(i) + ") / math.sqrt((" + str(i) +
                                   " - " + str(playerX) + ") ** 2 + (5 - " + str(playerY) + ") ** 2) * t",
                                   "5 + 9.5 * (" + str(playerY) + " - 5) / math.sqrt((" + str(i) + " - " + str(
                                       playerX) +
                                   ") ** 2 + (5 - " + str(playerY) + ") ** 2) * t", 100, 0, 0, 0, 0, 0, 0))
        elif frame == int((offset + 163 * 60 / bpm * 1000) / (1000 / FPS)):
            p = [-1, 1]
            now.extend([BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(400, 415)) + " - 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(400, 415)) + " - 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(400, 415)) + " - 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(400, 415)) + " - 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0)
                        ])
        elif frame == int((offset + 163.25 * 60 / bpm * 1000) / (1000 / FPS)):
            p = [-1, 1]
            now.extend([BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(400, 415)) + " - 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(400, 415)) + " - 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(400, 415)) + " - 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(400, 415)) + " - 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0)
                        ])
        elif frame == int((offset + 163.5 * 60 / bpm * 1000) / (1000 / FPS)):
            p = [-1, 1]
            now.extend([BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(400, 415)) + " - 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(400, 415)) + " - 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(400, 415)) + " - 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(400, 415)) + " - 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0)
                        ])
        elif frame == int((offset + 163.75 * 60 / bpm * 1000) / (1000 / FPS)):
            p = [-1, 1]
            now.extend([BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(400, 415)) + " - 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(400, 415)) + " - 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(400, 415)) + " - 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(400, 415)) + " - 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0)
                        ])
        elif frame == int((offset + 164 * 60 / bpm * 1000) / (1000 / FPS)):
            p = [-1, 1]
            now.extend([BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(400, 415)) + " - 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(400, 415)) + " - 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(400, 415)) + " - 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(400, 415)) + " - 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0)
                        ])
        elif frame == int((offset + 164.25 * 60 / bpm * 1000) / (1000 / FPS)):
            p = [-1, 1]
            now.extend([BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(400, 415)) + " - 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(400, 415)) + " - 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(400, 415)) + " - 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(400, 415)) + " - 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0)
                        ])
        elif frame == int((offset + 164.5 * 60 / bpm * 1000) / (1000 / FPS)):
            p = [-1, 1]
            now.extend([BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(400, 415)) + " - 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(400, 415)) + " - 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(400, 415)) + " - 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(400, 415)) + " - 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0)
                        ])
        elif frame == int((offset + 164.75 * 60 / bpm * 1000) / (1000 / FPS)):
            p = [-1, 1]
            now.extend([BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(100, 300)) + " + 4 * t * " + str(
                                    random.uniform(0.3, 0.5) * p[random.randint(0, 1)]),
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(random.uniform(0.8, 1)), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(-15, 0)) + " + 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(400, 415)) + " - 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(400, 415)) + " - 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(400, 415)) + " - 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0),
                        BulletC(-15, -15, bulletImg[random.randint(1, 2)], 15, frame,
                                str(random.randint(400, 415)) + " - 4 * t * " + str(
                                    random.uniform(0.8, 0.1)),
                                str(random.randint(150, 350)) + " + 4 * t * " + str(
                                    random.uniform(0.4, 0.7) * p[random.randint(0, 1)]), 100, 0, 0, 0,
                                0, 0, 0)
                        ])
        elif frame == int((offset + 165 * 60 / bpm * 1000) / (1000 / FPS)):
            for i in range(0, 425, 25):
                now.append(BulletC(i, 5, bulletImg[1], 15, frame,
                                   str(i) + " + 9.5 * (" + str(playerX) + " - " + str(i) + ") / math.sqrt((" + str(i) +
                                   " - " + str(playerX) + ") ** 2 + (5 - " + str(playerY) + ") ** 2) * t",
                                   "5 + 9.5 * (" + str(playerY) + " - 5) / math.sqrt((" + str(i) + " - " + str(
                                       playerX) +
                                   ") ** 2 + (5 - " + str(playerY) + ") ** 2) * t", 100, 0, 0, 0, 0, 0, 0))
        elif frame == int((offset + 166 * 60 / bpm * 1000) / (1000 / FPS)):
            for i in range(0, 425, 25):
                now.append(BulletC(i, 5, bulletImg[0], 15, frame,
                                   str(i) + " + 9.5 * (" + str(playerX) + " - " + str(i) + ") / math.sqrt((" + str(i) +
                                   " - " + str(playerX) + ") ** 2 + (5 - " + str(playerY) + ") ** 2) * t",
                                   "5 + 9.5 * (" + str(playerY) + " - 5) / math.sqrt((" + str(i) + " - " + str(
                                       playerX) +
                                   ") ** 2 + (5 - " + str(playerY) + ") ** 2) * t", 100, 0, 0, 0, 0, 0, 0))
        elif frame == int((offset + 167 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend([BulletC(400, 0, bulletImg[0], 15, frame, "400", "10 * t", 70, 0, 0, 0, 0, 0, 0),
                        BulletC(200, 0, bulletImg[0], 15, frame, "200", "10 * t", 70, 0, 0, 0, 0, 0, 0)])
        elif frame == int((offset + 167.125 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend([BulletC(375, 0, bulletImg[0], 15, frame, "375", "10 * t", 70, 0, 0, 0, 0, 0, 0),
                        BulletC(175, 0, bulletImg[0], 15, frame, "175", "10 * t", 70, 0, 0, 0, 0, 0, 0)])
        elif frame == int((offset + 167.25 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend([BulletC(350, 0, bulletImg[0], 15, frame, "350", "10 * t", 70, 0, 0, 0, 0, 0, 0),
                        BulletC(150, 0, bulletImg[0], 15, frame, "150", "10 * t", 70, 0, 0, 0, 0, 0, 0)])
        elif frame == int((offset + 167.375 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend([BulletC(325, 0, bulletImg[0], 15, frame, "325", "10 * t", 70, 0, 0, 0, 0, 0, 0),
                        BulletC(125, 0, bulletImg[0], 15, frame, "125", "10 * t", 70, 0, 0, 0, 0, 0, 0)])
        elif frame == int((offset + 167.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend([BulletC(300, 0, bulletImg[0], 15, frame, "300", "10 * t", 70, 0, 0, 0, 0, 0, 0),
                        BulletC(100, 0, bulletImg[0], 15, frame, "100", "10 * t", 70, 0, 0, 0, 0, 0, 0)])
        elif frame == int((offset + 167.625 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend([BulletC(275, 0, bulletImg[0], 15, frame, "275", "10 * t", 70, 0, 0, 0, 0, 0, 0),
                        BulletC(75, 0, bulletImg[0], 15, frame, "75", "10 * t", 70, 0, 0, 0, 0, 0, 0)])
        elif frame == int((offset + 167.75 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend([BulletC(250, 0, bulletImg[0], 15, frame, "250", "10 * t", 70, 0, 0, 0, 0, 0, 0),
                        BulletC(50, 0, bulletImg[0], 15, frame, "50", "10 * t", 70, 0, 0, 0, 0, 0, 0)])
        elif frame == int((offset + 167.875 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend([BulletC(225, 0, bulletImg[0], 15, frame, "225", "10 * t", 70, 0, 0, 0, 0, 0, 0),
                        BulletC(25, 0, bulletImg[0], 15, frame, "25", "10 * t", 70, 0, 0, 0, 0, 0, 0)])
        elif frame == int((offset + 168 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend([BulletC(212.5, 0, bulletImg[0], 15, frame, "212.5", "10 * t", 70, 0, 0, 0, 0, 0, 0),
                        BulletC(12.5, 0, bulletImg[0], 15, frame, "12.5", "10 * t", 70, 0, 0, 0, 0, 0, 0)])
    elif int((offset + 168 * 60 / bpm * 1000) / (1000 / FPS)) <= frame < int(
            (offset + 171 * 60 / bpm * 1000) / (1000 / FPS)):
        if frame == int((offset + 168.125 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend([BulletC(237.5, 0, bulletImg[0], 15, frame, "237.5", "10 * t", 70, 0, 0, 0, 0, 0, 0),
                        BulletC(37.5, 0, bulletImg[0], 15, frame, "37.5", "10 * t", 70, 0, 0, 0, 0, 0, 0)])
        elif frame == int((offset + 168.25 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend([BulletC(262.5, 0, bulletImg[0], 15, frame, "262.5", "10 * t", 70, 0, 0, 0, 0, 0, 0),
                        BulletC(62.5, 0, bulletImg[0], 15, frame, "62.5", "10 * t", 70, 0, 0, 0, 0, 0, 0)])
        elif frame == int((offset + 168.375 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend([BulletC(287.5, 0, bulletImg[0], 15, frame, "287.5", "10 * t", 70, 0, 0, 0, 0, 0, 0),
                        BulletC(87.5, 0, bulletImg[0], 15, frame, "87.5", "10 * t", 70, 0, 0, 0, 0, 0, 0)])
        elif frame == int((offset + 168.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend([BulletC(312.5, 0, bulletImg[0], 15, frame, "312.5", "10 * t", 70, 0, 0, 0, 0, 0, 0),
                        BulletC(112.5, 0, bulletImg[0], 15, frame, "112.5", "10 * t", 70, 0, 0, 0, 0, 0, 0)])
        elif frame == int((offset + 168.625 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend([BulletC(337.5, 0, bulletImg[0], 15, frame, "337.5", "10 * t", 70, 0, 0, 0, 0, 0, 0),
                        BulletC(137.5, 0, bulletImg[0], 15, frame, "137.5", "10 * t", 70, 0, 0, 0, 0, 0, 0)])
        elif frame == int((offset + 168.75 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend([BulletC(362.5, 0, bulletImg[0], 15, frame, "362.5", "10 * t", 70, 0, 0, 0, 0, 0, 0),
                        BulletC(162.5, 0, bulletImg[0], 15, frame, "162.5", "10 * t", 70, 0, 0, 0, 0, 0, 0)])
        elif frame == int((offset + 168.875 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend([BulletC(387.5, 0, bulletImg[0], 15, frame, "387.5", "10 * t", 70, 0, 0, 0, 0, 0, 0),
                        BulletC(187.5, 0, bulletImg[0], 15, frame, "187.5", "10 * t", 70, 0, 0, 0, 0, 0, 0)])
        elif frame == int((offset + 169 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend([BulletC(400, 0, bulletImg[0], 15, frame, "400", "10 * t", 70, 0, 0, 0, 0, 0, 0),
                        BulletC(200, 0, bulletImg[0], 15, frame, "200", "10 * t", 70, 0, 0, 0, 0, 0, 0)])
        elif frame == int((offset + 169.125 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend([BulletC(375, 0, bulletImg[0], 15, frame, "375", "10 * t", 70, 0, 0, 0, 0, 0, 0),
                        BulletC(175, 0, bulletImg[0], 15, frame, "175", "10 * t", 70, 0, 0, 0, 0, 0, 0)])
        elif frame == int((offset + 169.25 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend([BulletC(350, 0, bulletImg[0], 15, frame, "350", "10 * t", 70, 0, 0, 0, 0, 0, 0),
                        BulletC(150, 0, bulletImg[0], 15, frame, "150", "10 * t", 70, 0, 0, 0, 0, 0, 0)])
        elif frame == int((offset + 169.375 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend([BulletC(325, 0, bulletImg[0], 15, frame, "325", "10 * t", 70, 0, 0, 0, 0, 0, 0),
                        BulletC(125, 0, bulletImg[0], 15, frame, "125", "10 * t", 70, 0, 0, 0, 0, 0, 0)])
        elif frame == int((offset + 169.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend([BulletC(300, 0, bulletImg[0], 15, frame, "300", "10 * t", 70, 0, 0, 0, 0, 0, 0),
                        BulletC(100, 0, bulletImg[0], 15, frame, "100", "10 * t", 70, 0, 0, 0, 0, 0, 0)])
        elif frame == int((offset + 169.625 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend([BulletC(275, 0, bulletImg[0], 15, frame, "275", "10 * t", 70, 0, 0, 0, 0, 0, 0),
                        BulletC(75, 0, bulletImg[0], 15, frame, "75", "10 * t", 70, 0, 0, 0, 0, 0, 0)])
        elif frame == int((offset + 169.75 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend([BulletC(250, 0, bulletImg[0], 15, frame, "250", "10 * t", 70, 0, 0, 0, 0, 0, 0),
                        BulletC(50, 0, bulletImg[0], 15, frame, "50", "10 * t", 70, 0, 0, 0, 0, 0, 0)])
        elif frame == int((offset + 169.875 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend([BulletC(225, 0, bulletImg[0], 15, frame, "225", "10 * t", 70, 0, 0, 0, 0, 0, 0),
                        BulletC(25, 0, bulletImg[0], 15, frame, "25", "10 * t", 70, 0, 0, 0, 0, 0, 0)])
        elif frame == int((offset + 170 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[3], 15, frame, 0.08, 10, 0))
        elif frame == int((offset + 170.125 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[3], 15, frame, 0.08, 10, 0.01))
        elif frame == int((offset + 170.25 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[3], 15, frame, 0.08, 10, 0.02))
        elif frame == int((offset + 170.375 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[3], 15, frame, 0.08, 10, 0.03))
        elif frame == int((offset + 170.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[3], 15, frame, 0.08, 10, 0.04))
        elif frame == int((offset + 170.625 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[3], 15, frame, 0.08, 10, 0.05))
        elif frame == int((offset + 170.75 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[3], 15, frame, 0.08, 10, 0.06))
        elif frame == int((offset + 170.875 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[3], 15, frame, 0.08, 10, 0.07))
    elif int((offset + 171 * 60 / bpm * 1000) / (1000 / FPS)) <= frame < int(
            (offset + 179 * 60 / bpm * 1000) / (1000 / FPS)):
        if frame == int((offset + 171 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[0], 15, frame, 0.05, 12, 0))
        elif frame == int((offset + 171.125 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[0], 15, frame, 0.05, 12, 0.005))
        elif frame == int((offset + 171.25 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[0], 15, frame, 0.05, 12, 0.01))
        elif frame == int((offset + 171.375 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[0], 15, frame, 0.05, 12, 0.015))
        elif frame == int((offset + 171.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[0], 15, frame, 0.05, 12, 0.02))
        elif frame == int((offset + 171.625 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[0], 15, frame, 0.05, 12, 0.025))
        elif frame == int((offset + 171.75 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[0], 15, frame, 0.05, 12, 0.03))
        elif frame == int((offset + 171.875 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[0], 15, frame, 0.05, 12, 0.035))
        elif frame == int((offset + 172 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(350, 5, bulletImg[1], 15, frame, 0.07, 5, 0))
        elif frame == int((offset + 172.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(325, 5, bulletImg[1], 15, frame, 0.07, 5, 0))
        elif frame == int((offset + 172.95 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(300, 5, bulletImg[1], 15, frame, 0.07, 5, 0))
        elif frame == int((offset + 173.35 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(275, 5, bulletImg[1], 15, frame, 0.07, 5, 0))
        elif frame == int((offset + 173.7 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(250, 5, bulletImg[1], 15, frame, 0.07, 5, 0))
        elif frame == int((offset + 174 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(225, 5, bulletImg[1], 15, frame, 0.07, 5, 0))
        elif frame == int((offset + 174.25 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 15, frame, 0.07, 5, 0))
        elif frame == int((offset + 174.45 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(175, 5, bulletImg[1], 15, frame, 0.07, 5, 0))
        elif frame == int((offset + 174.6 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(150, 5, bulletImg[1], 15, frame, 0.07, 5, 0))
        elif frame == int((offset + 174.7 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(125, 5, bulletImg[1], 15, frame, 0.07, 5, 0))
        elif frame == int((offset + 174.8 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(90, 5, bulletImg[1], 15, frame, 0.07, 5, 0))
        elif frame == int((offset + 174.9 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(45, 5, bulletImg[1], 15, frame, 0.07, 5, 0))
        elif frame == int((offset + 175 * 60 / bpm * 1000) / (1000 / FPS)):
            now.append(LinearPattern(25, 0, bulletImg[2], 15, frame, 0.5, 8))
        elif frame == int((offset + 175.125 * 60 / bpm * 1000) / (1000 / FPS)):
            now.append(LinearPattern(75, 0, bulletImg[2], 15, frame, 0.5, 8))
        elif frame == int((offset + 175.25 * 60 / bpm * 1000) / (1000 / FPS)):
            now.append(LinearPattern(125, 0, bulletImg[2], 15, frame, 0.5, 8))
        elif frame == int((offset + 175.375 * 60 / bpm * 1000) / (1000 / FPS)):
            now.append(LinearPattern(175, 0, bulletImg[2], 15, frame, 0.5, 8))
        elif frame == int((offset + 175.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.append(LinearPattern(225, 0, bulletImg[2], 15, frame, 0.5, 8))
        elif frame == int((offset + 175.625 * 60 / bpm * 1000) / (1000 / FPS)):
            now.append(LinearPattern(275, 0, bulletImg[2], 15, frame, 0.5, 8))
        elif frame == int((offset + 175.75 * 60 / bpm * 1000) / (1000 / FPS)):
            now.append(LinearPattern(325, 0, bulletImg[2], 15, frame, 0.5, 8))
        elif frame == int((offset + 175.875 * 60 / bpm * 1000) / (1000 / FPS)):
            now.append(LinearPattern(375, 0, bulletImg[2], 15, frame, 0.5, 8))
        elif frame == int((offset + 176 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(50, 5, bulletImg[1], 15, frame, 0.07, 5, 0))
        elif frame == int((offset + 176.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(75, 5, bulletImg[1], 15, frame, 0.07, 5, 0))
        elif frame == int((offset + 176.95 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(100, 5, bulletImg[1], 15, frame, 0.07, 5, 0))
        elif frame == int((offset + 177.35 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(125, 5, bulletImg[1], 15, frame, 0.07, 5, 0))
        elif frame == int((offset + 177.7 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(150, 5, bulletImg[1], 15, frame, 0.07, 5, 0))
        elif frame == int((offset + 178 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(175, 5, bulletImg[1], 15, frame, 0.07, 5, 0))
        elif frame == int((offset + 178.25 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 15, frame, 0.07, 5, 0))
        elif frame == int((offset + 178.45 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(225, 5, bulletImg[1], 15, frame, 0.07, 5, 0))
        elif frame == int((offset + 178.6 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(250, 5, bulletImg[1], 15, frame, 0.07, 5, 0))
        elif frame == int((offset + 178.7 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(275, 5, bulletImg[1], 15, frame, 0.07, 5, 0))
        elif frame == int((offset + 178.8 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(310, 5, bulletImg[1], 15, frame, 0.07, 5, 0))
        elif frame == int((offset + 178.9 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(355, 5, bulletImg[1], 15, frame, 0.07, 5, 0))
    elif int((offset + 179 * 60 / bpm * 1000) / (1000 / FPS)) <= frame < int(
            (offset + 187 * 60 / bpm * 1000) / (1000 / FPS)):
        if frame == int((offset + 179 * 60 / bpm * 1000) / (1000 / FPS)):
            now.append(LinearPattern(375, 0, bulletImg[2], 15, frame, 0.5, 8))
        elif frame == int((offset + 179.125 * 60 / bpm * 1000) / (1000 / FPS)):
            now.append(LinearPattern(325, 0, bulletImg[2], 15, frame, 0.5, 8))
        elif frame == int((offset + 179.25 * 60 / bpm * 1000) / (1000 / FPS)):
            now.append(LinearPattern(275, 0, bulletImg[2], 15, frame, 0.5, 8))
        elif frame == int((offset + 179.375 * 60 / bpm * 1000) / (1000 / FPS)):
            now.append(LinearPattern(225, 0, bulletImg[2], 15, frame, 0.5, 8))
        elif frame == int((offset + 179.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.append(LinearPattern(175, 0, bulletImg[2], 15, frame, 0.5, 8))
        elif frame == int((offset + 179.625 * 60 / bpm * 1000) / (1000 / FPS)):
            now.append(LinearPattern(125, 0, bulletImg[2], 15, frame, 0.5, 8))
        elif frame == int((offset + 179.75 * 60 / bpm * 1000) / (1000 / FPS)):
            now.append(LinearPattern(75, 0, bulletImg[2], 15, frame, 0.5, 8))
        elif frame == int((offset + 179.875 * 60 / bpm * 1000) / (1000 / FPS)):
            now.append(LinearPattern(25, 0, bulletImg[2], 15, frame, 0.5, 8))
        elif frame == int((offset + 180 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(350, 5, bulletImg[1], 15, frame, 0.07, 5, 0))
        elif frame == int((offset + 180.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(325, 5, bulletImg[1], 15, frame, 0.07, 5, 0))
        elif frame == int((offset + 180.95 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(300, 5, bulletImg[1], 15, frame, 0.07, 5, 0))
        elif frame == int((offset + 181.35 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(275, 5, bulletImg[1], 15, frame, 0.07, 5, 0))
        elif frame == int((offset + 181.7 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(250, 5, bulletImg[1], 15, frame, 0.07, 5, 0))
        elif frame == int((offset + 182 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(225, 5, bulletImg[1], 15, frame, 0.07, 5, 0))
        elif frame == int((offset + 182.25 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 15, frame, 0.07, 5, 0))
        elif frame == int((offset + 182.45 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(175, 5, bulletImg[1], 15, frame, 0.07, 5, 0))
        elif frame == int((offset + 182.6 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(150, 5, bulletImg[1], 15, frame, 0.07, 5, 0))
        elif frame == int((offset + 182.7 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(125, 5, bulletImg[1], 15, frame, 0.07, 5, 0))
        elif frame == int((offset + 182.8 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(90, 5, bulletImg[1], 15, frame, 0.07, 5, 0))
        elif frame == int((offset + 182.9 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(45, 5, bulletImg[1], 15, frame, 0.07, 5, 0))
        elif frame == int((offset + 183 * 60 / bpm * 1000) / (1000 / FPS)):
            now.append(LinearPattern(25, 0, bulletImg[2], 15, frame, 0.5, 8))
        elif frame == int((offset + 183.125 * 60 / bpm * 1000) / (1000 / FPS)):
            now.append(LinearPattern(75, 0, bulletImg[2], 15, frame, 0.5, 8))
        elif frame == int((offset + 183.25 * 60 / bpm * 1000) / (1000 / FPS)):
            now.append(LinearPattern(125, 0, bulletImg[2], 15, frame, 0.5, 8))
        elif frame == int((offset + 183.375 * 60 / bpm * 1000) / (1000 / FPS)):
            now.append(LinearPattern(175, 0, bulletImg[2], 15, frame, 0.5, 8))
        elif frame == int((offset + 183.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.append(LinearPattern(225, 0, bulletImg[2], 15, frame, 0.5, 8))
        elif frame == int((offset + 183.625 * 60 / bpm * 1000) / (1000 / FPS)):
            now.append(LinearPattern(275, 0, bulletImg[2], 15, frame, 0.5, 8))
        elif frame == int((offset + 183.75 * 60 / bpm * 1000) / (1000 / FPS)):
            now.append(LinearPattern(325, 0, bulletImg[2], 15, frame, 0.5, 8))
        elif frame == int((offset + 183.875 * 60 / bpm * 1000) / (1000 / FPS)):
            now.append(LinearPattern(375, 0, bulletImg[2], 15, frame, 0.5, 8))
        elif frame == int((offset + 184 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(50, 5, bulletImg[1], 15, frame, 0.07, 5, 0))
        elif frame == int((offset + 184.5 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(75, 5, bulletImg[1], 15, frame, 0.07, 5, 0))
        elif frame == int((offset + 184.95 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(100, 5, bulletImg[1], 15, frame, 0.07, 5, 0))
        elif frame == int((offset + 185.35 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(125, 5, bulletImg[1], 15, frame, 0.07, 5, 0))
        elif frame == int((offset + 185.7 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(150, 5, bulletImg[1], 15, frame, 0.07, 5, 0))
        elif frame == int((offset + 186 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(175, 5, bulletImg[1], 15, frame, 0.07, 5, 0))
        elif frame == int((offset + 186.25 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(200, 5, bulletImg[1], 15, frame, 0.07, 5, 0))
        elif frame == int((offset + 186.45 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(225, 5, bulletImg[1], 15, frame, 0.07, 5, 0))
        elif frame == int((offset + 186.6 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(250, 5, bulletImg[1], 15, frame, 0.07, 5, 0))
        elif frame == int((offset + 186.7 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(275, 5, bulletImg[1], 15, frame, 0.07, 5, 0))
        elif frame == int((offset + 186.8 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(310, 5, bulletImg[1], 15, frame, 0.07, 5, 0))
        elif frame == int((offset + 186.9 * 60 / bpm * 1000) / (1000 / FPS)):
            now.extend(CirclePattern(355, 5, bulletImg[1], 15, frame, 0.07, 5, 0))


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
while running and level == 1:
    if currentFrame % 10 == 0:
        i += 1
    if currentFrame == 0:
        pygame.mixer.music.load(musics[0])
        pygame.mixer.music.play()
    currentFrame += 1
    screen.fill((255, 255, 255))  # 회색 화면
    screen.blit(background[0], (0, 0))

    # Text(score, 520, 30)
    Text((currentFrame * 1000 / 60 - 689) / 1000 * 210 / 60, 520, 60)
    playerPos = (x - 12, y - 22)
    screen.blit(playerImg, playerPos)
    score += i

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
    # Pattern1Easy(currentFrame, bullets, warnLine, line, x, y)
    if len(timingPoints) != 0:
        if currentFrame == timingPoints[0]:
            del timingPoints[0]
            bullets.extend(patterns[0])
            del patterns[0]

    index = 0
    for bullet in bullets:
        bullet.go(x, y)
        # if (bullet.x - x) ** 2 + (bullet.y - y) ** 2 < (bullet.size / 2) ** 2:
        #     bullets = []
        #     i = 0
        #     break
        if bullet.x < -30 or bullet.x > 430 or bullet.y < -10 or bullet.y > 530:
            del bullets[index]
        screen.blit(bullet.image, (bullet.x - bullet.size / 2, bullet.y - bullet.size / 2))
        index += 1
    for warn in warnLine:
        if warn.end < currentFrame - warn.start:
            warnLine.remove(warn)
        screen.blit(warn.image, (warn.x, 0))
    for linear in line:
        # if linear.x <= x <= linear.x + linear.size:
        #     line = []
        #     i = 0
        #     break
        if linear.end < currentFrame - linear.start:
            line.remove(linear)
        screen.blit(linear.image, (linear.x, 0))
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
