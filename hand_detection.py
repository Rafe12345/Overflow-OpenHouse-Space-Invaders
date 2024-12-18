import mediapipe as mp
import numpy as np
from PIL import Image, ImageTk
import tkinter as tk
import cv2

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    model_complexity=1,
    min_detection_confidence=0.75,
    min_tracking_confidence=0.75,
    max_num_hands=2
)

cap = cv2.VideoCapture(0)

root = tk.Tk()
root.title("Hand Detection: Left or Right")

label = tk.Label(root)
label.pack()

hand_info_label = tk.Label(root, text="Detecting...", font=("Helvetica", 16))
hand_info_label.pack()

def update_frame():
    success, frame = cap.read()
    if not success:
        return

    # Flip the frame for a mirrored view
    frame = cv2.flip(frame, 1)

    # Convert BGR to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb_frame)
    hand_info_text = "No Hands Detected"

    # Draw hand landmarks directly on the frame
    if results.multi_hand_landmarks:
        for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
            hand_label = handedness.classification[0].label  # "Left" or "Right"

            # Update the hand info text
            hand_info_text = f"{hand_label} Hand Detected"

            for landmark in hand_landmarks.landmark:
                h, w, _ = rgb_frame.shape
                x, y = int(landmark.x * w), int(landmark.y * h)

                rgb_frame[y - 5:y + 5, x - 5:x + 5] = [255, 0, 0] # Draw a red sqaure at each landmark

    hand_info_label.config(text=hand_info_text)
    img = Image.fromarray(rgb_frame)

    imgtk = ImageTk.PhotoImage(image=img)

    label.imgtk = imgtk
    label.configure(image=imgtk)

    root.after(10, update_frame)

update_frame()

# Run the Tkinter event loop
root.mainloop()

# Release resources
cap.release()
hands.close()
