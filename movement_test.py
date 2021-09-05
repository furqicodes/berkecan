import cv2
import numpy as np
import math

flag = False
min_area = 1000
frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)


def return_object():
    if flag:
        return center_x, center_y, area
    else:
        return -1, -1, -1


# def movement(x_raw, y_raw, area_raw):
#     har_x = 0.3912 * x_raw + 1375
#     har_y = 1.0438 * y_raw + 1250
#     har_z = -(100 * area_raw / (frameWidth * frameHeight)) / 40 * 276 + 1776
#     return har_x, har_y, har_z


while True:
    success, frame = cap.read()
    height, width, channels = frame.shape

    if not success:
        break

    # converted = convert_hls(img)
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2HLS)

    # yellow color mask
    lower = np.uint8([10, 0, 100])
    upper = np.uint8([40, 255, 255])
    # lower = np.uint8([100, 100, 100])
    # upper = np.uint8([200, 200, 200])
    yellow_mask = cv2.inRange(image, lower, upper)

    ret, thresh = cv2.threshold(yellow_mask, 127, 255, 1)

    contours, h = cv2.findContours(thresh, 1, 2)

    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
        x, y = approx[0][0]
        # print(len(approx))
        area = cv2.contourArea(cnt)

        if len(approx) == 4 and min_area <= area < width * height * 0.8:
            M = cv2.moments(cnt)
            # print( M )

            center_x = int(M['m10'] / M['m00'])
            center_y = int(M['m01'] / M['m00'])
            # print("rectangle")
            # print("x: ", center_x, "y: ", center_y)
            # print("**")
            cv2.putText(yellow_mask, "X: " + str(center_x) + " Y: " + str(center_y), (center_x, center_y),
                        cv2.FONT_HERSHEY_COMPLEX, .7,
                        (255, 255, 0), 2)

            cv2.drawContours(yellow_mask, [cnt], 0, 255, -1)
            cv2.circle(yellow_mask, (center_x, center_y), 1, (0, 0, 255), 3)

            flag = True
            # print(movement(center_x, center_y, area))
        else:
            flag = False

    cv2.imshow("mask", yellow_mask)
    # result = frame.copy()

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
