import cv2
import numpy as np
import math

minarea = 1000

cap = cv2.VideoCapture(0)


def hareket(x, y, area_param):
    har_y = 500 * math.tanh((3 * x / 500 - 9)) + 1500
    har_x = 500 * math.tanh((3 * y / 500 - 9)) + 1500
    return har_x, har_y


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
    yellow_mask = cv2.inRange(image, lower, upper)

    ret, thresh = cv2.threshold(yellow_mask, 127, 255, 1)

    contours, h = cv2.findContours(thresh, 1, 2)

    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
        x, y = approx[0][0]
        # print(len(approx))
        area = cv2.contourArea(cnt)

        if len(approx) == 4 and minarea <= area < width * height * 0.8:
            M = cv2.moments(cnt)
            # print( M )

            center_x = int(M['m10'] / M['m00'])
            center_y = int(M['m01'] / M['m00'])
            print("rectangle")
            print("x: ", center_x, "y: ", center_y)
            print("**")
            cart = [0, 0, 0, 0]
            cart[0] = width / 2 - 1  # x_ax_pos
            cart[1] = height / 2 - 1  # y_ax_pos
            cart[2] = center_x - cart[0]  # x
            cart[3] = - center_y + cart[1]  # y
            # print(cart)

            cv2.putText(yellow_mask, "X: " + str(cart[2]) + " Y: " + str(cart[3]), (center_x + 20, center_y + 20),
                        cv2.FONT_HERSHEY_COMPLEX, .7,
                        (0, 255, 0), 2)

            cv2.drawContours(yellow_mask, [cnt], 0, 255, -1)
            cv2.circle(yellow_mask, (center_x, center_y), 1, (0, 0, 255), 3)

            print(hareket(cart[2], cart[3], area))

    cv2.imshow("mask", yellow_mask)
    # result = frame.copy()

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
