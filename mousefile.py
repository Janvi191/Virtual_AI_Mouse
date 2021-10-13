import numpy as np
import autopy  # allow move over mouse
import cv2
import time
from cvzone.HandTrackingModule import HandDetector

wscr, hscr = autopy.screen.size()
# print(wscr, hscr)

###########################################
wcam, hcam = 1045, 780 # width of camera and height of camara
frameR = 300  # Frame reduction
smoothening = 6
#########################################

plocx, plocy = 0, 0
clocx, clocy = 0, 0

cap = cv2.VideoCapture(0)  # for webcamara.. aapdi jode multiple  camara 6 etale 1 camara ....jo 1 camero hoy to 0
# levaanu
# we have to have fix the width and height of camera
cap.set(3, wcam)  # this is for width ...this is prop id for width
cap.set(4, hcam)  # this is for height....this is prop id for height
pTime = 0
detector = HandDetector(maxHands=1)  # here only one hand is excepting


# def run(img, plocx, plocy, pTime, clocx, clocy, frameR=100, smoothening=6,wcam=1280, hcam=780):

while True:  # this for capture for everytime
    # 1>)FIND THE LANDMARKS
    success, img = cap.read()  # for get our framework  ...it give image and if code sucess or not
    # print(success)
    hands, img = detector.findHands(img)  # for detect hand  distance from all fingures and darw image and return it
    # Set inital values of landMark and fingers
    lmList = 0  # use for give the detail of evry fingure points  and initial value is 0
    fin_dis = 0  # distance between two fingures

    # Check if hand present
    if hands:
        # Get the values for Hand 1
        # hands=[hand1,hand2]
        hand1 = hands[0]  # 1 haath aapse
        # hand1 = [lmList, bbox, center, type]
        # hand2 = [lmList, bbox, center, type]
        lmList = hand1["lmList"]  # List of 21 Landmark points
        # bbox = hand1["bbox"]  # Bounding box info x,y,w,h
        # centerPoint = hand1['center']  # center of the hand cx,cy
        # handType = hand1["type"]  # Handtype Left or Right

        # Get fingers
        # fingers = detector.fingersUp(hand1)  #
        # Get info of distance of fingers
        # fin_dis1, info1, img = detector.findDistance(p1=lmList1[8], p2=lmList1[12],
        # img=img)  # info  between two fingures hole infprmation
        # print(info1)

        # 2>)Get the tip of the index and middle fingures
        if len(lmList) != 0:
            x1, y1 = lmList[8][0:]
            x2, y2 = lmList[12][0:]
            # print(x1, y1, x2, y2)
            # print(lmList[8])
            # 3>)check which fingures are up
            fingers = detector.fingersUp(hand1)
            # print(fingers)
        cv2.rectangle(img, (frameR, frameR), (wcam - frameR, hcam - frameR),
                      (255, 8, 255), 2)  # making rectengle for the mouse
        # 4>)ONLY INDEX FINGER  : MOVING MODE
        if fingers[1] == 1 and fingers[
            2] == 0:  # peli(index fingure) fingure up hoy and biji(middle fingure) fingure down hoy

            # IF IT IS IN MOVING MODE THEN WE ARE DO STEP 5
            # 5>)CONVERT OUR CORDINATES   # HERE OUR WEBCAME GIVEUS 648 TO 480  AND FOR MY SCREEN I HAVE FULL HD MEANS 920 X 1080 SO WE HAVE TO CONVERT CORDINATE TO GE CORRECT POSITION
            wscr, hscr = autopy.screen.size()
            x3 = np.interp(x1, (frameR, wcam - frameR), (0, wscr))
            y3 = np.interp(y1, (frameR, hcam - frameR), (0, hscr))

            # 6>) SMOTHEN VALUES:-- ana thi muse na erroe ni smoothnes aave
            clocx = plocx + (x3 - plocx) / smoothening
            clocy = plocy + (y3 - plocy) / smoothening
            # 7>)MOVE OUR MOUSE
            autopy.mouse.move(wscr - clocx,
                              clocy)  # x3 ni badale wsce-x3 lakhyu becoz we are flip the error etale error ne right side lai jaie e to right sside jase as well as left
            cv2.circle(img, (x1, y1), 15, (0, 0, 255), cv2.FILLED)
            plocx, plocy = clocx, clocy

        # 8>)CHECK CLIKING MODE:-BOTH INDEX AND MIDDLE FINGURES ARE UP --> THEN IT IS IN CLICKING MODE
        if fingers[1] == 1 and fingers[2] == 1:
            # 9>)IF IN THE CLICKING MODE THEN FIND DISTANCE BETWEEN TWO FINGURES .... IF DISTANCE IS SHORT THEN CLICKING MODE
            length, info, img = detector.findDistance(p1=lmList[8], p2=lmList[12],
                                                      img=img)  # info  between two fingures hole infprmation
            # print(length)
            # 10>)CLICK MOUSE IF DISTANCE SHORT
            if length < 58:
                cv2.circle(img, (info[4], info[5]),
                           15, (0, 255, 0), cv2.FILLED)
                autopy.mouse.click()

    # 11>) FRAME RATE
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img=img, text=str(int(fps)), org=(20, 70), fontFace=cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, fontScale=3,
                color=(0, 0, 225), thickness=3)
    # 12>) DISPLAY
    cv2.imshow("Image", img)  # for show our image
    cv2.waitKey(1)
    # return img, plocx, plocy, pTime, clocx, clocy