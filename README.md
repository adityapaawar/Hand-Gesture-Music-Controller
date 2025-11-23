Hand Gesture Music Controller

Control your music with just your hand gestures!

Features

Play / Pause Music: Show all 5 fingers to play or pause your music.

Next Track: Show 2 fingers to skip to the next song.

Volume Control:

Volume Up: Show 1 finger.

Volume Down: Pinch thumb + index finger.

Mute / Unmute: Make a fist → toggles mute.

Fast Forward / Rewind: Swipe your hand right → next track, left → previous track.

Gesture Visualization: Hand landmarks and connections are drawn on your hand in real-time.

Dynamic Visual Effects: Landmarks change color depending on the current action.

Cross-Application Control: Works with any media player responding to keyboard media keys.

Real-Time Feedback: Current action is displayed on the screen.

How to Use

Make sure you have a webcam connected.

Install required packages:

pip install -r requirements.txt


Run the program:

python main.py


Control music with your hand gestures:

Gesture	Action
5 fingers	Play / Pause
2 fingers	Next Track
1 finger	Volume Up
Thumb + Index Pinch	Volume Down
Fist	Mute / Unmute
Swipe Right	Fast Forward
Swipe Left	Rewind

Quit the program by pressing Q.

Requirements

Python 3.x

OpenCV (opencv-python)

MediaPipe (mediapipe)

PyAutoGUI (pyautogui)

NumPy (numpy)

Install all dependencies:

pip install -r requirements.txt

Notes

Works best with well-lit environments.

Only one hand is supported at a time.

Can be used with any media player that responds to keyboard media keys.
