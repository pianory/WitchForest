import pygame
import random
import sys
import math
import time


# 마녀의 숲은 게임 '동방프로젝트'와 게임 'Just Shapes and Beats' 등의 게임에 영감을 받아 제작되었습니다.
# 키보드로 움직이고 Shift 키를 통해 속도를 줄일 수 있다는 점과 탄막의 패턴이 굉장히 어렵다는 점은 동방 프로젝트에서, 박자에 맞춰 패턴이 나온다는 점은 JSAB에서 영감을 받았습니다.
# 게임을 만들며 여러 이미지를 제작하고, 캐릭터를 외주받아 작업하기도 하였습니다.
# 여럿이서 같이 만들었다면 더 좋은 프로젝트가 되었을 것 같은데, 좀 많이 아쉬운 프로젝트입니다.

# Director, Designer, Programmer, Patterner Pianory(송재한)
# Patterner, Programmer(Little Amount) Kogun(고건)
# Special Thanks to 404NotFound(김보슬/@circus_atm)

# -*- coding:utf-8 -*-#

# 01 - Main Game Setting
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((640, 640))
pygame.display.set_caption("마녀의 숲")

# 02 - Normal Variables
FPS, fpsClock = 60, pygame.time.Clock()
score = 0
fast = 3
xMinusLimit, xPlusLimit, yMinusLimit, yPlusLimit = 5, 395, 5, 495
level = 0
x = 200
y = 480
hiSpeed = 2
opening = True
hp = 1000


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

    def show(self, playerX, playerY): # Determine the Angle to Player
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

    def go(self, c): # Move the Bullet
        global FPS
        self.x = self.startX + math.cos(self.angle * math.pi) * self.speed * (c - self.timing) / 1000 * FPS
        self.y = self.startY + math.sin(self.angle * math.pi) * self.speed * (c - self.timing) / 1000 * FPS


# 03-04 - Class Objective
class Object:
    def __init__(self, start, end, image, x, y, speed, moveAngle, status, startX, startY, width, height):
        self.start, self.end, self.image, self.x, self.y, self.speed, self.moveAngle, self.status = start, end, image, x, y, speed, moveAngle, status
        self.startX, self.startY = startX, startY
        self.height, self.width = height, width

    def go(self, c): # Move the Object(Update TODO)
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


# 03-07 - Function that opens the bullet
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

    def go(self, curr): # Move the Note
        self.y = 450 - (self.timing - curr) / 1000 * 450 * hiSpeed

    def HIT(self, curr): # Is Hit?
        if abs(self.timing - curr) <= 330:
            return Judgement(abs(self.timing - curr))
        else:
            return 0


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


