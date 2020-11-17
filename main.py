import pygame
import random
import sys
import math
import time

# -*- coding:utf-8 -*-#

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((640, 640))
pygame.display.set_caption("마녀의 숲")

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
level = 2

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
    background = [pygame.image.load("./img/background.png")]
    musics = ["./audio/Armageddon.ogg"]
    a = [pygame.image.load("./img/danger.png")]

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
            (playerY - self.startY) / (playerX - self.startX + 0.0001)) / math.pi if playerX > self.startX else (math.pi + math.atan((playerY - self.startY) / (playerX - self.startX + 0.0001))) / math.pi


class BulletShow:
    def __init__(self, timing, image, size, startX, startY, angle, speed, status, x, y):
        self.timing, self.image, self.size, self.startX, self.startY, self.angle, self.status = timing, image, size, startX, startY, angle, status
        self.x, self.y = x, y
        self.speed = speed

    def go(self, c):
        global FPS
        self.x = self.startX + math.cos(self.angle * math.pi) * self.speed * (c - self.timing) / 1000 * FPS
        self.y = self.startY + math.sin(self.angle * math.pi) * self.speed * (c - self.timing) / 1000 * FPS


class Object:
    def __init__(self, start, end, image, x, y, speed, moveAngle, status, startX, startY, width, height):
        self.start, self.end, self.image, self.x, self.y, self.speed, self.moveAngle, self.status = start, end, image, x, y, speed, moveAngle, status
        self.startX, self.startY = startX, startY
        self.height, self.width = height, width

    def go(self, c):
        self.x = self.startX + math.cos(self.moveAngle * math.pi) * self.speed * (c - self.start) / 1000 * FPS
        self.y = self.startY + math.sin(self.moveAngle * math.pi) * self.speed * (c - self.start) / 1000 * FPS


class Line:
    def __init__(self, start, end, color, startX, startY, endX, endY, thickness):
        self.start, self.end, self.color, self.startX, self.startY, self.endX, self.endY, self.thickness = start, end, color, startX, startY, endX, endY, thickness


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


if level == 1:
    f = open("./data/pattern1.ptn", "r")
    try:
        bulletImg = [pygame.image.load("./img/15_1.png"), pygame.image.load("./img/15_2.png"),
                     pygame.image.load("./img/15_3.png"), pygame.image.load("./img/15_4.png"),
                     pygame.image.load("./img/15_5.png"), pygame.image.load("./img/25_1.png"),
                     pygame.image.load("./img/25_2.png"), pygame.image.load("./img/25_3.png"),
                     pygame.image.load("./img/25_4.png"), pygame.image.load("./img/25_5.png"),
                     ]
        playerImg = pygame.transform.scale(pygame.image.load("./img/player.png"), (37, 64))
        background = [pygame.image.load("./img/background.png")]
        musics = ["./audio/Armageddon.ogg"]
        objectImg = []

    except Exception as err:
        print('그림 또는 효과음 삽입에 문제가 있습니다.: ', err)
        pygame.quit()
        sys.exit(0)
elif level == 2:
    f = open("./data/pattern2.ptn", "r")
    try:
        bulletImg = [pygame.image.load("./img/15_5.png"), pygame.image.load("./img/15_black.png"),
                     pygame.image.load("./img/15_white.png"), pygame.image.load("./img/15_grey.png"),
                     pygame.image.load("./img/25_black.png"), pygame.image.load("./img/25_white.png")
                     ]
        playerImg = pygame.transform.scale(pygame.image.load("./img/player.png"), (37, 64))
        background = [pygame.image.load("./img/background.png")]
        musics = ["./audio/Pictured as Perfect.mp3"]
        objectImg = [pygame.image.load("./img/pictasperf_warn.png")]

    except Exception as err:
        print('그림 또는 효과음 삽입에 문제가 있습니다.: ', err)
        pygame.quit()
        sys.exit(0)
