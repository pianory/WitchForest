import pygame
import random
import sys
import math
import time

# -*- coding:utf-8 -*-#

# 01 - Main Game Setting
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((640, 640))
pygame.display.set_caption("마녀의 숲")

# 02 - Normal Variable
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
x = 200
y = 480
keys = [pygame.K_d, pygame.K_f, pygame.K_j, pygame.K_k]
hiSpeed = 2

# 02-01 - All Images
judgeImg = [pygame.image.load("./img/25_3.png"), pygame.image.load("./img/25_2.png"),
            pygame.image.load("./img/25_4.png"),
            pygame.image.load("./img/25_5.png"), pygame.image.load("./img/25_1.png")]
noteImg = [pygame.image.load("./img/note1.png").convert(), pygame.image.load("./img/note2.png").convert(),
           pygame.image.load("./img/note2.png").convert(), pygame.image.load("./img/note1.png").convert(),
           pygame.image.load("./img/note1L.png").convert(), pygame.image.load("./img/note2L.png").convert()]


# 03-01 - Class Bullet
class Bullet:
    def __init__(self, timing, x, y, image, size, angle, speed, startX, startY):
        self.x, self.y, self.image, self.size, self.angle, self.speed, self.timing = x, y, image, size, angle, speed, timing
        self.startX, self.startY = startX, startY

    def show(self, playerX, playerY):
        pass


# 03-02 - Class Bullet to Player
class BulletPlayer(Bullet):
    def __init__(self, timing, x, y, image, size, playerposX, playerposY, speed, startX, startY, angle):
        super().__init__(timing, x, y, image, size, angle, speed, startX, startY)
        self.playerposX, self.playerposY = playerposX, playerposY

    def show(self, playerX, playerY):
        self.angle = math.atan(
            (playerY - self.startY) / (playerX - self.startX + 0.0001)) / math.pi if playerX > self.startX else (
                                                                                                                        math.pi + math.atan(
                                                                                                                    (
                                                                                                                            playerY - self.startY) / (
                                                                                                                            playerX - self.startX + 0.0001))) / math.pi


# 03-03 - Class Bullet Showed to Screen
class BulletShow:
    def __init__(self, timing, image, size, startX, startY, angle, speed, status, x, y):
        self.timing, self.image, self.size, self.startX, self.startY, self.angle, self.status = timing, image, size, startX, startY, angle, status
        self.x, self.y = x, y
        self.speed = speed

    def go(self, c):
        global FPS
        self.x = self.startX + math.cos(self.angle * math.pi) * self.speed * (c - self.timing) / 1000 * FPS
        self.y = self.startY + math.sin(self.angle * math.pi) * self.speed * (c - self.timing) / 1000 * FPS


# 03-04 - Class Objective
class Object:
    def __init__(self, start, end, image, x, y, speed, moveAngle, status, startX, startY, width, height):
        self.start, self.end, self.image, self.x, self.y, self.speed, self.moveAngle, self.status = start, end, image, x, y, speed, moveAngle, status
        self.startX, self.startY = startX, startY
        self.height, self.width = height, width

    def go(self, c):
        self.x = self.startX + math.cos(self.moveAngle * math.pi) * self.speed * (c - self.start) / 1000 * FPS
        self.y = self.startY + math.sin(self.moveAngle * math.pi) * self.speed * (c - self.start) / 1000 * FPS


# 03-05 - Class Draws Line
class Line:
    def __init__(self, start, end, color, startX, startY, endX, endY, thickness):
        self.start, self.end, self.color, self.startX, self.startY, self.endX, self.endY, self.thickness = start, end, color, startX, startY, endX, endY, thickness


# 03-06 - Function makes circle pattern
def Circle(timing, x, y, image, size, angle, speed, shift):
    global FPS
    a = []
    i = 0
    while i < 2:
        a.append(Bullet(timing, x, y, image, size, i + shift, speed * 60 / FPS, x, y))
        i += angle
    return a


# 03-07 - Function that opens
def Opener(timing, x, y, image, size, angle, speed):
    global FPS
    a = []
    speedList = list(map(float, speed.split(";")))
    for i in speedList:
        a.append(Bullet(timing, x, y, image, size, angle, i * 60 / FPS, x, y))
    return a