# 05 - File Reading
def readPatternFile(f, stage):
    cr = 0
    timingPoints = []
    patterns = []
    cur = []
    while True:  # 05-01 - Reading Patterns
        line = f.readline()
        # print(line)
        if line == "=====\n": break
        if not line: break
        p = list(map(str, line.split()))
        if cr == int(p[0]):
            if p[1] == "C":
                r, s = p[7].split(";")
                cur.extend(
                    Circle(int(p[0]), float(p[2]), float(p[3]), bulletImg[int(p[4])], float(p[5]), float(r),
                           float(p[6]),
                           float(s)))
            elif p[1] == "L":
                cur.append(Bullet(int(p[0]), float(p[2]), float(p[3]), bulletImg[int(p[4])], float(p[5]), float(p[7]),
                                  float(p[6]) * 60 / FPS, float(p[2]), float(p[3])))
            elif p[1] == "E":
                cur.append(
                    BulletPlayer(int(p[0]), float(p[2]), float(p[3]), bulletImg[int(p[4])], float(p[5]), None, None,
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
                    Circle(int(p[0]), float(p[2]), float(p[3]), bulletImg[int(p[4])], float(p[5]), float(r),
                           float(p[6]),
                           float(s)))
            elif p[1] == "L":
                cur.append(Bullet(int(p[0]), float(p[2]), float(p[3]), bulletImg[int(p[4])], float(p[5]), float(p[7]),
                                  float(p[6]) * 60 / FPS, float(p[2]), float(p[3])))
            elif p[1] == "E":
                cur.append(
                    BulletPlayer(int(p[0]), float(p[2]), float(p[3]), bulletImg[int(p[4])], float(p[5]), None, None,
                                 float(p[6]) * 60 / FPS, float(p[2]), float(p[3]), 0))
            elif p[1] == "O":
                cur.extend(
                    Opener(int(p[0]), float(p[2]), float(p[3]), bulletImg[int(p[4])], float(p[5]), float(p[7]), p[6]))
        # nowLine += 1
        for _ in range(3 - stage):
            f.readline()
    timingPoints.append(cr)
    patterns.append(cur)
    return timingPoints, patterns


def readRhythmFile(f):
    laneNo = [0, 0, 0, 0]
    cur = []
    cr = 0
    rhythmTimingPoints = []
    rhythmNotes = []
    currentNotePattern = []
    while True:  # 10-01 - Reading Rhythm Patterns
        line = f.readline()
        if not line: break
        p = list(map(str, line.split()))
        if cr == int(p[0]):
            if int(p[1]) == 1:
                cur.append(Note1(int(p[0]), laneNo[0]))
                laneNo[0] += 1
            elif int(p[1]) == 2:
                cur.append(Note2(int(p[0]), laneNo[1]))
                laneNo[1] += 1
            elif int(p[1]) == 3:
                cur.append(Note3(int(p[0]), laneNo[2]))
                laneNo[2] += 1
            elif int(p[1]) == 4:
                cur.append(Note4(int(p[0]), laneNo[3]))
                laneNo[3] += 1
        else:
            if cr != 0:
                rhythmNotes.append(cur)
                rhythmTimingPoints.append(cr)
            cur = []
            curLong = []
            cr = int(p[0])
            if int(p[1]) == 1:
                cur.append(Note1(int(p[0]), laneNo[0]))
                laneNo[0] += 1
            elif int(p[1]) == 2:
                cur.append(Note2(int(p[0]), laneNo[1]))
                laneNo[1] += 1
            elif int(p[1]) == 3:
                cur.append(Note3(int(p[0]), laneNo[2]))
                laneNo[2] += 1
            elif int(p[1]) == 4:
                cur.append(Note4(int(p[0]), laneNo[3]))
                laneNo[3] += 1
    rhythmTimingPoints.append(cr)
    rhythmNotes.append(cur)
    return rhythmTimingPoints, rhythmNotes


def readStory(f):
    totalStory = []
    while True:
        who = f.readline().strip("\n")
        curLine = f.readline().strip("\n")
        if not curLine:
            break
        image = f.readline().strip("\n")
        totalStory.append([who] + [curLine] + [image])
    print(totalStory)
    return totalStory


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


def ShowCombo(combo):
    font = pygame.font.Font("./fonts/HeirofLightBold.ttf", 30)
    text = font.render(str(combo).zfill(3), True, (255, 255, 255))
    textRect = text.get_rect()
    textRect.centerx = 200
    textRect.centery = 200
    screen.blit(text, textRect)


gameOn = False
option = False
leaderboard = False
currentMenu = 0
previousOpeningKeys = [0, 0, 0, 0]
# 07 - Opening
while opening:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
    screen.blit(pygame.image.load("./img/main.png").convert(), (0, 0))
    key = pygame.key.get_pressed()
    if key[pygame.K_DOWN] and not previousOpeningKeys[0] or key[pygame.K_RIGHT] and not previousOpeningKeys[1]:
        currentMenu = currentMenu + 1 if currentMenu < 1 else 0
        pygame.mixer.music.load("./audio/click-short.wav")
        pygame.mixer.music.play()
    if key[pygame.K_UP] and not previousOpeningKeys[2] or key[pygame.K_LEFT] and not previousOpeningKeys[3]:
        currentMenu = currentMenu - 1 if currentMenu > 0 else 1
        pygame.mixer.music.load("./audio/click-short.wav")
        pygame.mixer.music.play()
    previousOpeningKeys = [key[pygame.K_DOWN], key[pygame.K_RIGHT], key[pygame.K_UP], key[pygame.K_LEFT],
                           key[pygame.K_RETURN]]
    if currentMenu == 0:
        screen.blit(pygame.image.load("./img/arrow.png"), (300, 335))
    if currentMenu == 1:
        screen.blit(pygame.image.load("./img/arrow.png"), (300, 415))
    if key[pygame.K_RETURN]:
        pygame.mixer.music.load("./audio/confirm.mp3")
        pygame.mixer.music.play()
        if currentMenu == 0:
            opening = False
            gameOn = True
        elif currentMenu == 1:
            opening = False
            howToPlay = True

    pygame.display.flip()

menuX = 0
menuY = 0
live = False
while gameOn: # 08 - Processing Game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
    screen.blit(pygame.image.load("./img/difficulty.png").convert(), (0, 0))
    key = pygame.key.get_pressed()
    if key[pygame.K_DOWN] and not previousOpeningKeys[0]:
        menuY = 1
        pygame.mixer.music.load("./audio/click-short.wav")
        pygame.mixer.music.play()
    if key[pygame.K_RIGHT] and not previousOpeningKeys[1]:
        menuX = 1
        pygame.mixer.music.load("./audio/click-short.wav")
        pygame.mixer.music.play()
    if key[pygame.K_UP] and not previousOpeningKeys[2]:
        menuY = 0
        pygame.mixer.music.load("./audio/click-short.wav")
        pygame.mixer.music.play()
    if key[pygame.K_LEFT] and not previousOpeningKeys[3]:
        menuX = 0
        pygame.mixer.music.load("./audio/click-short.wav")
        pygame.mixer.music.play()
    if menuX == 0 and menuY == 0:
        screen.blit(pygame.image.load("./img/arrow.png"), (50, 345))
        screen.blit(pygame.image.load("./img/arrowRight.png"), (250, 345))
    if menuX == 0 and menuY == 1:
        screen.blit(pygame.image.load("./img/arrow.png"), (50, 460))
        screen.blit(pygame.image.load("./img/arrowRight.png"), (250, 460))
    if menuX == 1 and menuY == 0:
        screen.blit(pygame.image.load("./img/arrow.png"), (365, 345))
        screen.blit(pygame.image.load("./img/arrowRight.png"), (565, 345))
    if menuX == 1 and menuY == 1:
        screen.blit(pygame.image.load("./img/arrow.png"), (365, 460))
        screen.blit(pygame.image.load("./img/arrowRight.png"), (565, 460))
    if key[pygame.K_RETURN] and not previousOpeningKeys[4]:
        pygame.mixer.music.load("./audio/confirm.mp3")
        pygame.mixer.music.play()
        if menuX == 0 and menuY == 0:
            difficulty = 0
        elif menuX == 1 and menuY == 0:
            difficulty = 1
        elif menuX == 0 and menuY == 1:
            difficulty = 2
        else:
            difficulty = 3
        gameOn = False
        live = True

    previousOpeningKeys = [key[pygame.K_DOWN], key[pygame.K_RIGHT], key[pygame.K_UP], key[pygame.K_LEFT],
                           key[pygame.K_RETURN]]

    pygame.display.flip()

avoiding = True
rhythm = False
isStart = True

while live: # 09 -  Main Game
    noteImg = [pygame.image.load("./img/25_1.png"), pygame.image.load("./img/25_2.png"), pygame.image.load("./img/25_3.png"), pygame.image.load("./img/25_4.png")]
    playerCharacter = [pygame.image.load("./img/Witch/Normal.png"), pygame.image.load("./img/Witch/Angry.png"),
                       pygame.image.load("./img/Witch/Laugh.png"), pygame.image.load("./img/Witch/Shocked.png")]
    if level == 0: # Loading the Image/Audio/Story
        try:
            story = [open("./data/story0.ptn", "r", encoding='UTF8')]
            background = [pygame.image.load("./img/background.png")]
        except Exception as err:
            print('그림 또는 효과음 삽입에 문제가 있습니다.: ', err)
            pygame.quit()
            sys.exit(0)
    elif level == 1:
        try:
            enemy = [pygame.image.load("./img/LeaF/Normal.png"), pygame.image.load("./img/LeaF/Angry.png"),
                     pygame.image.load("./img/LeaF/Laugh.png"), pygame.image.load("./img/LeaF/Shocked.png")]
            f = [open("./data/pattern1.ptn", "r"), open("./data/rhythm1.ptn", "r")]
            bulletImg = [pygame.image.load("./img/15_1.png"), pygame.image.load("./img/15_2.png"),
                         pygame.image.load("./img/15_3.png"), pygame.image.load("./img/15_4.png"),
                         pygame.image.load("./img/15_5.png"), pygame.image.load("./img/25_1.png"),
                         pygame.image.load("./img/25_2.png"), pygame.image.load("./img/25_3.png"),
                         pygame.image.load("./img/25_4.png"), pygame.image.load("./img/25_5.png")
                         ]
            playerImg = pygame.transform.scale(pygame.image.load("./img/witch.png"), (37, 64))
            background = [pygame.image.load("./img/background.png")]
            musics = ["./audio/Armageddon.ogg", "./audio/Wisdomiot.mp3"]
            story = [open("./data/story1-1.ptn", "r", encoding='UTF8'),
                     open("./data/story1-2.ptn", "r", encoding='UTF8'),
                     open("./data/story1-3.ptn", "r", encoding='UTF8')]  # 슈팅 전/피하기 전/리듬 전/End

        except Exception as err:
            print('그림 또는 효과음 삽입에 문제가 있습니다.: ', err)
            pygame.quit()
            sys.exit(0)

    elif level == 2:
        try:
            enemy = [pygame.image.load("./img/Riya/Normal.png"), pygame.image.load("./img/Riya/Angry.png"),
                     pygame.image.load("./img/Riya/Laugh.png"), pygame.image.load("./img/Riya/Shocked.png")]
            f = [open("./data/pattern2.ptn", "r"), open("./data/rhythm2.ptn", "r")]
            bulletImg = [pygame.image.load("./img/15_1.png"), pygame.image.load("./img/15_2.png"),
                         pygame.image.load("./img/15_3.png"), pygame.image.load("./img/15_4.png"),
                         pygame.image.load("./img/15_5.png"), pygame.image.load("./img/25_1.png"),
                         pygame.image.load("./img/25_2.png"), pygame.image.load("./img/25_3.png"),
                         pygame.image.load("./img/25_4.png"), pygame.image.load("./img/25_5.png")
                         ]
            playerImg = pygame.transform.scale(pygame.image.load("./img/witch.png"), (37, 64))
            background = [pygame.image.load("./img/background.png")]
            musics = ["./audio/Extinction.mp3", "./audio/Final Hope.mp3"]
            story = [open("./data/story2-1.ptn", "r", encoding='UTF8'),
                     open("./data/story2-2.ptn", "r", encoding='UTF8'),
                     open("./data/story2-3.ptn", "r", encoding='UTF8')]

        except Exception as err:
            print('그림 또는 효과음 삽입에 문제가 있습니다.: ', err)
            pygame.quit()
            sys.exit(0)

    elif level == 3:
        try:
            enemy = [pygame.image.load("./img/Neple/Normal.png"), pygame.image.load("./img/Neple/Angry.png"),
                     pygame.image.load("./img/Neple/Laugh.png"), pygame.image.load("./img/Neple/Shocked.png")]
            f = [open("./data/pattern3.ptn", "r"), open("./data/rhythm3.ptn", "r")]
            bulletImg = [pygame.image.load("./img/15_1.png"), pygame.image.load("./img/15_2.png"),
                         pygame.image.load("./img/15_3.png"), pygame.image.load("./img/15_4.png"),
                         pygame.image.load("./img/15_5.png"), pygame.image.load("./img/25_1.png"),
                         pygame.image.load("./img/25_2.png"), pygame.image.load("./img/25_3.png"),
                         pygame.image.load("./img/25_4.png"), pygame.image.load("./img/25_5.png")
                         ]
            playerImg = pygame.transform.scale(pygame.image.load("./img/witch.png"), (37, 64))
            background = [pygame.image.load("./img/background.png")]
            musics = ["./audio/Bring Me B4ck.mp3", "./audio/Eternity.mp3"]
            story = [open("./data/story3-1.ptn", "r", encoding='UTF8'),
                     open("./data/story3-2.ptn", "r", encoding='UTF8'),
                     open("./data/story3-3.ptn", "r", encoding='UTF8')]

        except Exception as err:
            print('그림 또는 효과음 삽입에 문제가 있습니다.: ', err)
            pygame.quit()
            sys.exit(0)

    elif level == 4:
        try:
            enemy = [pygame.image.load("./img/Frums/Normal.png"), pygame.image.load("./img/Frums/Angry.png"),
                     pygame.image.load("./img/Frums/Laugh.png"), pygame.image.load("./img/Frums/Shocked.png")]
            f = [open("./data/pattern4.ptn", "r"), open("./data/rhythm4.ptn", "r")]
            bulletImg = [pygame.image.load("./img/15_5.png"), pygame.image.load("./img/15_black.png"),
                         pygame.image.load("./img/15_white.png"), pygame.image.load("./img/15_grey.png"),
                         pygame.image.load("./img/25_black.png"), pygame.image.load("./img/25_white.png")
                         ]
            playerImg = pygame.transform.scale(pygame.image.load("./img/witch.png"), (37, 64))
            background = [pygame.image.load("./img/background.png")]
            musics = ["./audio/Pictured as Perfect.mp3", "./audio/Ultra Blazures.mp3"]
            story = [open("./data/story4-1.ptn", "r", encoding='UTF8'),
                     open("./data/story4-2.ptn", "r", encoding='UTF8'),
                     open("./data/story4-3.ptn", "r", encoding='UTF8')]

        except Exception as err:
            print('그림 또는 효과음 삽입에 문제가 있습니다.: ', err)
            pygame.quit()
            sys.exit(0)
    if level == 0: # Opening Story
        currentStory = readStory(story[0]) # Read Story
        playerNo = 0 # Image No.
        enemyNo = 0
        for i in currentStory: # Until Story Finishes
            time.sleep(0.5)
            if i[0] == "Circus": # Change the Image
                playerNo = int(i[2])
            else:
                enemyNo = int(i[2])
            while True:
                pygame.event.pump()  # Allow pygame to handle internal actions.
                key = pygame.key.get_pressed()
                screen.fill((0, 0, 0))
                screen.blit(pygame.image.load("./img/story.png"), (5, 337)) # Show the Story
                font = pygame.font.Font("./fonts/HeirofLightBold.ttf", 18)
                text = font.render(i[0], True, (255, 255, 255))
                screen.blit(text, (20, 350))
                font = pygame.font.Font("./fonts/HeirofLightRegular.ttf", 15)
                text = font.render(i[1], True, (0, 0, 0))
                screen.blit(text, (20, 400))

                screen.blit(playerCharacter[playerNo], (5, 80))
                screen.blit(background[0], (0, 0))
                if currentStory[-1] == i: # When Last Story
                    text = font.render("Space : Start", True, (0, 0, 0))
                    screen.blit(text, (300, 450))
                pygame.display.flip()
                if key[pygame.K_SPACE]: # When the SpaceBar Pressed
                    break
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit(0)

    if difficulty == 3 and level != 0: # Story 1
        currentStory = readStory(story[0])
        playerNo = 0
        enemyNo = 0
        for i in currentStory:
            time.sleep(0.1)
            if i[0] == "Circus":
                playerNo = int(i[2])
            else:
                enemyNo = int(i[2])
            while True:
                pygame.event.pump()  # Allow pygame to handle internal actions.
                key = pygame.key.get_pressed()
                screen.fill((0, 0, 0))
                screen.blit(pygame.image.load("./img/story.png"), (5, 337))
                font = pygame.font.Font("./fonts/HeirofLightBold.ttf", 18)
                text = font.render(i[0], True, (255, 255, 255))
                screen.blit(text, (20, 350))
                font = pygame.font.Font("./fonts/HeirofLightRegular.ttf", 15)
                text = font.render(i[1], True, (0, 0, 0))
                screen.blit(text, (20, 400))

                screen.blit(playerCharacter[playerNo], (5, 80))
                screen.blit(enemy[enemyNo], (395 - 180, 80))
                screen.blit(background[0], (0, 0))
                if currentStory[-1] == i:
                    text = font.render("Space : Start", True, (0, 0, 0))
                    screen.blit(text, (300, 450))
                pygame.display.flip()
                if key[pygame.K_SPACE]:
                    break
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit(0)

    if level != 0: # Loading The Avoid Pattern
        patternNo, isStart, bullets = 0, True, []
        timingPoints, patterns = readPatternFile(f[0], difficulty)
        for _ in range(1000):
            bullets.append(BulletShow(None, None, None, None, None, None, None, False, None,
                                      None))  # Tmg, img, siz, sx, sy, ang, spd, sta, x, y
    # Avoid Game
    while avoiding and level != 0:
        if isStart: # Song On
            pygame.mixer.music.load(musics[0])
            pygame.mixer.music.play()
            start = int(round(time.time() * 1000))
            isStart = False
            previous = 0
            got = start
        nowTime = int(round(time.time() * 1000)) # Timing
        screen.fill((0, 0, 0))
        playerPos = (x - 37 / 2, y - 32)
        screen.blit(playerImg, playerPos)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
        pygame.event.pump()  # Allow pygame to handle internal actions.
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]: # Player Move
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

        if len(timingPoints) > patternNo: # Load The Pattern
            if nowTime - start >= int(timingPoints[patternNo]):
                j = 0
                curr = patterns[patternNo][j]
                curr.show(x, y)
                i = 0
                while j < len(patterns[patternNo]):
                    if not bullets[i].status:
                        bullets[i].timing, bullets[i].image, bullets[i].size, bullets[i].startX, bullets[i].startY, \
                        bullets[
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
        for i in bullets: # Show the Pattern On Screen
            if i.status:
                i.go(nowTime - start)
                if i.x < -10 or i.x > 410 or i.y < -10 or i.y > 510:
                    i.status = False
                else: # HP Drain
                    if (i.x - x) ** 2 + (i.y - y) ** 2 < (i.size / 2) ** 2:
                        i.status = False
                        got = nowTime
                        hp -= int(i.size ** 2 // 45) * (4 - difficulty) ** 2 // (5 - level) ** 0.5
                    screen.blit(i.image, (int(int(i.x) - i.size / 2), int(int(i.y) - i.size / 2)))
        if (nowTime - start) // 1000 > previous // 1000: # HP Regeneration
            hp += (1 + (nowTime - got) // 1000) * (5 - level)
            if hp > 1000:
                hp = 1000
        if nowTime - start > timingPoints[-1] + 5000: # Score On
            score += (timingPoints[-1] + 5000 - previous) * hp
        else:
            score += (nowTime - start - previous) * hp
        previous = nowTime - start
        screen.blit(background[0], (0, 0))
        showHP(hp)
        Text(score, 520, 50)
        pygame.display.flip()
        if nowTime - start > timingPoints[-1] + 5000: # Stage Clear
            avoiding = False
        if hp < 0:
            avoiding, live = False, False # Stage Failed
        fpsClock.tick(FPS)
    if not live:
        break

    if difficulty == 3 and level != 0: # Story 2
        currentStory = readStory(story[1])
        playerNo = 0
        enemyNo = 0
        for i in currentStory:
            time.sleep(0.1)
            if i[0] == "Circus":
                playerNo = int(i[2])
            else:
                enemyNo = int(i[2])
            while True:
                pygame.event.pump()  # Allow pygame to handle internal actions.
                key = pygame.key.get_pressed()
                screen.fill((0, 0, 0))
                screen.blit(pygame.image.load("./img/story.png"), (5, 337))
                font = pygame.font.Font("./fonts/HeirofLightBold.ttf", 18)
                text = font.render(i[0], True, (255, 255, 255))
                screen.blit(text, (20, 350))
                font = pygame.font.Font("./fonts/HeirofLightRegular.ttf", 15)
                text = font.render(i[1], True, (0, 0, 0))
                screen.blit(text, (20, 400))

                screen.blit(playerCharacter[playerNo], (5, 80))
                screen.blit(enemy[enemyNo], (395 - 180, 80))
                screen.blit(background[0], (0, 0))
                if currentStory[-1] == i:
                    text = font.render("Space : Start", True, (0, 0, 0))
                    screen.blit(text, (300, 450))
                pygame.display.flip()
                if key[pygame.K_SPACE]:
                    break
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit(0)
    if difficulty == 3 and level != 0: # Load Rhythm Pattern For 'Very hard'
        isStart = True
        rhythm = True
        patternNo = 0
        currentLines = [0, 0, 0, 0]
        offset = -275
        combo = 0
        judge = 0
        rhythmTimingPoints, rhythmNotes = readRhythmFile(f[1])
        currentNotePattern = []
        for _ in range(35):
            currentNotePattern.append(ShowingNote(None, -1, 0, False))
    while rhythm: # Rhythm Game
        if isStart:
            pygame.mixer.music.load(musics[1])
            pygame.mixer.music.play()
            start = int(round(time.time() * 1000))
            isStart = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
        noteX = [200 - 96, 200 - 32, 200 + 32, 200 + 96]
        nowTime = int(round(time.time() * 1000))
        screen.fill((0, 0, 0))
        pygame.draw.line(screen, (255, 0, 0), [5, 450], [395, 450], 30)
        if len(rhythmTimingPoints) > patternNo: # Load Pattern
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
        for i in currentNotePattern: # Show the Pattern On Screen
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
        if key[pygame.K_d] and not previousKey[0]: # Key Press
            for p in currentNotePattern:
                if p.type == 1 and p.num == currentLines[0] and p.status:
                    judge = p.HIT(nowTime - start + offset) # Judge the Judge
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
        font = pygame.font.Font("./fonts/PentagramsSalemica-B978.ttf", 28) # Show the Judge
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
        if judge != 0: # Missed
            if nowTime - start - judgeTiming <= 500:
                textRect = text.get_rect()
                textRect.centerx = 200
                textRect.centery = 300
                screen.blit(text, textRect)
        pygame.display.flip()
        if nowTime - start > rhythmTimingPoints[-1] + 5000:
            rhythm = False
        if hp < 0:
            rhythm, live = False, False
    if not live:
        break

    if difficulty == 3 and level != 0: # Story 3
        currentStory = readStory(story[2])
        playerNo = 0
        enemyNo = 0
        for i in currentStory:
            time.sleep(0.1)
            if i[0] == "Circus":
                playerNo = int(i[2])
            else:
                enemyNo = int(i[2])
            while True:
                pygame.event.pump()  # Allow pygame to handle internal actions.
                key = pygame.key.get_pressed()
                screen.fill((0, 0, 0))
                screen.blit(pygame.image.load("./img/story.png"), (5, 337))
                font = pygame.font.Font("./fonts/HeirofLightBold.ttf", 18)
                text = font.render(i[0], True, (255, 255, 255))
                screen.blit(text, (20, 350))
                font = pygame.font.Font("./fonts/HeirofLightRegular.ttf", 15)
                text = font.render(i[1], True, (0, 0, 0))
                screen.blit(text, (20, 400))

                screen.blit(playerCharacter[playerNo], (5, 80))
                screen.blit(enemy[enemyNo], (395 - 180, 80))
                screen.blit(background[0], (0, 0))
                if currentStory[-1] == i:
                    text = font.render("Space : Start", True, (0, 0, 0))
                    screen.blit(text, (300, 450))
                pygame.display.flip()
                if key[pygame.K_SPACE]:
                    break
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit(0)
    level += 1
    avoiding = True
    if level == 5:
        break

while not live: # Dead
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
    screen.blit(pygame.image.load("./img/GameOver.png"), (0, 0))
    font = pygame.font.Font("./fonts/HeirofLightBold.ttf", 24)
    text = font.render("SCORE  " + str(score).zfill(14), True, (255, 100, 100))
    textRect = text.get_rect()
    textRect.centerx = 320
    textRect.centery = 400
    screen.blit(text, textRect)
    pygame.display.flip()

while live: # Finish
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
    screen.blit(pygame.image.load("./img/GameSuccess.png"), (0, 0))
    font = pygame.font.Font("./fonts/HeirofLightBold.ttf", 24)
    text = font.render("SCORE  " + str(score).zfill(14), True, (255, 100, 255))
    textRect = text.get_rect()
    textRect.centerx = 320
    textRect.centery = 400
    screen.blit(text, textRect)
    pygame.display.flip()


while howToPlay: # How To Play
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
    screen.blit(pygame.image.load("./img/HowToPlay.png"), (0, 0))
    pygame.display.flip()
