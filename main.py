import cv2
import mediapipe as mp
import time
import pyautogui
import math

#fps, 1 is the webcam listed
cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

#FPS, previous \ current time
pTime = 0
cTime = 0

while True:
    #might be able to supply a new background image here or split camera data from overlay
    success, img = cap.read()
    #Adjusts window size, may need to take in screen or windows parameters or adjust with gui
    #to-do invert it so hand moves correctly on screen, make movement 1:1
    img = cv2.resize(img, None, None, fx=3, fy=3)

    #converts image to picture for mpHands
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    #print(results.multi_hand_landmarks)
    if results.multi_hand_landmarks:
        #iterates through hands
        for handLms in results.multi_hand_landmarks:
            p1 = [0, 0]
            p2 = [0, 0]
            for id, lm in enumerate(handLms.landmark):
                #id gives the hand and lm does the joint num and position
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                if id == 4:
                    p1.insert(0, cx)
                    p1.insert(1, cy)
                if id == 8:
                    if cx != 0:
                        pyautogui.moveTo(cx, cy)
                        p2.insert(0, cx)
                        p2.insert(1, cy)
                        distance = math.sqrt( ((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2) )
                        print(distance)
                        if distance < 70:
                            pyautogui.mouseDown(button="left")
                        if distance > 71:
                            pyautogui.mouseUp(button="left")
                """
                if p1[0] != 0:
                    if distance < 50:
                        pyautogui.mouseDown(button="left")
                    else:
                        pyautogui.mouseUp(button="left")
                """

                #check which join is which 8 \ 4 : pointer \ thumb
                #cv2.putText(img, str(id), (cx,cy), cv2.FONT_ITALIC, 3, (255,0,255), 3)
                """ 
                used to track which finger an sorting through them
                if id == 4:
                    cv2.circle(img, (cx,cy), 15, (0,255,0), cv2.FILLED)
                    print(id, cx, cy)
                    pyautogui.moveTo(cx, cy)
                """



            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)


    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_ITALIC, 3, (255,0,255), 3)

    #display
    cv2.imshow("Image", img)
    cv2.waitKey(1);