# 03-08 - Judgements
def Judgement(accuracy):
    if (accuracy - 1) // 30 == 0:
        return 101
    elif (accuracy - 1) // 30 == 1:
        return 100
    elif (accuracy - 1) // 30 <= 3:
        return 70
    elif (accuracy - 1) // 30 <= 5:
        return 40
    elif (accuracy - 1) // 30 <= 8:
        return 10
    else:
        return -1


# 03-09 - Note
class Note:
    def __init__(self, timing, num):
        self.timing = timing
        self.y = -500
        self.num = num


class ShowingNote:
    def __init__(self, timing, num, type, status):
        self.timing = timing
        self.y = -500
        self.num = num
        self.status = status
        self.type = type

    def go(self, curr):
        self.y = 450 - (self.timing - curr) / 1000 * 450 * hiSpeed

    def HIT(self, curr):
        if abs(self.timing - curr) <= 330:
            return Judgement(abs(self.timing - curr))
        else:
            return 0


# 03-10 - Long Note
class LongNote:
    def __init__(self, timing, num, end):
        self.timing = timing
        self.end = end
        self.y = -500
        self.num = num

    def go(self, curr):
        self.y = 450 - (self.timing - curr) / 1000 * 450 * hiSpeed - 15.5

    def HIT(self, curr, curNum):
        if curNum == self.num:
            if self.timing <= curr <= end:
                return 10
            elif curr > end:
                return 101


class Note1(Note):
    type = 1

    def __init__(self, timing, num):
        super().__init__(timing, num)


class Note2(Note):
    type = 2

    def __init__(self, timing, num):
        super().__init__(timing, num)


class Note3(Note):
    type = 3

    def __init__(self, timing, num):
        super().__init__(timing, num)


class Note4(Note):
    type = 4

    def __init__(self, timing, num):
        super().__init__(timing, num)


class LongNote1(LongNote):
    type = 1

    def __init__(self, timing, num, end):
        super().__init__(timing, num, end)


class LongNote2(LongNote):
    type = 2

    def __init__(self, timing, num, end):
        super().__init__(timing, num, end)


class LongNote3(LongNote):
    type = 3

    def __init__(self, timing, num, end):
        super().__init__(timing, num, end)


class LongNote4(LongNote):
    type = 4

    def __init__(self, timing, num, end):
        super().__init__(timing, num, end)


# 04 - Loads Level Medias
if level == 1:
    f = [open("./data/pattern1.ptn", "r"), open("./data/rhythm1.ptn", "r")]
    try:
        bulletImg = [pygame.image.load("./img/15_1.png"), pygame.image.load("./img/15_2.png"),
                     pygame.image.load("./img/15_3.png"), pygame.image.load("./img/15_4.png"),
                     pygame.image.load("./img/15_5.png"), pygame.image.load("./img/25_1.png"),
                     pygame.image.load("./img/25_2.png"), pygame.image.load("./img/25_3.png"),
                     pygame.image.load("./img/25_4.png"), pygame.image.load("./img/25_5.png")
                     ]
        playerImg = pygame.transform.scale(pygame.image.load("./img/witch.png"), (37, 64))
        background = [pygame.image.load("./img/background.png")]
        musics = ["./audio/Armageddon.ogg"]
        objectImg = []

    except Exception as err:
        print('그림 또는 효과음 삽입에 문제가 있습니다.: ', err)
        pygame.quit()
        sys.exit(0)

elif level == 2:
    f = [open("./data/pattern2.ptn", "r"), open("./data/rhythm2.ptn", "r")]
    try:
        bulletImg = [pygame.image.load("./img/15_5.png"), pygame.image.load("./img/15_black.png"),
                     pygame.image.load("./img/15_white.png"), pygame.image.load("./img/15_grey.png"),
                     pygame.image.load("./img/25_black.png"), pygame.image.load("./img/25_white.png")
                     ]
        playerImg = pygame.transform.scale(pygame.image.load("./img/witch.png"), (37, 64))
        background = [pygame.image.load("./img/background.png")]
        musics = ["./audio/Pictured as Perfect.mp3", "./audio/Ultra Blazures.mp3"]

    except Exception as err:
        print('그림 또는 효과음 삽입에 문제가 있습니다.: ', err)
        pygame.quit()
        sys.exit(0)

