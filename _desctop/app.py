from cvzone.HandTrackingModule import HandDetector
from flask import url_for
import numpy as np
import pygame
import cvzone
import cv2
import random
import math

SUCCESS_SCORE = 5
INTRO_AUDIO = url_for('static', filename='audios/intro.mp3')
STAGE_AUDIO = url_for('static', filename='audios/stage.mp3')
FAILED_AUDIO = url_for('static', filename='audios/failed.mp3')
SUCCESS_AUDIO = url_for('static', filename='audios/success.mp3')
EAT_EFFECT = url_for('static', filename='audios/eat.mp3')
FOOD_IMG = url_for('static', filename='images/cherry.mp3')
RED_IMG = url_for('static', filename='images/red.mp3')
YELLOW_IMG = url_for('static', filename='images/yellow.mp3')
BLUE_IMG = url_for('static', filename='images/blue.mp3')

class IndexController:
    def __init__(self):
        # Load Audios
        pygame.mixer.init()
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.load(INTRO_AUDIO)
        pygame.mixer.music.play()
        pygame.mixer.music.queue(STAGE_AUDIO)
        self.failed_audio = pygame.mixer.Sound(FAILED_AUDIO)
        self.success_audio = pygame.mixer.Sound(SUCCESS_AUDIO)
        self.eat_effect = pygame.mixer.Sound(EAT_EFFECT)
        # Load Images
        self.food_img = cv2.imread(FOOD_IMG, cv2.IMREAD_UNCHANGED)
        self.food_height, self.food_width, _ = self.food_img.shape
        self.food_point = 0, 0
        self.red_img = cv2.imread(RED_IMG, cv2.IMREAD_UNCHANGED)
        self.red_height, self.red_width, _ = self.red_img.shape
        self.red_point = random.randint(100, 1000), random.randint(100, 600)
        self.yellow_img = cv2.imread(YELLOW_IMG, cv2.IMREAD_UNCHANGED)
        self.yellow_height, self.wYellow, _ = self.yellow_img.shape
        self.yellow_point = random.randint(100, 1000), random.randint(100, 600)
        self.blue_img = cv2.imread(BLUE_IMG, cv2.IMREAD_UNCHANGED)
        self.blue_height, self.wBlue, _ = self.blue_img.shape
        self.blue_point = random.randint(100, 1000), random.randint(100, 600)
        # Settings
        self.points = []  # all points of the pacman
        self.current_point = 0, 0  # current headig point
        self.display_height = 0
        self.display_width = 0
        self.score = 0  # count of eaten food
        self.cap = 0  # videoCapt ure instance

    def index(self):
        self.cap = cv2.VideoCapture(0)
        self.display_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.display_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        if self.cap.isOpened():
            self.random_food_location()
            detector = HandDetector(detectionCon=0.8, maxHands=1)
            while True:
                success, img = self.cap.read()
                img = cv2.flip(img, 1)
                if not success:
                    break
                else:
                    hands, img = detector.findHands(img, flipType=False)
                    bg_img = np.zeros((self.display_height, self.display_width, 3), np.uint8)
                    if hands:
                        self.current_point = hands[0]["lmList"][8][0:2]
                        bg_img = self.update(bg_img)
                        cv2.imshow("desctop varsion", bg_img)
                        cv2.waitKey(1)

    def random_food_location(self):  # Cherry placement
        self.food_point = random.randint(100, 1000), random.randint(100, 600)

    def move_monster(self, main_img, img, img_width, img_height, monster_point, i, distance):  # Monster movements
        points = (int(monster_point[0] + (self.points[i - 1][0] - monster_point[0]) / distance), int(monster_point[1] + (self.points[i - 1][1] - monster_point[1]) / distance))
        return cvzone.overlayPNG(main_img, img, (points[0] - img_width // 2, points[1] - img_height // 2)), points

    def mouth_movement(self, main_img, distance, i):  # Mouth movement of the pacman
        if distance > 0:
            unit_vector = ((self.points[i - 1][0] - self.points[i][0]) / distance, (self.points[i - 1][1] - self.points[i][1]) / distance)
            start_angle = math.atan2(unit_vector[1], unit_vector[0]) * 180 / math.pi
            end_angle = start_angle + math.pi * 2 * (5 / 6) * 180 / math.pi
            cv2.ellipse(main_img, self.points[i], (30, 30), 180, start_angle, end_angle, (0, 255, 255), thickness=-1)

    def calculate_distance(self, i, monster_point=False):  # Distance between Monster and Pacman or Distance from past location
        if monster_point:
            return math.sqrt((self.points[i][0] - monster_point[0]) ** 2 + (self.points[i][1] - monster_point[1]) ** 2)
        else:
            return math.sqrt((self.points[i - 1][0] - self.points[i][0]) ** 2 + (self.points[i - 1][1] - self.points[i][1]) ** 2)

    def update(self, main_img):
        self.points.append([self.current_point[0], self.current_point[1]])
        # Check if Pacman ate the Food # score up
        if self.food_point[0] - self.food_width // 2 < self.current_point[0] < self.food_point[0] + self.food_width // 2 and self.food_point[1] - self.food_height // 2 < self.current_point[1] < self.food_point[1] + self.food_height // 2:
            self.eat_effect.play()
            self.score += 1
            self.random_food_location()
            if self.score == SUCCESS_SCORE:  # game clear
                cvzone.putTextRect(main_img, "Game Clear!!", [int(self.display_height / 3), int(self.display_width / 4)], scale=7, thickness=5, offset=20, colorR=(0, 0, 0), colorT=(0, 0, 255))
                cvzone.putTextRect(main_img, f"Your Score: {self.score}", [int(self.display_height / 3), int(self.display_width / 3)], scale=7, thickness=5, offset=20, colorR=(0, 0, 0), colorT=(0, 0, 255))
                pygame.mixer.music.pause()
                self.success_audio.play()
                self.cap.release()
                return main_img
        # Check if Pacman collided with monsters # game over
        if self.red_point[0] - self.red_width // 2 < self.current_point[0] < self.red_point[0] + self.red_width // 2 and self.red_point[1] - self.red_height // 2 < self.current_point[1] < self.red_point[1] + self.red_height // 2 or self.yellow_point[0] - self.wYellow // 2 < self.current_point[0] < self.yellow_point[0] + self.wYellow // 2 and self.yellow_point[1] - self.yellow_height // 2 < self.current_point[1] < self.yellow_point[1] + self.yellow_height // 2 or self.blue_point[0] - self.wBlue // 2 < self.current_point[0] < self.blue_point[0] + self.wBlue // 2 and self.blue_point[1] - self.blue_height // 2 < self.current_point[1] < self.blue_point[1] + self.blue_height // 2:
            cvzone.putTextRect(main_img, "Game Over", [int(self.display_height / 2), int(self.display_width / 4)], scale=7, thickness=5, offset=20, colorR=(0, 0, 0), colorT=(0, 0, 255))
            cvzone.putTextRect(main_img, f"Your Score: {self.score}", [int(self.display_height / 3), int(self.display_width / 3)], scale=7, thickness=5, offset=20, colorR=(0, 0, 0), colorT=(0, 0, 255))
            pygame.mixer.music.pause()
            self.failed_audio.play()
            self.cap.release()
            return main_img
        if self.points:
            for i, _ in enumerate(self.points):
                self_distance = self.calculate_distance(i)
                red_distance = self.calculate_distance(i, self.red_point)
                yellow_distance = self.calculate_distance(i, self.yellow_point)
                blue_distance = self.calculate_distance(i, self.blue_point)
            # Draw pacman
            self.mouth_movement(main_img, self_distance, i)
            # Draw monsters
            main_img, self.red_point = self.move_monster(main_img, self.red_img, self.red_width, self.red_height, self.red_point, i, red_distance)
            main_img, self.yellow_point = self.move_monster(main_img, self.yellow_img, self.wYellow, self.yellow_height, self.yellow_point, i, yellow_distance)
            main_img, self.blue_point = self.move_monster(main_img, self.blue_img, self.wBlue, self.blue_height, self.blue_point, i, blue_distance)
        # Draw Food
        main_img = cvzone.overlayPNG(main_img, self.food_img, (self.food_point[0] - self.food_width // 2, self.food_point[1] - self.food_height // 2))
        # Draw score
        cvzone.putTextRect(main_img, f"Score: {self.score}", [50, 80], scale=3, thickness=3, offset=10, colorR=(0, 0, 0), colorT=(0, 0, 255))

        return main_img


IndexController().index()
