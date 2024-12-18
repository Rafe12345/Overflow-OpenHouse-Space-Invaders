import mediapipe as mp
import cv2
import threading

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    model_complexity=1,
    min_detection_confidence=0.75,
    min_tracking_confidence=0.75,
    max_num_hands=2
)

# Shared variable for hand status
hand_status = {"left": False, "right": False}

# Hand Detection Thread
def hand_detection_thread():
    global hand_status
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Flip frame for a mirrored view
        frame = cv2.flip(frame, 1)

        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        # Reset hand status
        hand_status["left"] = False
        hand_status["right"] = False

        # Check detected hands
        if results.multi_hand_landmarks:
            for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                hand_label = handedness.classification[0].label  # "Left" or "Right"
                wrist_y = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y

                # Determine if hand is raised (arbitrary threshold)
                if wrist_y < 0.5:  # Adjust threshold based on your camera's angle
                    hand_status[hand_label.lower()] = True

        if cv2.waitKey(1) & 0xFF == 27:  # Exit on ESC key
            break

    cap.release()
    cv2.destroyAllWindows()
    hands.close()

# Start Hand Detection Thread
thread = threading.Thread(target=hand_detection_thread, daemon=True)
thread.start()
