from cvzone.HandTrackingModule import HandDetector
import numpy as np
import pygame
import cvzone
import cv2
import random
import math

STAGE_AUDIO = "./static/audios/main.mp3"
FOOD_IMG = "./static/images/cherry.png"
RED_IMG = "./static/images/red.png"
YELLOW_IMG = "./static/images/yellow.png"
BLUE_IMG = "./static/images/blue.png"



class IndexController:
    def __init__(self):
        # Load Images
        self.imgFood = cv2.imread(FOOD_IMG, cv2.IMREAD_UNCHANGED)
        self.hFood, self.wFood, _ = self.imgFood.shape
        self.foodPoint = 0, 0
        self.imgRed = cv2.imread(RED_IMG, cv2.IMREAD_UNCHANGED)
        self.hRed, self.wRed, _ = self.imgRed.shape
        self.redPoint = random.randint(100, 1000), random.randint(100, 600)
        self.imgYellow = cv2.imread(YELLOW_IMG, cv2.IMREAD_UNCHANGED)
        self.hYellow, self.wYellow, _ = self.imgYellow.shape
        self.yellowPoint = random.randint(100, 1000), random.randint(100, 600)
        self.imgBlue = cv2.imread(BLUE_IMG, cv2.IMREAD_UNCHANGED)
        self.hBlue, self.wBlue, _ = self.imgBlue.shape
        self.bluePoint = random.randint(100, 1000), random.randint(100, 600)

        self.detector = HandDetector(detectionCon=0.8, maxHands=1)
        self.randomFoodLocation()
        # self.moveMonster()
        self.points = []  # all points of the snake
        self.lengths = []  # distance between each point
        self.currentLength = 0  # total length of the snake
        self.allowedLength = 150  # total allowed Length
        self.currentHead = 0, 0  # current headig point
        self.previousHead = 0, 0  # previous headig -t NS d point
        self.gameOver = False  # game flag
        self.score = 0  # count of eaten food
        self.cap = 0  # videoCapture instance
        self.dh = 0  # display height
        self.dw = 0  # display width

        # pygame.mixer.init()
        # pygame.mixer.music.set_volume(0.5)
        # pygame.mixer.music.load(STAGE_AUDIO)
        # pygame.mixer.music.play()
        # pygame.mixer.music.pause()

    def index(self):
        self.cap = cv2.VideoCapture(0)
        self.dw = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.dh = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        while True:
            success, img = self.cap.read()
            img = cv2.flip(img, 1)
            if not success:
                break
            else:
                hands, img = self.detector.findHands(img, flipType=False)
                bg_img = np.zeros((self.dh, self.dw, 3), np.uint8)
                if hands:
                    self.currentHead = hands[0]["lmList"][8][0:2]
                    bg_img = self.update(bg_img)
                _, buffer = cv2.imencode(".jpg", bg_img)
                yield (b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + buffer.tobytes() + b"\r\n")

    def randomFoodLocation(self):
        self.foodPoint = random.randint(100, 1000), random.randint(100, 600)

    def moveMonster(self, imgMain, img, wImg, hImg, monsterPoint, i, distance):
        points = (int(monsterPoint[0] + (self.points[i - 1][0] - monsterPoint[0]) / distance), int(monsterPoint[1] + (self.points[i - 1][1] - monsterPoint[1]) / distance))
        return cvzone.overlayPNG(imgMain, img, (points[0] - wImg // 2, points[1] - hImg // 2)), points

    def mouseVector(self, imgMain, distance, i):
        if distance > 0:
            unit_vector = ((self.points[i - 1][0] - self.points[i][0]) / distance, (self.points[i - 1][1] - self.points[i][1]) / distance)
            start_angle = math.atan2(unit_vector[1], unit_vector[0]) * 180 / math.pi
            end_angle = start_angle + math.pi * 2 * (5 / 6) * 180 / math.pi
            cv2.ellipse(imgMain, self.points[i], (30, 30), 180, start_angle, end_angle, (0, 255, 255), thickness=-1)

    def calcDistance(self, i, MonsterPoints=False):
        if MonsterPoints:
            return math.sqrt((self.points[i][0] - MonsterPoints[0]) ** 2 + (self.points[i][1] - MonsterPoints[1]) ** 2)
        else:
            return math.sqrt((self.points[i - 1][0] - self.points[i][0]) ** 2 + (self.points[i - 1][1] - self.points[i][1]) ** 2)

    def update(self, imgMain):
        if self.gameOver:
            cvzone.putTextRect(imgMain, "Game Over", [int(self.dh / 2), int(self.dw / 4)], scale=7, thickness=5, offset=20, colorR=(0, 0, 0), colorT=(0, 0, 255))
            cvzone.putTextRect(imgMain, f"Your Score: {self.score}", [int(self.dh / 3), int(self.dw / 3)], scale=7, thickness=5, offset=20, colorR=(0, 0, 0), colorT=(0, 0, 255))
            self.cap.release()
            return imgMain
        else:
            px, py = self.previousHead
            cx, cy = self.currentHead
            self.points.append([cx, cy])
            distance = math.hypot(cx - px, cy - py)
            self.lengths.append(distance)
            self.currentLength += distance
            self.previousHead = cx, cy

            # Check if Pacman ate the Food
            if  self.foodPoint[0] - self.wFood // 2 < cx <  self.foodPoint[0] + self.wFood // 2 and  self.foodPoint[1] - self.hFood // 2 < cy <  self.foodPoint[1] + self.hFood // 2:
                self.randomFoodLocation()
                self.allowedLength += 50
                self.score += 1
            # Check if Monster ate the Pacman
            if self.redPoint[0] - self.wRed // 2 < cx < self.redPoint[0] + self.wRed // 2 and self.redPoint[1] - self.hRed // 2 < cy < self.redPoint[1] + self.hRed // 2 or self.yellowPoint[0] - self.wYellow // 2 < cx < self.yellowPoint[0] + self.wYellow // 2 and self.yellowPoint[1] - self.hYellow // 2 < cy < self.yellowPoint[1] + self.hYellow // 2 or self.bluePoint[0] - self.wBlue // 2 < cx < self.bluePoint[0] + self.wBlue // 2 and self.bluePoint[1] - self.hBlue // 2 < cy < self.bluePoint[1] + self.hBlue // 2:
                print("HITTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT!!!")
            if self.points:
                for i, _ in enumerate(self.points):
                # Draw Pacman
                    distance = self.calcDistance(i)
                    Reddistance = self.calcDistance(i, self.redPoint)
                    Yellowdistance = self.calcDistance(i, self.yellowPoint)
                    Bluedistance = self.calcDistance(i, self.bluePoint)
                if distance > 0:
                    self.mouseVector(imgMain, distance, i)
                # Draw monsters
                imgMain, self.redPoint = self.moveMonster(imgMain, self.imgRed, self.wRed, self.hRed, self.redPoint, i, Reddistance)
                imgMain, self.yellowPoint = self.moveMonster(imgMain, self.imgYellow, self.wYellow, self.hYellow, self.yellowPoint, i, Yellowdistance)
                imgMain, self.bluePoint = self.moveMonster(imgMain, self.imgBlue, self.wBlue, self.hBlue, self.bluePoint, i, Bluedistance)
            # Draw Food
            imgMain = cvzone.overlayPNG(imgMain, self.imgFood, (self.foodPoint[0] - self.wFood // 2, self.foodPoint[1] - self.hFood // 2))
            cvzone.putTextRect(imgMain, f"Score: {self.score}", [50, 80], scale=3, thickness=3, offset=10, colorR=(0, 0, 0), colorT=(0, 0, 255))

            # Check for Collision
            # pts = np.array(self.points[:-2], np.int32)
            # pts = pts.reshape((-1, 1, 2))
            # cv2.polylines(imgMain, [pts], False, (0, 0, 0), 3)
            # minDist = cv2.pointPolygonTest(pts, (cx, cy), True)
            # print(minDist)

            # if -1 <=
            # mFoodLocation()

            return imgMain
