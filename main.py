import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time

# ----------------- Setup -----------------
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.8)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

# Gesture cooldown (seconds)
cooldown = 1.0
last_action_time = 0

# Swipe detection
prev_x = None

# Mute state
is_muted = False

# ----------------- Functions -----------------
def fingers_up(hand_landmarks):
    tips = [4, 8, 12, 16, 20]
    fingers = []

    # Thumb
    if hand_landmarks.landmark[tips[0]].x < hand_landmarks.landmark[tips[0] - 1].x:
        fingers.append(1)
    else:
        fingers.append(0)

    # Other 4 fingers
    for tip in tips[1:]:
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)
    return fingers

def distance(point1, point2):
    return np.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

# ----------------- Main Loop -----------------
while True:
    ret, img = cap.read()
    if not ret:
        break

    img = cv2.flip(img, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    current_time = time.time()

    action_text = ""

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            # Dynamic color based on action
            color = (0, 255, 0)

            mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS, mp_draw.DrawingSpec(color=color))

            fingers = fingers_up(handLms)
            num_fingers = sum(fingers)

            # Play/Pause - 5 fingers
            if num_fingers == 5 and current_time - last_action_time > cooldown:
                pyautogui.press('playpause')
                action_text = "Play/Pause"
                color = (0, 255, 255)
                last_action_time = current_time

            # Next Track - 2 fingers
            elif num_fingers == 2 and current_time - last_action_time > cooldown:
                pyautogui.press('nexttrack')
                action_text = "Next Track"
                color = (255, 0, 0)
                last_action_time = current_time

            # Volume Up - 1 finger
            elif num_fingers == 1 and current_time - last_action_time > cooldown:
                pyautogui.press('volumeup')
                action_text = "Volume Up"
                color = (0, 0, 255)
                last_action_time = current_time

            # Volume Down - pinch (thumb + index)
            thumb = handLms.landmark[4]
            index = handLms.landmark[8]
            dist = distance(thumb, index)
            if dist < 0.05 and current_time - last_action_time > cooldown:
                pyautogui.press('volumedown')
                action_text = "Volume Down"
                color = (255, 255, 0)
                last_action_time = current_time

            # Mute / Unmute - fist (no fingers up)
            if num_fingers == 0 and current_time - last_action_time > cooldown:
                pyautogui.press('volumemute')
                is_muted = not is_muted
                action_text = "Muted" if is_muted else "Unmuted"
                color = (0, 255, 255)
                last_action_time = current_time

            # Swipe left / right - fast forward / rewind
            x_index = int(handLms.landmark[8].x * img.shape[1])
            if prev_x is not None:
                if x_index - prev_x > 100 and current_time - last_action_time > cooldown:
                    pyautogui.press('nexttrack')
                    action_text = "Fast Forward"
                    last_action_time = current_time
                elif prev_x - x_index > 100 and current_time - last_action_time > cooldown:
                    pyautogui.press('prevtrack')
                    action_text = "Rewind"
                    last_action_time = current_time
            prev_x = x_index

            # Display current action
            if action_text != "":
                cv2.putText(img, action_text, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 3)

    cv2.imshow("Enhanced Hand Gesture Music Controller", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