# 05 - Reads File
cr = 0
timingPoints = []
patterns = []
cur = []
nowLine = 0
while True:  # 05-01 - Reading Patterns
    line = f[0].readline()
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
while True:  # 05-02 - Reading Objects
    line = f[0].readline()
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
while True:  # 05-03 Reading Lines
    line = f[0].readline()
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

f[0].close()


# 06 - Other Functions
def Text(arg1, x, y):
    font = pygame.font.Font("./fonts/HeirofLightRegular.ttf", 18)
    text = font.render("SCORE  " + str(arg1).zfill(14), True, (255, 255, 255))
    textRect = text.get_rect()
    textRect.centerx = x
    textRect.centery = y
    screen.blit(text, textRect)


def showHP(arg):
    font = pygame.font.Font("./fonts/HeirofLightBold.ttf", 20)
    if arg < 0:
        green = 0
        blue = 0
        red = 255
    elif arg < 500:
        green = int(arg * 2.55 / 10)
        blue = 0
        red = 255 - int(255 / 500 * arg)
    else:
        blue = int((arg - 500) * 2.55 / 10)
        green = int((1000 - arg) * 2.55 / 10)
        red = 0
    pygame.draw.line(screen, (red, green, blue), [100, 570], [100 + int(arg * 3) / 10, 570], 30)
    text = font.render("HP  " + str(arg).zfill(3), True, (red // 2 + 128, green // 2 + 128, blue // 2 + 128))
    textRect = text.get_rect()
    textRect.centerx = 50
    textRect.centery = 570
    screen.blit(text, textRect)


# 07 - Main Page(Menu)
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

# 08 - Gaming
patternNo, objectNo, drawingNo = 0, 0, 0
length, objectLength, drawingLength = len(patterns), len(objects), len(drawings)
bullets, showingObjects, showingDrawings = [], [], []
hp = 1000
for _ in range(1000):
    bullets.append(BulletShow(None, None, None, None, None, None, None, False, None,
                              None))  # Tmg, img, siz, sx, sy, ang, spd, sta, x, y
for _ in range(30):
    showingObjects.append(Object(None, None, None, None, None, None, None, False, None, None, None, None))
for _ in range(100):
    showingDrawings.append(Line(None, None, None, None, None, None, None, None))

avoiding = True
# 09 - Main Game / Avoiding
while avoiding:
    if isStart:
        pygame.mixer.music.load(musics[0])
        pygame.mixer.music.play()
        start = int(round(time.time() * 1000))
        print(start)
        isStart = False
        previous = 0
    nowTime = int(round(time.time() * 1000))
    screen.fill((0, 0, 0))
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
    playerPos = (x - 37 / 2, y - 32)
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
                x -= 0.5 * fast * (nowTime - start - previous) / 1000 * 60
                if x < xMinusLimit: x = xMinusLimit
        else:
            if x >= xMinusLimit:
                x -= 1.5 * fast * (nowTime - start - previous) / 1000 * 60
                if x < xMinusLimit: x = xMinusLimit
    if key[pygame.K_RIGHT]:
        if key[pygame.K_LSHIFT]:
            if x <= xPlusLimit:
                x += 0.5 * fast * (nowTime - start - previous) / 1000 * 60
                if x > xPlusLimit: x = xPlusLimit
        else:
            if x <= xPlusLimit:
                x += 1.5 * fast * (nowTime - start - previous) / 1000 * 60
                if x > xPlusLimit: x = xPlusLimit
    if key[pygame.K_UP]:
        if key[pygame.K_LSHIFT]:
            if y >= yMinusLimit:
                y -= 0.5 * fast * (nowTime - start - previous) / 1000 * 60
                if y < yMinusLimit: y = yMinusLimit
        else:
            if y >= yMinusLimit:
                y -= 1.5 * fast * (nowTime - start - previous) / 1000 * 60
                if y < yMinusLimit: y = yMinusLimit
    if key[pygame.K_DOWN]:
        if key[pygame.K_LSHIFT]:
            if y <= yPlusLimit:
                y += 0.5 * fast * (nowTime - start - previous) / 1000 * 60
                if y > yPlusLimit: y = yPlusLimit
        else:
            if y <= yPlusLimit:
                y += 1.5 * fast * (nowTime - start - previous) / 1000 * 60
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
                    hp -= int(i.size ** 2 // 45)
                screen.blit(i.image, (int(int(i.x) - i.size / 2), int(int(i.y) - i.size / 2)))
    if (nowTime - start) // 1000 > previous // 1000:
        if hp < 999:
            hp += 2
        elif hp == 999:
            hp = 1000
    if nowTime - start > timingPoints[-1] + 5000:
        score += (timingPoints[-1] + 5000 - previous) * hp
    else:
        score += (nowTime - start - previous) * hp
    previous = nowTime - start
    screen.blit(background[0], (0, 0))
    showHP(hp)
    Text(score, 520, 50)
    pygame.display.flip()
    if nowTime - start > timingPoints[-1] + 5000:
        avoiding = False
    if hp < 0:
        avoiding, running = False, False
    fpsClock.tick(FPS)
# rhythm = True
# while rhythm:
laneNo = [0, 0, 0, 0]
cur = []
curLong = []
cr = 0
rhythmTimingPoints = []
rhythmNotes = []
rhythmLongNotes = []
currentNotePattern = []
currentLongPattern = []
while True:  # 10-01 - Reading Rhythm Patterns
    line = f[1].readline()
    if not line: break
    p = list(map(str, line.split()))
    if cr == int(p[0]):
        if p[1] == "N":
            if int(p[2]) == 1:
                cur.append(Note1(int(p[0]), laneNo[0]))
                laneNo[0] += 1
            elif int(p[2]) == 2:
                cur.append(Note2(int(p[0]), laneNo[1]))
                laneNo[1] += 1
            elif int(p[2]) == 3:
                cur.append(Note3(int(p[0]), laneNo[2]))
                laneNo[2] += 1
            elif int(p[2]) == 4:
                cur.append(Note4(int(p[0]), laneNo[3]))
                laneNo[3] += 1
        elif p[1] == "L":
            if int(p[2]) == 1:
                cur.append(Note1(int(p[0]), laneNo[0]))
                curLong.append(LongNote1(int(p[0]), laneNo[0], int(p[3])))
                laneNo[0] += 1
            elif int(p[2]) == 2:
                cur.append(Note2(int(p[0]), laneNo[1]))
                curLong.append(LongNote2(int(p[0]), laneNo[1], int(p[3])))
                laneNo[1] += 1
            elif int(p[2]) == 3:
                cur.append(Note3(int(p[0]), laneNo[2]))
                curLong.append(LongNote3(int(p[0]), laneNo[2], int(p[3])))
                laneNo[2] += 1
            elif int(p[2]) == 4:
                cur.append(Note4(int(p[0]), laneNo[3]))
                curLong.append(LongNote4(int(p[0]), laneNo[3], int(p[3])))
                laneNo[3] += 1
    else:
        if cr != 0:
            rhythmNotes.append(cur)
            rhythmLongNotes.append(curLong)
            rhythmTimingPoints.append(cr)
        cur = []
        curLong = []
        cr = int(p[0])
        if p[1] == "N":
            if int(p[2]) == 1:
                cur.append(Note1(int(p[0]), laneNo[0]))
                laneNo[0] += 1
            elif int(p[2]) == 2:
                cur.append(Note2(int(p[0]), laneNo[1]))
                laneNo[1] += 1
            elif int(p[2]) == 3:
                cur.append(Note3(int(p[0]), laneNo[2]))
                laneNo[2] += 1
            elif int(p[2]) == 4:
                cur.append(Note4(int(p[0]), laneNo[3]))
                laneNo[3] += 1
        elif p[1] == "L":
            if int(p[2]) == 1:
                cur.append(Note1(int(p[0]), laneNo[0]))
                curLong.append(LongNote1(int(p[0]), laneNo[0], int(p[3])))
                laneNo[0] += 1
            elif int(p[2]) == 2:
                cur.append(Note2(int(p[0]), laneNo[1]))
                curLong.append(LongNote2(int(p[0]), laneNo[1], int(p[3])))
                laneNo[1] += 1
            elif int(p[2]) == 3:
                cur.append(Note3(int(p[0]), laneNo[2]))
                curLong.append(LongNote3(int(p[0]), laneNo[2], int(p[3])))
                laneNo[2] += 1
            elif int(p[2]) == 4:
                cur.append(Note4(int(p[0]), laneNo[3]))
                curLong.append(LongNote4(int(p[0]), laneNo[3], int(p[3])))
                laneNo[3] += 1
    # nowLine += 1

rhythmTimingPoints.append(cr)
rhythmNotes.append(cur)
rhythmLongNotes.append(curLong)
opening = True
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

story = open("./data/story2.ptn", "r", encoding='UTF8')
who = story.readline()
said = story.readline()
blank = story.readline()
previous = True
storyNo = 0
while True:
    pygame.event.pump()  # Allow pygame to handle internal actions.
    key = pygame.key.get_pressed()
    screen.fill((0, 0, 0))
    screen.blit(pygame.image.load("./img/story.png"), (5, 337))
    font = pygame.font.Font("./fonts/HeirofLightBold.ttf", 18)
    text = font.render(who, True, (255, 255, 255))
    screen.blit(text, (20, 350))
    font = pygame.font.Font("./fonts/HeirofLightRegular.ttf", 12)
    text = font.render(said, True, (0, 0, 0))
    screen.blit(text, (20, 400))
    screen.blit(pygame.image.load("./img/Witch/Normal.png"), (5, 80))
    screen.blit(pygame.image.load("./img/Frums/Normal.png"), (395 - 180, 80))
    screen.blit(background[0], (0, 0))
    if not blank:
        text = font.render("Space : Start", True, (0, 0, 0))
        screen.blit(text, (300, 450))
    if not who:
        break
    pygame.display.flip()
    if key[pygame.K_SPACE] and not previous:
        who = story.readline()
        said = story.readline()
        blank = story.readline()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
    previous = key[pygame.K_SPACE]


def ShowCombo(combo):
    font = pygame.font.Font("./fonts/HeirofLightBold.ttf", 30)
    text = font.render(str(combo).zfill(3), True, (255, 255, 255))
    textRect = text.get_rect()
    textRect.centerx = 200
    textRect.centery = 200
    screen.blit(text, textRect)


isStart = True
rhythm = True
patternNo = 0
currentLines = [0, 0, 0, 0]
offset = -275
combo = 0
judge = 0
for _ in range(35):
    currentNotePattern.append(ShowingNote(None, -1, 0, False))
while rhythm:
    if isStart:
        pygame.mixer.music.load(musics[1])
        pygame.mixer.music.play()
        start = int(round(time.time() * 1000))
        isStart = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
    noteX = [200-96, 200-32, 200+32, 200+96]
    nowTime = int(round(time.time() * 1000))
    screen.fill((0, 0, 0))
    pygame.draw.line(screen, (255, 0, 0), [5, 450], [395, 450], 30)
    if len(rhythmTimingPoints) > patternNo:
        if rhythmTimingPoints[patternNo] <= nowTime - start + 1000 + offset:
            j = 0
            curr = rhythmNotes[patternNo][j]
            i = 0
            while j < len(rhythmNotes[patternNo]):
                if not currentNotePattern[i].status:
                    currentNotePattern[i].timing, currentNotePattern[i].num = curr.timing, curr.num
                    currentNotePattern[i].type = curr.type
                    currentNotePattern[i].status = True
                    j += 1
                    if j >= len(rhythmNotes[patternNo]):
                        break
                    curr = rhythmNotes[patternNo][j]
                i += 1
            patternNo += 1
    pygame.event.pump()  # Allow pygame to handle internal actions.
    key = pygame.key.get_pressed()
    for i in currentNotePattern:
        if i.status:
            i.go(nowTime - start + offset)
            screen.blit(noteImg[i.type - 1], (noteX[i.type - 1] - 32, i.y - 15.5))
            if i.timing < nowTime - start + offset - 330 and i.status:
                currentLines[i.type - 1] += 1
                i.status = False
                hp -= 50
                combo = 0
                judge = -1
                judgeTiming = nowTime - start
    if key[pygame.K_d] and not previousKey[0]:
        for p in currentNotePattern:
            if p.type == 1 and p.num == currentLines[0] and p.status:
                judge = p.HIT(nowTime - start + offset)
                if judge > 0:
                    currentLines[0] += 1
                    combo += 1
                    score += int((judge + (combo ** 0.5 / 10) * 100) * hp / 10)
                    p.status = False
                    judgeTiming = nowTime - start
                    if judge == 100 or judge == 101:
                        if hp < 999:
                            hp += 2
                        else:
                            hp = 1000
                    elif 20 < judge < 100:
                        if hp < 1000:
                            hp += 1
                        else:
                            hp = 1000
                    break
                if judge == -1:
                    currentLines[0] += 1
                    combo = 0
                    p.status = False
                    judgeTiming = nowTime - start
                    hp -= 50
                    break
    if key[pygame.K_f] and not previousKey[1]:
        for p in currentNotePattern:
            if p.type == 2 and p.num == currentLines[1] and p.status:
                judge = p.HIT(nowTime - start + offset)
                if judge > 0:
                    currentLines[1] += 1
                    combo += 1
                    score += int((judge + (combo ** 0.5 / 10) * 100) * hp / 10)
                    p.status = False
                    judgeTiming = nowTime - start
                    if judge == 100 or judge == 101:
                        if hp < 999:
                            hp += 2
                        else:
                            hp = 1000
                    elif 20 < judge < 100:
                        if hp < 1000:
                            hp += 1
                        else:
                            hp = 1000
                    break
                if judge == -1:
                    currentLines[1] += 1
                    combo = 0
                    p.status = False
                    judgeTiming = nowTime - start
                    hp -= 50
                    break
    if key[pygame.K_j] and not previousKey[2]:
        for p in currentNotePattern:
            if p.type == 3 and p.num == currentLines[2] and p.status:
                judge = p.HIT(nowTime - start + offset)
                if judge > 0:
                    currentLines[2] += 1
                    combo += 1
                    score += int((judge + (combo ** 0.5 / 10) * 100) * hp / 10)
                    p.status = False
                    judgeTiming = nowTime - start
                    if judge == 100 or judge == 101:
                        if hp < 999:
                            hp += 2
                        else:
                            hp = 1000
                    elif 20 < judge < 100:
                        if hp < 1000:
                            hp += 1
                        else:
                            hp = 1000
                    break
                if judge == -1:
                    currentLines[2] += 1
                    combo = 0
                    p.status = False
                    judgeTiming = nowTime - start
                    hp -= 50
                    break
    if key[pygame.K_k] and not previousKey[3]:
        for p in currentNotePattern:
            if p.type == 4 and p.num == currentLines[3] and p.status:
                judge = p.HIT(nowTime - start + offset)
                if judge > 0:
                    currentLines[3] += 1
                    combo += 1
                    score += int((judge + (combo ** 0.5 / 10) * 100) * hp / 10)
                    p.status = False
                    judgeTiming = nowTime - start
                    if judge == 100 or judge == 101:
                        if hp < 999:
                            hp += 2
                        else:
                            hp = 1000
                    elif 20 < judge < 100:
                        if hp < 1000:
                            hp += 1
                        else:
                            hp = 1000
                    break
                if judge == -1:
                    currentLines[3] += 1
                    combo = 0
                    p.status = False
                    judgeTiming = nowTime - start
                    hp -= 50
                    break
    previousKey = [key[pygame.K_d], key[pygame.K_f], key[pygame.K_j], key[pygame.K_k]]
    screen.blit(background[0], (0, 0))
    Text(score, 520, 50)
    showHP(hp)
    ShowCombo(combo)
    font = pygame.font.Font("./fonts/PentagramsSalemica-B978.ttf", 28)
    if judge == 101:
        text = font.render("Witchtic!", True, (255, 128, 255))  # 보라
    elif judge == 100:
        text = font.render("Witchtic!", True, (255, 192, 255))  # 연보라
    elif judge == 70:
        text = font.render("Thamiel!", True, (255, 255, 128))  # 연노랑
    elif judge == 40:
        text = font.render("Samael", True, (128, 255, 128))  # 연두
    elif judge == 10:
        text = font.render("Nehemoth", True, (255, 128, 128))  # 분홍
    elif judge == -1:
        text = font.render("Sephira...", True, (255, 0, 0))  # 빨강
    if judge != 0:
        if nowTime - start - judgeTiming <= 500:
            textRect = text.get_rect()
            textRect.centerx = 200
            textRect.centery = 300
            screen.blit(text, textRect)
    pygame.display.flip()

screen.blit(gameOverImg, (0, 0))
Text(score, screen.get_rect().centerx, screen.get_rect().centery)
pygame.display.flip()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
