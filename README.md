<h1 align='center'>Visual Lineage - Luigi Mansion</h1>

Easily Luigi Mansion With Computer Vision Using HandTracking

ハンドトラッキングを用いたコンピュータビジョンによる簡易ルイージマンション

## Usage

When the black screen appears, prepare your hand (index finger) as far as the camera can see. 
The index finger will be tracked and you can move Luigi by moving your index finger.
By pressing the keyboard, you can change Luigi's viewpoint alternately to the left and right.
If a KeyboardInterrupt occurs, run the program as an administrator user or check the keyboard access rights.

黒い画面が表示されたら、カメラに映る範囲で手（人差し指）を用意してください。
人差し指がトラッキングされ、人差し指を動かルイージを動かすことができます。
キーボードを押すことで、ルイージの視点を左右交互に変更できます。
KeyboardInterruptが発生した場合は、管理者ユーザーで実行するか、キーボードへのアクセス権を確認してください。

## Installation

```bash
$ git clone https://github.com/sshd911/visual-lineage-luigi-mansion.git && cd visual-lineage-luigi-mansion

# Desctop
$ cd desctop
$ make install
$ make run

# Web
$ cd web
$ make install
$ make run
```

## Requirement

- desktop & web
  - cvzone >= 1.5.0
  - numpy >= 1.2.0
  - pydub >= 0.25.0
  - opencv-python >= 4.7.0
  - opencv_contrib_python >= 4.7.0
  - scipy >= 1.10.0
  - mediapipe
- web
  - Flask >= 2.2.0

###### MacOS Apple Silicon

- desktop & web
  - python >= 3.9.0
  - mediapipe-silicon >= 0.8.0

###### MacOS Intel Tip

###### Windows

###### Linux
