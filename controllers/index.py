from cvzone.HandTrackingModule import HandDetector
from pydub.playback import _play_with_simpleaudio
from scipy.spatial.distance import euclidean
from pydub import AudioSegment
import numpy as np
import cvzone
import cv2
import random
import copy
import os


class IndexController:
    STATIC_DIR = os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir), "static")
    IMAGES_DIR = os.path.join(STATIC_DIR, "images")
    AUDIOS_DIR = os.path.join(STATIC_DIR, "audios")

    STAGE_AUDIO = f"{AUDIOS_DIR}/stage.mp3"
    FAILED_AUDIO = f"{AUDIOS_DIR}/failed.mp3"
    SUCCESS_AUDIO = f"{AUDIOS_DIR}/success.mp3"
    COIN_EFFECT = f"{AUDIOS_DIR}/coin.mp3"
    COIN_IMG = f"{IMAGES_DIR}/coin.png"
    RED_IMG = f"{IMAGES_DIR}/king_boo.png"
    YELLOW_IMG = f"{IMAGES_DIR}/boo.png"
    BLUE_IMG = f"{IMAGES_DIR}/boo.png"
    WALK_IMG = f"{IMAGES_DIR}/walk.png"
    STOP_IMG = f"{IMAGES_DIR}/stop.png"
    SUCCESS_SCORE = 3

    def __init__(self):
        # Load Audios
        self.stage_audio = _play_with_simpleaudio(AudioSegment.from_file(self.STAGE_AUDIO))
        self.failed_audio = AudioSegment.from_file(self.FAILED_AUDIO)
        self.success_audio = AudioSegment.from_file(self.SUCCESS_AUDIO)
        self.coin_effect = AudioSegment.from_file(self.COIN_EFFECT)
        # Load Images
        self.coin_img = cv2.imread(self.COIN_IMG, cv2.IMREAD_UNCHANGED)
        self.red_img = cv2.imread(self.RED_IMG, cv2.IMREAD_UNCHANGED)
        self.yellow_img = cv2.imread(self.YELLOW_IMG, cv2.IMREAD_UNCHANGED)
        self.blue_img = cv2.imread(self.BLUE_IMG, cv2.IMREAD_UNCHANGED)
        self.walk_img = cv2.imread(self.WALK_IMG, cv2.IMREAD_UNCHANGED)
        self.stop_img = cv2.imread(self.STOP_IMG, cv2.IMREAD_UNCHANGED)
        # Settings
        self.red_point = random.randint(100, 1000), random.randint(100, 600)
        self.yellow_point = random.randint(100, 1000), random.randint(100, 600)
        self.blue_point = random.randint(100, 1000), random.randint(100, 600)
        self.coin_point = random.randint(100, 1000), random.randint(100, 600)
        self.red_height, self.red_width, _ = self.red_img.shape
        self.yellow_height, self.yellow_width, _ = self.yellow_img.shape
        self.blue_height, self.blue_width, _ = self.blue_img.shape
        self.coin_height, self.coin_width, _ = self.coin_img.shape
        self.detector = HandDetector(detectionCon=0.8, maxHands=1)
        self.points = []  # Luigi's current and previous positions
        self.current_point = 0, 0  # current Luigi's point
        self.display_height = 0
        self.display_width = 0
        self.score = 0
        self.map = 0, 0, 0
        self.flag = True

    def index(self):
        cap = cv2.VideoCapture(0)
        self.display_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.display_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.map = np.zeros((self.display_height, self.display_width, 3), np.uint8)
        if cap.isOpened():
            while True:
                success, img = cap.read()
                if not success:
                    break
                else:
                    hands, _ = self.detector.findHands(cv2.flip(img, 1), flipType=False)
                    map = copy.copy(self.map)
                    if hands:
                        self.current_point = hands[0]["lmList"][8][0:2]
                        map = self.update(map, cap)
                    _, buffer = cv2.imencode(".jpg", map)
                    yield (b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + buffer.tobytes() + b"\r\n")

    def scoreUp(self):
        _play_with_simpleaudio(self.coin_effect)
        self.coin_point = random.randint(10, 1000), random.randint(10, 600)
        self.score += 1
        return self.score

    def gameClear(self, main_img, cap):
        cvzone.putTextRect(main_img, "Game Clear!!", [int(self.display_height / 3), int(self.display_width / 4)], scale=7, thickness=5, offset=20, colorR=(0, 0, 0), colorT=(0, 0, 255))
        cvzone.putTextRect(main_img, f"Your Score: {self.score}", [int(self.display_height / 3), int(self.display_width / 3)], scale=7, thickness=5, offset=20, colorR=(0, 0, 0), colorT=(0, 0, 255))
        self.stage_audio.stop()
        _play_with_simpleaudio(self.success_audio)
        cap.release()
        return main_img

    def gameOver(self, main_img, cap):
        cvzone.putTextRect(main_img, "Game Over", [int(self.display_height / 2), int(self.display_width / 4)], scale=7, thickness=5, offset=20, colorR=(0, 0, 0), colorT=(0, 0, 255))
        cvzone.putTextRect(main_img, f"Your Score: {self.score}", [int(self.display_height / 3), int(self.display_width / 3)], scale=7, thickness=5, offset=20, colorR=(0, 0, 0), colorT=(0, 0, 255))
        self.stage_audio.stop()
        _play_with_simpleaudio(self.failed_audio)
        cap.release()
        return main_img

    def move_boo(self, main_img, img, monster_point, img_width, img_height, i):  # Monster movements
        img = cv2.flip(img, 1) if self.points[i][0] < monster_point[0] else img
        distance = euclidean(self.points[i], monster_point)
        points = (int(monster_point[0] + (self.points[i - 1][0] - monster_point[0]) / distance), int(monster_point[1] + (self.points[i - 1][1] - monster_point[1]) / distance))
        main_img = cvzone.overlayPNG(main_img, img, (points[0] - img_width // 2, points[1] - img_height // 2))
        return main_img, points

    def walking_animation(self, main_img, i):
        distance = euclidean(self.points[i - 1], self.points[i])
        if distance > 0:
            img = (self.walk_img, self.stop_img)[random.randint(0, 1)] if self.points[i][0] != self.points[i - 1][0] else self.stop_img
            # print(main_img.shape == img.shape, main_img.shape ,img.shape)
            img = cv2.flip(img, 1) if self.points[i][0] > min([self.red_point[0], self.yellow_point[0], self.blue_point[0]]) else img
            main_img = cvzone.overlayPNG(main_img, img, (self.points[i][0] - img.shape[0] // 2, self.points[i][1] - img.shape[1] // 2))
        return main_img

    def update(self, main_img, cap):
        # Save Luigi's current and previous positions
        self.points[1:2] = np.array([[self.current_point[0], self.current_point[1]]])
        # Check if Luigi got the coin
        if self.coin_point[0] - self.coin_width // 2 < self.current_point[0] < self.coin_point[0] + self.coin_width // 2 and self.coin_point[1] - self.coin_height // 2 < self.current_point[1] < self.coin_point[1] + self.coin_height // 2:
            if self.scoreUp() == self.SUCCESS_SCORE:
                return self.gameClear(main_img, cap)
        # Check if Luigi collided with boo
        if self.red_point[0] - self.red_width // 2 < self.current_point[0] < self.red_point[0] + self.red_width // 2 and self.red_point[1] - self.red_height // 2 < self.current_point[1] < self.red_point[1] + self.red_height // 2 or self.yellow_point[0] - self.yellow_width // 2 < self.current_point[0] < self.yellow_point[0] + self.yellow_width // 2 and self.yellow_point[1] - self.yellow_height // 2 < self.current_point[1] < self.yellow_point[1] + self.yellow_height // 2 or self.blue_point[0] - self.blue_width // 2 < self.current_point[0] < self.blue_point[0] + self.blue_width // 2 and self.blue_point[1] - self.blue_height // 2 < self.current_point[1] < self.blue_point[1] + self.blue_height // 2:
            return self.gameOver(main_img, cap)
        if self.points:
            for i, _ in enumerate(self.points):
                if i > 0:
                    # Draw Boo
                    main_img, self.red_point = self.move_boo(main_img, self.red_img, self.red_point, self.red_width, self.red_height, i)
                    main_img, self.yellow_point = self.move_boo(main_img, self.yellow_img, self.yellow_point, self.yellow_width, self.yellow_height, i)
                    main_img, self.blue_point = self.move_boo(main_img, self.blue_img, self.blue_point, self.blue_width, self.blue_height, i)
                    # Draw Luigi
                    main_img = self.walking_animation(main_img, i)
        # Draw coin
        main_img = cvzone.overlayPNG(main_img, self.coin_img, (self.coin_point[0] - self.coin_width // 2, self.coin_point[1] - self.coin_height // 2))
        # Draw score
        cvzone.putTextRect(main_img, f"Score: {self.score}", [50, 80], scale=3, thickness=3, offset=10, colorR=(0, 0, 0), colorT=(0, 0, 255))

        return main_img
