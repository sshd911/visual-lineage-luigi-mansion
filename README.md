<h1 align='center'>Visual Lineage - Luigi Mansion</h1>

<div align='center'>

![Untitled_compressed_AdobeExpress](https://user-images.githubusercontent.com/93387572/210764771-390a3c5c-3978-427b-bf9c-24f9dfec86d8.gif)![Untitled__1__AdobeExpress](https://user-images.githubusercontent.com/93387572/210764769-3d263ef5-6046-46a0-a736-5a16293a469f.gif)

Simplified Luigi's Mansion with hand tracking

ハンドトラッキングによる簡易ルイージマンション

</div>

## Usage

The index finger is tracked and you can move Luigi by moving the index finger.
By pressing the keyboard, you can change Luigi's viewpoint alternately to the left and right.。<br />
＊ If KeyboardInterrupt occurs, I would think that running it as an administrator user or granting access to the keyboard would solve the problem.

人差し指がトラッキングされ、人差し指を動かすことでルイージを動かすことができます。
キーボードを押すことで、ルイージの視点を左右交互に変更できます。<br />
＊ KeyboardInterruptが発生した場合は、管理者ユーザーで実行するか、キーボードへのアクセス権を付与することで解決するかと思います。

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
  - keyboard >= 0.13.0
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
