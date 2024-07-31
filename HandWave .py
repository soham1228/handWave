import cv2
import mediapipe as mp
import pyautogui
import webbrowser
import os
import time

# Initialize video capture, hand detector, and drawing utils
cap = cv2.VideoCapture(0)
hand_detector = mp.solutions.hands.Hands(max_num_hands=1)
drawing_utils = mp.solutions.drawing_utils
screen_width, screen_height = pyautogui.size()

# Initialize variables for hand landmarks
palm_y, palm_x = 0, 0
index_y, index_x = 0, 0
pinky_y, pinky_x = 0, 0  
middle_y, middle_x = 0, 0
thumb_y, thumb_x = 0, 0
ring_y, ring_x = 0, 0

# Web browser opening control
web_frame_count = 0
WEB_THROTTLE_RATE = 2
web_opened = False

# Mouse click control

is_clicking = False 
CLICK_DELAY = 1

# OpenCV window setup
window_name = 'AiMouse'
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
cv2.moveWindow(window_name, 0, 0)  # Set window position  
cv2.resizeWindow(window_name, 600, 550)  # Set window size

try:
    while True:
        start_time = time.time()
        ret, frame = cap.read()
        if not ret:
            break
        
        frame = cv2.flip(frame, 1)
        frame_height, frame_width, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        output = hand_detector.process(rgb_frame)
        hands = output.multi_hand_landmarks

        if hands:
            for hand in hands:
                drawing_utils.draw_landmarks(frame, hand, mp.solutions.hands.HAND_CONNECTIONS)
                landmarks = hand.landmark
                landmarks = hand.landmark

                for id, landmark in enumerate(landmarks):
                    x = int(landmark.x * frame_width)
                    y = int(landmark.y * frame_height)
                    
                    if id == 0:
                        cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 0, 0), thickness=-1)
                        palm_x = screen_width / frame_width * x
                        palm_y = screen_height / frame_height * y
                        pyautogui.moveTo(palm_x, palm_y)
                    
                    elif id == 8:
                        cv2.circle(img=frame, center=(x, y), radius=10, color=(128, 0, 0), thickness=-1)
                        index_x = screen_width / frame_width * x
                        index_y = screen_height / frame_height * y
                    
                    elif id == 4:
                        cv2.circle(img=frame, center=(x, y), radius=10, color=(122, 122, 122), thickness=-1)
                        thumb_x = screen_width / frame_width * x
                        thumb_y = screen_height / frame_height * y
                        if abs(index_y - thumb_y) < 50 and abs(index_x - thumb_x) < 50:
                            if not is_clicking:
                                pyautogui.mouseDown()
                                is_clicking = True
                        else:
                            if is_clicking:
                                pyautogui.mouseUp()
                                is_clicking = False
                    
                    elif id == 20:
                        cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 0, 255), thickness=-1)
                        pinky_x = screen_width / frame_width * x
                        pinky_y = screen_height / frame_height * y
                        if web_frame_count % WEB_THROTTLE_RATE == 0 and not web_opened:
                            if abs(pinky_y - thumb_y) < 50 and abs(pinky_x - thumb_x) < 50:
                                webbrowser.open('http://www.google.com')
                                web_opened = True
                        web_frame_count += 1
                        if web_frame_count > 50:
                            web_opened = False
                            web_frame_count = 0
                    
                    elif id == 12:
                        cv2.circle(img=frame, center=(x, y), radius=10, color=(255, 105, 180), thickness=-1)
                        ring_x = screen_width / frame_width * x
                        ring_y = screen_height / frame_height * y
                        if abs(ring_y - thumb_y) < 50 and abs(ring_x - thumb_x) < 50:
                            pyautogui.hotkey('ctrl', 'c')
                    
                    elif id == 16:
                        cv2.circle(img=frame, center=(x, y), radius=10, color=(225, 155, 200), thickness=-1)
                        middle_x = screen_width / frame_width * x
                        middle_y = screen_height / frame_height * y
                        if abs(middle_y - thumb_y) < 50 and abs(middle_x - thumb_x) < 50: 
                            pyautogui.hotkey('ctrl', 'v')
                        #if abs(middle_y - index_y) == 0:
                            #os.system("start osk")
        
        # Update OpenCV window
        cv2.imshow(window_name, frame)
        cv2.moveWindow(window_name, 0, frame_height-250)
        
        key = cv2.waitKey(1)
        if key == ord('q'):
            break

        # Throttle frame processing to 30 FPS
        elapsed_time = time.time() - start_time
        if elapsed_time < 1.0 / 30:
            time.sleep(1.0 / 30 - elapsed_time)
finally:
    cap.release()
    cv2.destroyAllWindows()
