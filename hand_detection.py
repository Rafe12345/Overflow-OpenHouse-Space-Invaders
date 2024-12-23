import mediapipe as mp
import cv2
import threading

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    model_complexity=1,
    min_detection_confidence=0.8,
    min_tracking_confidence=0.8,
    max_num_hands=2
)
mp_drawing = mp.solutions.drawing_utils

# Shared variable for hand status
hand_status = {"left": False, "right": False}

# Hand Detection Thread
def hand_detection_thread():
    global hand_status
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1000)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Flip frame for a mirrored view
        frame = cv2.flip(frame, 1)

        # Convert BGR to RGB for MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        # Reset hand status
        hand_status["left"] = False
        hand_status["right"] = False

        # Check detected hands
        if results.multi_hand_landmarks:
            for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                hand_label = handedness.classification[0].label  # "Left" or "Right"
                hand_status[hand_label.lower()] = True
                wrist_y = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y
                # Determine if the hand is raised (arbitrary threshold)
                # if wrist_y < 0.5:  # Adjust based on camera angle
                #     hand_status[hand_label.lower()] = True
            # Draw landmarks on the video frame
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        cv2.imshow("Hand Detection", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
    hands.close()

# Start Hand Detection Thread
thread = threading.Thread(target=hand_detection_thread, daemon=True)
thread.start()