# File Read
cr = 0
timingPoints = []
patterns = []
cur = []
nowLine = 0
while True:
    line = f.readline()
    # print(line)
    if line == "=====\n": break
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
                                    float(p[6]) * 60 / FPS, float(p[2]), float(p[3]), 0))
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
                                    float(p[6]) * 60 / FPS, float(p[2]), float(p[3]), 0))
        elif p[1] == "O":
            cur.extend(
                Opener(int(p[0]), float(p[2]), float(p[3]), bulletImg[int(p[4])], float(p[5]), float(p[7]), p[6]))
    # nowLine += 1
timingPoints.append(cr)
patterns.append(cur)
objectTimingPoints = []
objects = []
cr = 0
cur = []
while True:  # Objects
    line = f.readline()
    if line == "=====\n": break
    if not line: break
    p = list(map(float, line.split()))
    if cr == int(p[0]):
        cur.append(
            Object(p[0], p[1], objectImg[int(p[4])], p[2], p[3], p[8], p[7], False, p[2], p[3], p[5], p[6])
        )
    else:
        if cr != 0:
            objects.append(cur)
            objectTimingPoints.append(cr)
        cur = []
        cr = int(p[0])
        cur.append(
            Object(p[0], p[1], objectImg[int(p[4])], p[2], p[3], p[8], p[7], False, p[2], p[3], p[5], p[6])
        )
    # nowLine += 1
if len(cur) > 0:
    objectTimingPoints.append(cr)
    objects.append(cur)
drawingTimingPoints = []
drawings = []
cr = 0
cur = []
while True:  # Objects
    line = f.readline()
    if line == "=====\n": break
    if not line: break
    p = list(map(str, line.split()))
    red, green, blue = map(int, p[2].split(";"))
    if cr == int(p[0]):
        cur.append(Line(int(p[0]), int(p[1]), (red, green, blue), float(p[3]), float(p[4]), float(p[5]), float(p[6]),
                        float(p[7])))
    else:
        if cr != 0:
            drawings.append(cur)
            drawingTimingPoints.append(cr)
        cur = []
        cr = int(p[0])
        cur.append(Line(int(p[0]), int(p[1]), (red, green, blue), float(p[3]), float(p[4]), float(p[5]), float(p[6]),
                        float(p[7])))
    # nowLine += 1
if len(cur) > 0:
    drawingTimingPoints.append(cr)
    drawings.append(cur)

f.close()


def Text(arg1, x, y):
    font = pygame.font.Font("./fonts/HeirofLightRegular.ttf", 18)
    text = font.render("TIMING  " + str(arg1).zfill(10), True, (255, 255, 255))
    textRect = text.get_rect()
    textRect.centerx = x
    textRect.centery = y
    screen.blit(text, textRect)


def showHP(arg):
    font = pygame.font.Font("./fonts/HeirofLightBold.ttf", 20)
    text = font.render("HP  " + str(arg).zfill(3), True, (255, 100, 100))
    textRect = text.get_rect()
    textRect.centerx = 50
    textRect.centery = 570
    screen.blit(text, textRect)
    if arg < 0:
        green = 0
        blue = 0
        red = 255
    elif arg < 50:
        green = int(arg * 2.55)
        blue = 0
        red = 255 - int(255/50*arg)
    else:
        blue = int((arg - 50) * 2.55)
        green = int((100 - arg) * 2.55)
        red = 0
    pygame.draw.line(screen, (red, green, blue), [100, 570], [100+int(arg*3), 570], 30)


warnLine, line = [], []
while opening:
    screen.fill((0, 0, 0))  # 회색 화면
    key = pygame.key.get_pressed()
    if key[pygame.K_SPACE]:
        opening = False
        running = True
        level = 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
isStart = True

i = 0
q = 0
patternNo = 0
objectNo = 0
drawingNo = 0
length = len(patterns)
objectLength = len(objects)
drawingLength = len(drawings)
bullets = []
showingObjects = []
showingDrawings = []
hp = 100
for _ in range(1000):
    bullets.append(BulletShow(None, None, None, None, None, None, None, False, None,
                              None))  # Tmg, img, siz, sx, sy, ang, spd, sta, x, y
for _ in range(30):
    showingObjects.append(Object(None, None, None, None, None, None, None, False, None, None, None, None))
