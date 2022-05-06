import cv2
import mediapipe as mp
import time

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

    #converts image to picture for mpHands
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    #print(results.multi_hand_landmarks)
    if results.multi_hand_landmarks:
        #iterates through hands
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                #id gives the hand and lm does the joint num and position
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                if id == 20:
                    print(id, cx, cy)



            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)


    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_ITALIC, 3, (255,0,255), 3)

    #display
    cv2.imshow("Image", img)
    cv2.waitKey(1);