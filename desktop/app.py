from cvzone.HandTrackingModule import HandDetector
from pydub.playback import _play_with_simpleaudio
from scipy.spatial.distance import euclidean
from pydub import AudioSegment
import numpy as np
import cvzone
import cv2
import keyboard
import random
import copy
import os


class LuigiMansion:
    STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
    IMAGES_DIR = os.path.join(STATIC_DIR, "images")
    AUDIOS_DIR = os.path.join(STATIC_DIR, "audios")

    STAGE_AUDIO = f"{AUDIOS_DIR}/stage.mp3"
    FAILED_AUDIO = f"{AUDIOS_DIR}/failed.mp3"
    SUCCESS_AUDIO = f"{AUDIOS_DIR}/success.mp3"
    COIN_EFFECT = f"{AUDIOS_DIR}/coin.mp3"
    COIN_IMG = f"{IMAGES_DIR}/coin.png"
    KING_BOO_IMG = f"{IMAGES_DIR}/king_boo.png"
    BOO_IMG = f"{IMAGES_DIR}/boo.png"
    MARIO_BOO_IMG = f"{IMAGES_DIR}/mario_boo.png"
    WALK_IMG = f"{IMAGES_DIR}/walk.png"
    STOP_IMG = f"{IMAGES_DIR}/stop.png"
    SUCCESS_SCORE = 10
    MAGNIFICATION = 1.2

    def __init__(self):
        # Load Audios
        self.stage_audio = _play_with_simpleaudio(AudioSegment.from_file(self.STAGE_AUDIO))
        self.failed_audio = AudioSegment.from_file(self.FAILED_AUDIO)
        self.success_audio = AudioSegment.from_file(self.SUCCESS_AUDIO)
        self.coin_effect = AudioSegment.from_file(self.COIN_EFFECT)
        # Load Images
        self.coin_img = cv2.imread(self.COIN_IMG, cv2.IMREAD_UNCHANGED)
        self.king_boo_img = cv2.imread(self.KING_BOO_IMG, cv2.IMREAD_UNCHANGED)
        self.boo_img = cv2.imread(self.BOO_IMG, cv2.IMREAD_UNCHANGED)
        self.mario_boo_img = cv2.imread(self.MARIO_BOO_IMG, cv2.IMREAD_UNCHANGED)
        self.walk_img = cv2.imread(self.WALK_IMG, cv2.IMREAD_UNCHANGED)
        self.stop_img = cv2.imread(self.STOP_IMG, cv2.IMREAD_UNCHANGED)
        # Settings
        keyboard.on_press(self.on_key_pressed)
        self.detector = HandDetector(detectionCon=0.8, maxHands=1)
        self.king_boo_point = random.randint(100, 1000), random.randint(100, 600)
        self.boo_point = random.randint(100, 1000), random.randint(100, 600)
        self.mario_boo_point = random.randint(100, 1000), random.randint(100, 600)
        self.coin_point = random.randint(100, 1000), random.randint(100, 600)
        self.current_point = random.randint(100, 1000), random.randint(100, 600)  # current Luigi's point
        self.king_boo_width, self.king_boo_height, _ = self.king_boo_img.shape
        self.boo_width, self.boo_height, _ = self.boo_img.shape
        self.mario_boo_width, self.mario_boo_height, _ = self.mario_boo_img.shape
        self.coin_width, self.coin_height, _ = self.coin_img.shape
        self.luigi_width, self.luigi_height, _ = self.walk_img.shape
        self.points = []  # Luigi's current and previous positions
        self.display_height = 0
        self.display_width = 0
        self.main_img = 0
        self.score = 0
        self.key_pressed = False
        self.direction = ["LEFT", "RIGHT"]

    def index(self):
        cap = cv2.VideoCapture(0)
        self.display_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.display_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.main_img = np.zeros((self.display_height, self.display_width, 3), np.uint8)
        if cap.isOpened():
            while True:
                success, img = cap.read()
                if not success:
                    break
                else:
                    hands, _ = self.detector.findHands(cv2.flip(img, 1), flipType=False)
                    main_img = copy.copy(self.main_img)
                    if hands:
                        self.current_point = hands[0]["lmList"][8][0:2]
                    main_img = self.update(main_img, cap)
                    cv2.imshow("desctop varsion", main_img)
                    cv2.waitKey(1)

    def update(self, main_img, cap):
        # Save Luigi's current and previous positions
        if len(self.points) == 2:
            self.points[0] = self.points[1]
        self.points[1:2] = np.array([self.current_point])
        # Check if Luigi collided with boo
        if (self.king_boo_point[0] - self.king_boo_width // 2 < self.current_point[0] < self.king_boo_point[0] + self.luigi_width // 2) and (self.king_boo_point[1] - self.king_boo_height // 2 < self.current_point[1] < self.king_boo_point[1] + self.luigi_height // 2) or (self.boo_point[0] - self.boo_width // 2 < self.current_point[0] < self.boo_point[0] + self.luigi_width // 2) and (self.boo_point[1] - self.boo_height // 2 < self.current_point[1] < self.boo_point[1] + self.luigi_height // 2) or (self.mario_boo_point[0] - self.mario_boo_width // 2 < self.current_point[0] < self.mario_boo_point[0] + self.luigi_width // 2) and (self.mario_boo_point[1] - self.mario_boo_height // 2 < self.current_point[1] < self.mario_boo_point[1] + self.luigi_height // 2):
            self.filed(main_img, cap)
        # Check if Luigi got the coin
        if (self.coin_point[0] - self.coin_width // 2 < self.current_point[0] < self.coin_point[0] + self.coin_width // 2 or self.current_point[0] - self.luigi_width // 2 < self.coin_point[0] < self.current_point[0] + self.luigi_width // 2) and (self.coin_point[1] - self.coin_height // 2 < self.current_point[1] < self.coin_point[1] + self.coin_height // 2 or self.current_point[1] - self.luigi_height // 2 < self.coin_point[1] < self.current_point[1] + self.luigi_height // 2):
            # Check if score reached the success score
            if self.score_up() == self.SUCCESS_SCORE:
                self.success(main_img, cap)
        for i, _ in enumerate(self.points):
            if i > 0:
                # Draw Boo
                main_img, self.king_boo_point = self.boo_animation(main_img, self.king_boo_img, self.king_boo_point, self.king_boo_width, self.king_boo_height, i)
                main_img, self.boo_point = self.boo_animation(main_img, self.boo_img, self.boo_point, self.boo_width, self.boo_height, i)
                main_img, self.mario_boo_point = self.boo_animation(main_img, self.mario_boo_img, self.mario_boo_point, self.mario_boo_width, self.mario_boo_height, i)
                # Draw Luigi
                main_img = self.luigi_animation(main_img, i)
        return self.draws(main_img)

    def on_key_pressed(self, _):
        self.key_pressed = not self.key_pressed
        self.walk_img = cv2.flip(self.walk_img, 1)
        self.stop_img = cv2.flip(self.stop_img, 1)

    def boo_animation(self, main_img, img, boo_point, img_width, img_height, i):
        if 0 < boo_point[0] - img_width // 2 and boo_point[0] + img_width // 2 < self.display_width and 0 < boo_point[1] - img_height // 2 and boo_point[1] + img_height // 2 < self.display_height:
            if self.key_pressed == self.direction.index("LEFT"):
                if self.points[i][0] < boo_point[0]:
                    img = cv2.flip(img, 1)
                    distance = euclidean(self.points[i], boo_point)
                    if distance > 0:
                        boo_point = (int(boo_point[0] + (self.points[i][0] - boo_point[0]) / (distance / 2)), int(boo_point[1] + (self.points[i][1] - boo_point[1]) / (distance / 2)))
            if self.key_pressed == self.direction.index("RIGHT"):
                if self.points[i][0] > boo_point[0]:
                    img = cv2.flip(img, 1)
                    distance = euclidean(self.points[i], boo_point)
                    if distance > 0:
                        boo_point = (int(boo_point[0] + (self.points[i][0] - boo_point[0]) / (distance / 2)), int(boo_point[1] + (self.points[i][1] - boo_point[1]) / (distance / 2)))
            main_img = cvzone.overlayPNG(main_img, img, (boo_point[0] - img_width // 2, boo_point[1] - img_height // 2))
        return main_img, boo_point

    def luigi_animation(self, main_img, i):
        img = (self.walk_img, self.stop_img)[random.randint(0, 1)] if self.points[i][0] != self.points[i - 1][0] else self.stop_img
        self.luigi_width, self.luigi_height, _ = img.shape
        if 0 < self.points[i][0] - self.luigi_width // 2 and self.points[i][0] + self.luigi_width // 2 < self.display_width and 0 < self.points[i][1] - self.luigi_height // 2 and self.points[i][1] + self.luigi_height // 2 < self.display_height:
            main_img = cvzone.overlayPNG(main_img, img, (self.points[i][0] - self.luigi_width // 2, self.points[i][1] - self.luigi_height // 2))
        else:
            self.points[i] = self.points[i - 1]
            main_img = cvzone.overlayPNG(main_img, img, (self.points[i][0] - self.luigi_width // 2, self.points[i][1] - self.luigi_height // 2))
        return main_img

    def score_up(self):
        self.score += 1
        _play_with_simpleaudio(self.coin_effect)
        self.coin_point = random.randint(0 + self.coin_width // 2, self.display_width - self.coin_width // 2), random.randint(0 + self.coin_height // 2, self.display_height - self.coin_height // 2)
        self.walk_img = cv2.resize(self.walk_img, (int(self.walk_img.shape[1] * self.MAGNIFICATION), int(self.walk_img.shape[0] * self.MAGNIFICATION)))
        self.stop_img = cv2.resize(self.stop_img, (int(self.stop_img.shape[1] * self.MAGNIFICATION), int(self.stop_img.shape[0] * self.MAGNIFICATION)))
        return self.score

    def draws(self, main_img):
        cvzone.putTextRect(main_img, f"Score: {self.score}/{self.SUCCESS_SCORE}", [50, 80], scale=3, thickness=3, offset=10, colorR=(0, 0, 0), colorT=(0, 0, 255))
        return cvzone.overlayPNG(main_img, self.coin_img, (self.coin_point[0] - self.coin_width // 2, self.coin_point[1] - self.coin_height // 2))

    def success(self, main_img, cap):
        cvzone.putTextRect(main_img, "Game Clear!!", [int(self.display_height / 3), int(self.display_width / 4)], scale=7, thickness=5, offset=20, colorR=(0, 0, 0), colorT=(0, 0, 255))
        cvzone.putTextRect(main_img, f"Your Score: {self.score}", [int(self.display_height / 3), int(self.display_width / 3)], scale=7, thickness=5, offset=20, colorR=(0, 0, 0), colorT=(0, 0, 255))
        self.stage_audio.stop()
        _play_with_simpleaudio(self.success_audio)
        cv2.imshow("game success", main_img)
        while True:
            if cv2.waitKey(1) == ord("q"):
                break
        cap.release()
        cv2.destroyAllWindows()

    def filed(self, main_img, cap):
        cvzone.putTextRect(main_img, "Game Over", [int(self.display_height / 2), int(self.display_width / 4)], scale=7, thickness=5, offset=20, colorR=(0, 0, 0), colorT=(0, 0, 255))
        cvzone.putTextRect(main_img, f"Your Score: {self.score}", [int(self.display_height / 3), int(self.display_width / 3)], scale=7, thickness=5, offset=20, colorR=(0, 0, 0), colorT=(0, 0, 255))
        self.stage_audio.stop()
        _play_with_simpleaudio(self.failed_audio)
        cv2.imshow("game failed", main_img)
        while True:
            if cv2.waitKey(1) == ord("q"):
                break
        cap.release()
        cv2.destroyAllWindows()


LuigiMansion().index()
