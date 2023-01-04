from cvzone.HandTrackingModule import HandDetector
from pydub.playback import _play_with_simpleaudio
from scipy.spatial.distance import euclidean
from pydub import AudioSegment
from numba import jit
import numpy as np
import cvzone
import cv2
import random
import copy
import math
import os


class IndexController:
    STATIC_DIR = os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir), "static")
    IMAGES_DIR = os.path.join(STATIC_DIR, "images")
    AUDIOS_DIR = os.path.join(STATIC_DIR, "audios")

    STAGE_AUDIO = f"{AUDIOS_DIR}/stage.mp3"
    FAILED_AUDIO = f"{AUDIOS_DIR}/failed.mp3"
    SUCCESS_AUDIO = f"{AUDIOS_DIR}/success.mp3"
    EAT_EFFECT = f"{AUDIOS_DIR}/eat.mp3"
    FOOD_IMG = f"{IMAGES_DIR}/cherry.png"
    RED_IMG = f"{IMAGES_DIR}/red.png"
    YELLOW_IMG = f"{IMAGES_DIR}/yellow.png"
    BLUE_IMG = f"{IMAGES_DIR}/blue.png"
    SUCCESS_SCORE = 10

    def __init__(self):
        # Load Audios
        self.stage_audio = _play_with_simpleaudio(AudioSegment.from_file(self.STAGE_AUDIO))
        self.failed_audio = AudioSegment.from_file(self.FAILED_AUDIO)
        self.success_audio = AudioSegment.from_file(self.SUCCESS_AUDIO)
        self.eat_effect = AudioSegment.from_file(self.EAT_EFFECT)
        # Load Images
        self.food_img = cv2.imread(self.FOOD_IMG, cv2.IMREAD_UNCHANGED)
        self.red_img = cv2.imread(self.RED_IMG, cv2.IMREAD_UNCHANGED)
        self.yellow_img = cv2.imread(self.YELLOW_IMG, cv2.IMREAD_UNCHANGED)
        self.blue_img = cv2.imread(self.BLUE_IMG, cv2.IMREAD_UNCHANGED)
        self.red_point = random.randint(100, 1000), random.randint(100, 600)
        self.blue_point = random.randint(100, 1000), random.randint(100, 600)
        self.yellow_point = random.randint(100, 1000), random.randint(100, 600)
        # Settings
        self.food_height, self.food_width, _ = self.food_img.shape
        self.red_height, self.red_width, _ = self.red_img.shape
        self.yellow_height, self.yellow_width, _ = self.yellow_img.shape
        self.blue_height, self.blue_width, _ = self.blue_img.shape
        self.points = []  # all points of the pacman
        self.current_point = 0, 0  # current headig point
        self.food_point = 0, 0
        self.display_height = 0
        self.display_width = 0
        self.score = 0
        self.map = 0, 0, 0

    # @jit
    def index(self):
        cap = cv2.VideoCapture(0)
        self.display_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.display_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.map = np.zeros((self.display_height, self.display_width, 3), np.uint8)
        if cap.isOpened():
            self.random_food_location()
            detector = HandDetector(detectionCon=0.8, maxHands=1)
            while True:
                success, img = cap.read()
                img = cv2.flip(img, 1)
                if not success:
                    break
                else:
                    hands, img = detector.findHands(img, flipType=False)
                    map = copy.copy(self.map)
                    if hands:
                        self.current_point = hands[0]["lmList"][8][0:2]
                        map = self.update(map, cap)
                    cv2.imshow("desctop varsion", map)
                    cv2.waitKey(1)

    # @jit
    def random_food_location(self):  # Cherry placement
        self.food_point = random.randint(100, 1000), random.randint(100, 600)

    # @jit
    def move_monster(self, main_img, img, img_width, img_height, monster_point, i):  # Monster movements
        distance = euclidean(self.points[i], monster_point)
        points = (int(monster_point[0] + (self.points[i - 1][0] - monster_point[0]) / distance), int(monster_point[1] + (self.points[i - 1][1] - monster_point[1]) / distance))
        main_img = cvzone.overlayPNG(main_img, img, (points[0] - img_width // 2, points[1] - img_height // 2))
        return main_img, points

    # @jit
    def mouth_movement(self, main_img, i):  # Mouth movement of the pacman
        distance = euclidean(self.points[i - 1], self.points[i])
        if distance > 0:
            unit_vector = ((self.points[i - 1][0] - self.points[i][0]) / distance, (self.points[i - 1][1] - self.points[i][1]) / distance)
            start_angle = np.arctan2(unit_vector[1], unit_vector[0]) * 180 / math.pi
            end_angle = start_angle + math.pi * 2 * (5 / 6) * 180 / math.pi
            cv2.ellipse(main_img, self.points[i], (30, 30), 180, start_angle, end_angle, (0, 255, 255), thickness=-1)

    # @jit
    def update(self, main_img, cap):
        self.points[2:3] = np.array([[self.current_point[0], self.current_point[1]]])
        # Check if Pacman ate the Food # score up
        if self.food_point[0] - self.food_width // 2 < self.current_point[0] < self.food_point[0] + self.food_width // 2 and self.food_point[1] - self.food_height // 2 < self.current_point[1] < self.food_point[1] + self.food_height // 2:
            _play_with_simpleaudio(self.eat_effect)
            self.score += 1
            self.random_food_location()
            if self.score == self.SUCCESS_SCORE:  # game clear
                cvzone.putTextRect(main_img, "Game Clear!!", [int(self.display_height / 3), int(self.display_width / 4)], scale=7, thickness=5, offset=20, colorR=(0, 0, 0), colorT=(0, 0, 255))
                cvzone.putTextRect(main_img, f"Your Score: {self.score}", [int(self.display_height / 3), int(self.display_width / 3)], scale=7, thickness=5, offset=20, colorR=(0, 0, 0), colorT=(0, 0, 255))
                self.stage_audio.stop()
                _play_with_simpleaudio(self.success_audio)
                cap.release()
                return main_img
        # Check if Pacman collided with monsters # game over
        if self.red_point[0] - self.red_width // 2 < self.current_point[0] < self.red_point[0] + self.red_width // 2 and self.red_point[1] - self.red_height // 2 < self.current_point[1] < self.red_point[1] + self.red_height // 2 or self.yellow_point[0] - self.yellow_width // 2 < self.current_point[0] < self.yellow_point[0] + self.yellow_width // 2 and self.yellow_point[1] - self.yellow_height // 2 < self.current_point[1] < self.yellow_point[1] + self.yellow_height // 2 or self.blue_point[0] - self.blue_width // 2 < self.current_point[0] < self.blue_point[0] + self.blue_width // 2 and self.blue_point[1] - self.blue_height // 2 < self.current_point[1] < self.blue_point[1] + self.blue_height // 2:
            cvzone.putTextRect(main_img, "Game Over", [int(self.display_height / 2), int(self.display_width / 4)], scale=7, thickness=5, offset=20, colorR=(0, 0, 0), colorT=(0, 0, 255))
            cvzone.putTextRect(main_img, f"Your Score: {self.score}", [int(self.display_height / 3), int(self.display_width / 3)], scale=7, thickness=5, offset=20, colorR=(0, 0, 0), colorT=(0, 0, 255))
            self.stage_audio.stop()
            _play_with_simpleaudio(self.failed_audio)
            cap.release()
            return main_img
        if self.points:
            for i, _ in enumerate(self.points):
                # Draw monsters
                main_img, self.red_point = self.move_monster(main_img, self.red_img, self.red_width, self.red_height, self.red_point, i)
                main_img, self.yellow_point = self.move_monster(main_img, self.yellow_img, self.yellow_width, self.yellow_height, self.yellow_point, i)
                main_img, self.blue_point = self.move_monster(main_img, self.blue_img, self.blue_width, self.blue_height, self.blue_point, i)
            # Draw pacman
            self.mouth_movement(main_img, i)
        # Draw Food
        main_img = cvzone.overlayPNG(main_img, self.food_img, (self.food_point[0] - self.food_width // 2, self.food_point[1] - self.food_height // 2))
        # Draw score
        cvzone.putTextRect(main_img, f"Score: {self.score}", [50, 80], scale=3, thickness=3, offset=10, colorR=(0, 0, 0), colorT=(0, 0, 255))

        return main_img


IndexController().index()
