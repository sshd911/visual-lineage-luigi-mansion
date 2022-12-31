from cvzone.HandTrackingModule import HandDetector
import numpy as np
import pygame
import cvzone
import cv2
import random
import math

FOOD_IMG = "./static/images/food.png"
STAGE_AUDIO = "./static/audios/main.mp3"


class IndexController:
    def __init__(self):
        self.points = []  # all points of the snake
        self.lengths = []  # distance between each point
        self.currentLength = 0  # total length of the snake
        self.allowedLength = 150  # total allowed Length
        self.previousHead = 0, 0  # previous headig -t NS d point
        self.imgFood = cv2.imread(FOOD_IMG, cv2.IMREAD_UNCHANGED)
        self.hFood, self.wFood, _ = self.imgFood.shape
        self.foodPoint = 0, 0
        self.randomFoodLocation()
        self.score = 0
        self.gameOver = False
        self.detector = HandDetector(detectionCon=0.8, maxHands=1)
        # pygame.mixer.init()
        # pygame.mixer.music.set_volume(0.5)
        # pygame.mixer.music.load(STAGE_AUDIO)
        # pygame.mixer.music.play()
        # pygame.mixer.music.pause()

    def index(self):
        cap = cv2.VideoCapture(0)
        dw = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        dh = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        if cap.isOpened():
            while True:
                _, img = cap.read()
                img = cv2.flip(img, 1)
                hands, img = self.detector.findHands(img, flipType=False)
                # bg_img = np.zeros((dh, dw, 3), np.uint8)
                if hands:
                    lmList = hands[0]["lmList"]
                    pointIndex = lmList[8][0:2]
                    img = self.update(img, pointIndex, dh, dw, cap)
                    # bg_img = self.update(bg_img, pointIndex, dh, dw, cap)
                _, buffer = cv2.imencode(".jpg", img)
                # _, buffer = cv2.imencode(".jpg", bg_img)
                yield (b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + buffer.tobytes() + b"\r\n")

    def randomFoodLocation(self):
        self.foodPoint = random.randint(100, 1000), random.randint(100, 600)

    def update(self, imgMain, currentHead, dh, dw, cap):
        if self.gameOver:
            cvzone.putTextRect(imgMain, "Game Over", [int(dh / 2), int(dw / 4)], scale=7, thickness=5, offset=20, colorR=(0, 0, 0), colorT=(0, 0, 255))
            cvzone.putTextRect(imgMain, f"Your Score: {self.score}", [int(dh / 3), int(dw / 3)], scale=7, thickness=5, offset=20, colorR=(0, 0, 0), colorT=(0, 0, 255))
            cap.release()
            cv2.destroyAllWindows()
            return imgMain
        else:
            px, py = self.previousHead
            cx, cy = currentHead
            self.points.append([cx, cy])
            distance = math.hypot(cx - px, cy - py)
            self.lengths.append(distance)
            self.currentLength += distance
            self.previousHead = cx, cy

            # Length Reduction
            if self.currentLength > self.allowedLength:
                for i, length in enumerate(self.lengths):
                    self.currentLength -= length
                    self.lengths.pop(i)
                    self.points.pop(i)
                    if self.currentLength < self.allowedLength:
                        break

            # Check if Packman ate the Food
            rx, ry = self.foodPoint
            if rx - self.wFood // 2 < cx < rx + self.wFood // 2 and ry - self.hFood // 2 < cy < ry + self.hFood // 2:
                self.randomFoodLocation()
                self.allowedLength += 50
                self.score += 1
            # Draw Packman
            if self.points:
                for i, point in enumerate(self.points):
                    if i != 0:
                        cv2.line(imgMain, self.points[i - 1], self.points[i], (0, 0, 0), 20)
                distance = math.sqrt((self.points[i - 1][0] - self.points[i][0]) ** 2 + (self.points[i - 1][1] - self.points[i][1]) ** 2)
                if distance > 0:
                    unit_vector = ((self.points[i - 1][0] - self.points[i][0]) / distance, (self.points[i - 1][1] - self.points[i][1]) / distance)
                    start_angle = math.atan2(unit_vector[1], unit_vector[0]) * 180 / math.pi
                    end_angle = start_angle + math.pi * 2 * (5 / 6) * 180 / math.pi
                    cv2.ellipse(imgMain, self.points[i], (30, 30), 180, start_angle, end_angle, (0, 255, 255), thickness=-1)

            # Draw Food
            imgMain = cvzone.overlayPNG(imgMain, self.imgFood, (rx - self.wFood // 2, ry - self.hFood // 2))
            cvzone.putTextRect(imgMain, f"Score: {self.score}", [50, 80], scale=3, thickness=3, offset=10, colorR=(0, 0, 0), colorT=(0, 0, 255))

            # Check for Collision
            pts = np.array(self.points[:-2], np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(imgMain, [pts], False, (0, 0, 0), 3)
            minDist = cv2.pointPolygonTest(pts, (cx, cy), True)
            # print(minDist)

            if -1 <= minDist <= 1:
                # print("Hit")
                self.gameOver = True
                self.points = []  # all points of the snake
                self.lengths = []  # distance between each point
                self.currentLength = 0  # total length of the snake
                self.allowedLength = 150  # total allowed Length
                self.previousHead = 0, 0  # previous head point
                self.randomFoodLocation()

            return imgMain
