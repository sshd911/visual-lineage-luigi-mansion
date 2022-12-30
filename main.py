import mediapipe as np
import numpy as np
import cvzone
import cv2
import random
import math

class Main:
    def __init__(self, pathFood):
        self.points = []  # all points of the snake
        self.lengths = []  # distance between each point
        self.currentLength = 0  # total length of the snake
        self.allowedLength = 150  # total allowed Length
        self.previousHead = 0, 0  # previous head point
        self.imgFood = cv2.imread(pathFood, cv2.IMREAD_UNCHANGED)
        self.hFood, self.wFood, _ = self.imgFood.shape
        self.foodPoint = 0, 0
        self.randomFoodLocation()
        self.score = 0
        self.gameOver = False

    def randomFoodLocation(self):
        self.foodPoint = random.randint(100, 1000), random.randint(100, 600)

    def update(self, imgMain, currentHead, dh, dw):
        if self.gameOver:
            cvzone.putTextRect(imgMain, "Game Over", [int(dh/2), int(dw/4)], scale=7, thickness=5, offset=20, colorR=(0,0,0), colorT=(0,0,255))
            cvzone.putTextRect(imgMain, f"Your Score: {self.score}", [int(dh/3), int(dw/3)], scale=7, thickness=5, offset=20, colorR=(0,0,0), colorT=(0,0,255))
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

            # Check if snake ate the Food
            rx, ry = self.foodPoint
            if (
                rx - self.wFood // 2 < cx < rx + self.wFood // 2
                and ry - self.hFood // 2 < cy < ry + self.hFood // 2
            ):
                self.randomFoodLocation()
                self.allowedLength += 50
                self.score += 1
            # Draw Snake
            if self.points:
                for i, point in enumerate(self.points):
                    if i != 0:
                        cv2.line(
                            imgMain, self.points[i - 1], self.points[i], (0, 0, 255), 20
                        )
                cv2.circle(imgMain, self.points[-1], 20, (0, 255, 0), cv2.FILLED)

            # Draw Food
            imgMain = cvzone.overlayPNG(
                imgMain, self.imgFood, (rx - self.wFood // 2, ry - self.hFood // 2)
            )

            cvzone.putTextRect(
                imgMain,
                f"Score: {self.score}",
                [50, 80],
                scale=3,
                thickness=3,
                offset=10,
                colorR=(0,0,0),
                colorT=(0,0,255)
            )

            # Check for Collision
            pts = np.array(self.points[:-2], np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(imgMain, [pts], False, (0, 255, 0), 3)
            minDist = cv2.pointPolygonTest(pts, (cx, cy), True)

            if -1 <= minDist <= 1:
                print("Hit")
                self.gameOver = True
                self.points = []  # all points of the snake
                self.lengths = []  # distance between each point
                self.currentLength = 0  # total length of the snake
                self.allowedLength = 150  # total allowed Length
                self.previousHead = 0, 0  # previous head point
                self.randomFoodLocation()

        return imgMain
