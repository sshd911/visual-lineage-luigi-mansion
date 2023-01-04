<h1 align='center'>Visual Lineage - Luigi Mansion</h1>
Easily Luigi Mansion with computer vision using handtrackig

## Usage

When a black screen appears, hold your hand in front of the screen. Your index finger will be tracked, and moving your index finger will move Luigi.

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
