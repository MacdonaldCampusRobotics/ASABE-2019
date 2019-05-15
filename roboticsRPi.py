############################
#  Coded by Jaesung Park   #
#     Mar. 29, 2019        #
############################

import cv2 as cv
import numpy as np

# Video capture
cap = cv.VideoCapture(0)

while(True):
    # video to image
    ret, img_color = cap.read()
    #cv.imshow("video", img_color)

    img_hsv = cv.cvtColor(img_color, cv.COLOR_BGR2HSV)

    # For Mask Generation from HSV value
    lower_blueA1 = np.array([70,120,30])
    upper_blueA1 = np.array([110,255, 255])
    lower_bgr = np.array([0,150,0])
    upper_bgr = np.array([255,255, 255])
    lower_redA1 = np.array([0,120,30])
    upper_redA1 = np.array([10,255, 255])
    lower_redA2 = np.array([170,120,30])
    upper_redA2 = np.array([180,255, 255])
    img_maskB = cv.inRange(img_hsv, lower_redA1, upper_redA1)
    img_maskC = cv.inRange(img_hsv, lower_redA2, upper_redA2)
    img_green = cv.inRange(img_hsv, lower_blueA1, upper_blueA1)
    img_red = cv.bitwise_or(img_maskB, img_maskC)
    img_sum = cv.bitwise_or(img_red, img_green)

    # Morphology computation
    kernel = np.ones((15,15), np.uint8)
    img_maskA = cv.morphologyEx(img_sum, cv.MORPH_OPEN, kernel)
    img_maskB = cv.morphologyEx(img_sum, cv.MORPH_CLOSE, kernel)

    # Mask generation
    img_maskC = cv.bitwise_or(img_maskA, img_maskB)
    img_result = cv.bitwise_and(img_color, img_color, mask=img_maskC)
    #cv.imshow('img_result', img_result)

    ##original contour##
    contours, hierarchy = cv.findContours(img_maskC, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    cv.drawContours(img_color, contours, -1, (255, 0, 0), 3)  # blue

    #for cnt in contours:
    try:
        #finding maximum size contour
        areas = [cv.contourArea(c) for c in contours]
        max_index = np.argmax(areas)
        cnt=contours[max_index]

        #making convex hull and detecting convexivitydefects
        hull = cv.convexHull(cnt, returnPoints=False)
        defects = cv.convexityDefects(cnt, hull)
        count_defect = 0

        for i in range(defects.shape[0]):
            s, e, f, d = defects[i, 0]
            start = tuple(cnt[s][0])
            end = tuple(cnt[e][0])
            far = tuple(cnt[f][0])
            if d > 3000:
                cv.line(img_color, start, end, [0, 255, 255], 5)
                cv.circle(img_color, far, 5, [255,255,0], -1)
                count_defect=count_defect+1

        if cv.countNonZero(img_green) > cv.countNonZero(img_red):
            leaf_color="The color is Green"
        else:
            leaf_color = "The color is Red"

        # Number of Leaves
        leaf_number=0
        if count_defect>5 :
            leaf_number="Number of Leaves = 4"
        else:
            leaf_number="Number of Leaves = 2"
		print(leaf_color)
		print("-")
		print(leaf_number)
		print("\n")
        # Text in video or Picture
        #cv.putText(img_color, leaf_color, (100, 100), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255),2)
        #cv.putText(img_color, leaf_number, (100, 140), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255),2)

        # If there is no contour
    except:
        #cv.putText(img_color, "no contour", (100, 100), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)

    # Showing result
    #cv.imshow("convex", img_color)


    # Press ESC when you want to finish this program
    key = cv.waitKey(1) & 0xFF
    if key == 27: # esc
        break

cv.destroyAllWindows()


