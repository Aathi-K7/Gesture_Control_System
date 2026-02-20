import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# Start Camera (USB Camera = 0)
cap = cv2.VideoCapture(0)

# Reduce resolution for Raspberry Pi performance
cap.set(3, 640)
cap.set(4, 480)

finger_tips = [4, 8, 12, 16, 20]

while True:
    success, frame = cap.read()
    if not success:
        print("Camera not working")
        break

    # Flip for mirror view
    frame = cv2.flip(frame, 1)

    # Convert BGR to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb_frame)

    finger_count = 0

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            landmarks = hand_landmarks.landmark

            # Thumb
            if landmarks[finger_tips[0]].x < landmarks[finger_tips[0] - 1].x:
                finger_count += 1

            # Other 4 fingers
            for tip in finger_tips[1:]:
                if landmarks[tip].y < landmarks[tip - 2].y:
                    finger_count += 1

    # Gesture Name
    gesture = ""

    if finger_count == 0:
        gesture = "Fist"
    elif finger_count == 1:
        gesture = "One"
    elif finger_count == 2:
        gesture = "Two"
    elif finger_count == 3:
        gesture = "Three"
    elif finger_count == 4:
        gesture = "Four"
    elif finger_count == 5:
        gesture = "Five"

    # Display Gesture
    cv2.putText(frame, f'Fingers: {finger_count}', (10, 70),
                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)

    cv2.putText(frame, f'Gesture: {gesture}', (10, 130),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    cv2.imshow("Gesture Control System", frame)

    # Press Q to Exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
