# import rovpy
import time
import movement_test

frameWidth = 640
frameHeight = 480


def movement(x_raw, y_raw, area_raw):
    har_x = 0.3912 * x_raw + 1375
    har_y = 1.0438 * y_raw + 1250
    har_z = -(100 * area_raw / (frameWidth * frameHeight)) / 40 * 276 + 1776
    return har_x, har_y, har_z


while True:
    x, y, area = movement_test.return_object()
    mesafe = 100  # sensör çağır

    if x and y == -1:
        if mesafe < 50:
            print("Sola dönülüyor")
        # yaw(1400)
        else:
            print("Düz ilerleniyor")
        # forward(1600)
    else:
        print("Hedefe ilerleniyor")  # hedefe ilerle