for _ in range(100):
    showingDrawings.append(Line(None, None, None, None, None, None, None, None))
while running:
    if isStart:
        pygame.mixer.music.load(musics[0])
        pygame.mixer.music.play()
        start = int(round(time.time() * 1000))
        print(start)
        isStart = False
        previous = start
    nowTime = int(round(time.time() * 1000))
    screen.fill((0, 0, 0))  # 회색 화면
    if nowTime - previous > 1000:
        previous += 1000
        if hp < 100:
            hp += 1
    screen.blit(background[0], (0, 0))

    # screen.blit(a[0], (5, 5))
    # screen.blit(a[1], (300, 300))
    Text(nowTime - start, 520, 30)
    if objectLength > objectNo and objectLength > 0:
        if nowTime - start >= int(objectTimingPoints[objectNo]):
            j = 0
            curr = objects[objectNo][j]
            i = 0
            while j < len(objects[objectNo]):
                if not showingObjects[i].status:
                    showingObjects[i].start, showingObjects[i].end, showingObjects[i].image, showingObjects[i].x, \
                    showingObjects[i].y, showingObjects[i].speed, showingObjects[i].moveAngle, showingObjects[i].startX, \
                    showingObjects[i].startY, showingObjects[i].width, showingObjects[
                        i].height = curr.start, curr.end, curr.image, curr.x, curr.y, curr.speed, curr.moveAngle, curr.startX, curr.startY, curr.width, curr.height
                    showingObjects[i].status = True
                    j += 1
                    if j >= len(objects[objectNo]):
                        break
                    curr = objects[objectNo][j]
                i += 1
            objectNo += 1
    if drawingLength > drawingNo and drawingLength > 0:
        if nowTime - start >= int(drawingTimingPoints[drawingNo]):
            j = 0
            curr = drawings[drawingNo][j]
            i = 0
            while j < len(drawings[drawingNo]):
                if showingDrawings[i].end is None or showingDrawings[i].end < nowTime - start:
                    showingDrawings[i].start, showingDrawings[i].end, showingDrawings[i].color, showingDrawings[
                        i].startX, showingDrawings[i].startY, showingDrawings[i].endX, showingDrawings[i].endY, \
                    showingDrawings[
                        i].thickness = curr.start, curr.end, curr.color, curr.startX, curr.startY, curr.endX, curr.endY, curr.thickness
                    j += 1
                    if j >= len(drawings[drawingNo]):
                        break
                    curr = drawings[drawingNo][j]
                i += 1
            drawingNo += 1
    playerPos = (x - 12, y - 22)
    screen.blit(playerImg, playerPos)
    showHP(hp)
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
                    bullets[i].timing, bullets[i].image, bullets[i].size, bullets[i].startX, bullets[i].startY, bullets[
                        i].angle, bullets[i].speed, bullets[i].x, bullets[i].y \
                        = curr.timing, curr.image, curr.size, curr.startX, curr.startY, curr.angle, curr.speed, curr.x, curr.y
                    bullets[i].status = True
                    j += 1
                    if j >= len(patterns[patternNo]):
                        break
                    curr = patterns[patternNo][j]
                    curr.show(x, y)
                i += 1
            patternNo += 1
    for i in showingObjects:
        if i.status:
            i.go(nowTime - start)
            if i.end < nowTime - start:
                i.status = False
            else:
                screen.blit(i.image, (int(int(i.x) - i.width / 2), int(int(i.y) - i.height / 2)))
    for i in showingDrawings:
        if i.end is not None:
            if i.end > nowTime - start:
                pygame.draw.line(screen, i.color, [int(i.startX), int(i.startY)], [int(i.endX), int(i.endY)],
                                 int(i.thickness))
    for i in bullets:
        if i.status:
            i.go(nowTime - start)
            if i.x < -10 or i.x > 410 or i.y < -10 or i.y > 510:
                i.status = False
            else:
                if (i.x - x) ** 2 + (i.y - y) ** 2 < (i.size / 2) ** 2:
                    i.status = False
                    hp -= 5
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
