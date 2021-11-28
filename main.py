import cv2
import numpy as np

video1 = cv2.VideoCapture('samples/sample1.mp4')
video2 = cv2.VideoCapture('samples/sample2.mp4')
bar = cv2.imread('samples/bg.jpeg')
logo = cv2.imread('samples/logo.jpeg')
save_name = "output.mp4"
fps = video1.get(cv2.CAP_PROP_FPS)
width = 690
height = 360
output_size = ((width * 2), height)

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(save_name, fourcc, fps, output_size)


def connect_frame(frame1, frame2, width, height):
    frame2 = cv2.resize(frame2, (int(width), int(height)), interpolation=cv2.INTER_AREA)
    bg = cv2.resize(frame1, (int(width + width), int(height)), interpolation=cv2.INTER_AREA)
    bg[0:int(height), 0:int(width)] = frame1
    bg[0:int(height), int(width):int(width + width)] = frame2
    return (bg)


while True:

    ret1, frame1 = video1.read()
    ret2, frame2 = video2.read()

    if ret1 is not False and ret2 is not False:

        frame = connect_frame(frame1, frame2, width, height)
        frame = cv2.copyMakeBorder(frame, 20, 20, 20, 20, cv2.BORDER_CONSTANT, value=[255, 255, 255])

        # added left bar
        y_bar = cv2.resize(bar, (int(20), int(height + 40)), interpolation=cv2.INTER_AREA)
        x_bar = cv2.resize(bar, (int(40+width*2), int(20)), interpolation=cv2.INTER_AREA)
        img_height, img_width, _ = y_bar.shape
        x = 0
        y = 0
        frame[x:x + img_height, y:y + img_width] = y_bar

        # added top bar
        img_height, img_width, _ = x_bar.shape
        x = 0
        y = 0
        frame[x:x + img_height, y:y + img_width] = x_bar

        # added bottom bar
        img_height, img_width, _ = x_bar.shape
        x = 40+height-20
        y = 0
        frame[x:x + img_height, y:y + img_width] = x_bar

        # added right bar
        img_height, img_width, _ = y_bar.shape
        x = 0
        y = 40+width*2-20
        frame[x:x + img_height, y:y + img_width] = y_bar


        # add logo
        logo = cv2.resize(logo, (int(100), int(100)), interpolation=cv2.INTER_AREA)
        img_height, img_width, _ = logo.shape
        x = 10
        y = 10
        frame[x:x + img_width, y:y + img_height] = logo

        cv2.imshow('Video frame', frame)  # for video showing window
        out.write(cv2.resize(frame, output_size))

        key = cv2.waitKey(1)
        if key != ord('q'):
            continue
        break
    else:
        print("video is not found")
    break
out.release()
cv2.destroyAllWindows()
